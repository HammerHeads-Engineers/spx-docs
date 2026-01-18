---
title: Code‑Defined Simulations (Load Python Classes as Models)
description: >-
  Build model logic directly in Python and plug it into SPX via YAML/JSON — an
  alternative to fully declarative models.
icon: python
---

# Loading Python Classes as Models

Not every behavior is pleasant to express in YAML/JSON. When the core of your model is easier to write in Python, you can keep the **system structure** (models/instances/connections) declarative, while implementing the **behavior** in a plain Python class and importing it into SPX.\
This guide walks through a small but complete “temperature sensor” example and shows how the Python class is wired to attributes and methods, and how you can later expose those attributes over Modbus.

***

## When to use it

* Your logic is complex enough that Python is clearer than a purely declarative spec.
* You want to reuse existing Python libraries or your own tested code.
* You still need portable system topology (YAML/JSON) for deployment, tests, and tooling.

***

## 1) Write the Python class

Create `extensions/py_temp_sensor.py` and implement the behavior.\
The class below keeps an internal temperature, exposes it via a `temperature` property, and defines a small `tick()` helper that the model can call on each `run()`.

```python
# extensions/py_temp_sensor.py
import math
import time

class PyTempSensor:
    """
    Minimal sensor logic implemented in Python.
    - Keeps an internal temperature value
    - Exposes a property 'temperature' used by SPX
    - Provides a 'tick' helper to update the internal state
    """
    def __init__(self, start: float = 25.0, drift: float = 0.0):
        self._t = start
        self._drift = drift
        self._t0 = time.time()

    # Property used by SPX to read/write the attribute
    @property
    def temperature(self) -> float:
        return self._t

    @temperature.setter
    def temperature(self, val: float):
        self._t = float(val)

    # Optional helper you can call from actions/logic
    def tick(self) -> float:
        # Example: a tiny sinusoid + linear drift
        now = time.time() - self._t0
        self._t = self._t + self._drift + 0.05 * math.sin(now)
        return self._t
```

**What to notice**

* You do **not** need to inherit from any SPX base class. A plain Python class is fine.
* SPX will bind the model’s attributes to your class’ property/getter/setter.
* Any public method (like `tick`) can be mapped to SPX lifecycle methods (e.g., `run`).

***

## 2) Declare it in YAML (or JSON)

Now reference that Python class from a model definition.\
The YAML below defines a `PySensorModel` with one attribute and uses `import` to load `PyTempSensor`. It maps the model’s `temperature` attribute to the class’ `temperature` property and maps the model’s `run` method to the class’ `tick` function.

{% tabs %}
{% tab title="YAML" %}
```yaml
# system.yaml (snippet)
models:
  PySensorModel:
    attributes:
      temperature: 0.0
    import:
        /app/extensions/py_temp_sensor.py:
            class: PyTempSensor
            init:
                kwargs:
                    start: 25.0
                    drift: 0.0
            attributes:
                temperature: { property: temperature }
            methods: 
                run: tick
instances:
  - sensor: PySensorModel
```


{% endtab %}

{% tab title="JSON" %}
```json
{
  "models": {
    "PySensorModel": {
      "attributes": {
        "temperature": 0.0
      },
      "import": {
        "/app/extensions/py_temp_sensor.py": {
          "class": "PyTempSensor",
          "init": {
            "kwargs": {
              "start": 25.0,
              "drift": 0.0
            }
          },
          "attributes": {
            "temperature": { "property": "temperature" }
          },
          "methods": {
            "run": "tick"
          }
        }
      }
    }
  },
  "instances": [
    { "sensor": "PySensorModel" }
  ]
}
```


{% endtab %}
{% endtabs %}

**How the mapping works**

* `import` uses the path to the Python file as a key. SPX loads the module and instantiates `class: PyTempSensor`.
* `init.kwargs` are forwarded to `__init__` (so you can configure defaults from YAML/JSON).
* Under `attributes` you bind each SPX attribute to either:
  * a property on your class: `{ property: temperature }`, or
  * explicit accessors: `{ getter: read_temp, setter: set_temp }`.
* Under `methods` you can map model methods to your Python methods, e.g., `run: tick`.\
  When the instance runs, SPX will call `PyTempSensor.tick()`.

> Internally this is handled by the `python_file` importer. Wiring happens during `prepare()`.

***

## 3) Create a model and instance, then run

The next snippet shows how to use the HTTP wrapper to push the YAML to the server and create a running instance. We also disable background polling to keep the sample deterministic and call `prepare()` to ensure the importer wires up the attributes/methods before use.

```python
import spx_python

# Initialize HTTP-based SPX client wrapper pointing to local SPX server
product_key = os.environ['SPX_PRODUCT_KEY']
wrapper = spx_python.init(address='http://localhost:8000',
                                product_key=product_key)
```

```python
import yaml

# Create a new model for the PT100 sensor
pt_100_yaml = '''
attributes:
  temperature: 0.0
import:
    /app/extensions/py_temp_sensor.py:
        class: PyTempSensor
        init:
            kwargs:
                start: 25.0
                drift: 0.0
        attributes:
            temperature: { property: temperature }
        methods: 
            run: tick
'''

# Parse YAML and build the model
data = yaml.safe_load(pt_100_yaml)
wrapper["models"]["pt_100_py"] = data
wrapper["instances"]["test_pt_100_py"] = "pt_100_py"

instance = wrapper["instances"]["test_pt_100_py"]
instance["polling"].disable()
instance.prepare()

print("Available models:", wrapper["models"].keys())
print("Available instances:", wrapper["instances"].keys())
```

**What happens here**

1. The model is created with the `import` block as defined above.
2. The instance `test_pt_100_py` is added, referencing that model.
3. `prepare()` loads the Python file, instantiates `PyTempSensor`, and connects:
   * the model’s `temperature` attribute ⇄ the `temperature` property,
   * the model’s `run` method ⇄ the `tick()` function.
4. From now on, each `instance.run()` calls `PyTempSensor.tick()`.

***

## 4) Sample and visualize the signal

This final code collects samples by repeatedly calling `run()` (therefore invoking `tick()` under the hood) and plots `temperature` over time with Plotly.

```python
import plotly.graph_objects as go

# --- simulation & sampling ---
STEPS = 1500        # number of ticks
DT = 0.1           # optional: time step used for the X axis (seconds)
times, temps = [], []

temp_attr = instance["attributes"]["temperature"]
temp_attr.internal_value = 50.0  # initial temperature

for step in range(STEPS):
    instance.run()                 # advance the model by one tick
    times.append(step * DT)        # time axis (seconds)
    temps.append(temp_attr.internal_value)  # read current temperature
    # time.sleep(DT)               # uncomment for real delays

# --- plot with Plotly ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=times, y=temps, mode="lines", name="Temperature"))
fig.update_layout(
    title="Temperature over Time",
    xaxis_title="Time [s]",
    yaxis_title="Temperature",
    template="plotly_white",
)
fig.show()
```

**Key takeaways**

* `instance.run()` → mapped to `PyTempSensor.tick()`.
* The `temperature` attribute you read is the property on your class.
* You can choose your own update cadence and time base.

***

## 5) (Optional) Expose your Python‑backed attributes over Modbus

You can build **hybrid** models: keep the logic in Python, and expose selected attributes via industrial protocols such as **Modbus**.\
The YAML below adds a `communication` section to the same model and publishes `temperature` as a holding register with `modbus_slave` (recommended Modbus TCP server adapter).

> Exact keys and encoding options may vary across SPX releases. See the dedicated Modbus guide for full details. The snippet demonstrates the typical shape.

{% tabs %}
{% tab title="YAML" %}
```yaml
# Add to your system.yaml
models:
  PySensorModel:
    attributes:
      temperature: 0.0
    import:
        /app/extensions/py_temp_sensor.py:
            class: PyTempSensor
            init:
                kwargs:
                    start: 25.0
                    drift: 0.0
            attributes:
                temperature: { property: temperature }
            methods: 
                run: tick
    communication:
      - modbus_slave:
          mapping:
            temperature: { address: [0, 1], group: h_r, type: float }

instances:
  - sensor: PySensorModel
```


{% endtab %}

{% tab title="JSON" %}
```json
{
  "models": {
    "PySensorModel": {
      "attributes": {
        "temperature": 0.0
      },
      "import": {
        "/app/extensions/py_temp_sensor.py": {
          "class": "PyTempSensor",
          "init": {
            "kwargs": {
              "start": 25.0,
              "drift": 0.0
            }
          },
          "attributes": {
            "temperature": { "property": "temperature" }
          },
          "methods": {
            "run": "tick"
          }
        }
      },
      "communication": [
        {
          "modbus_slave": {
            "mapping": {
              "temperature": {
                "address": [0, 1],
                "group": "h_r",
                "type": "float"
              }
            }
          }
        }
      ]
    }
  },
  "instances": [
    { "sensor": "PySensorModel" }
  ]
}
```


{% endtab %}
{% endtabs %}

**What this adds**

* A Modbus TCP server is started for the instance.
* The `temperature` attribute is mapped to a pair of holding registers.
* You can extend the mapping with more attributes or different encodings.

***

## Advanced options

*   **Getter/Setter mapping**\
    Prefer explicit functions instead of a property:

    {% tabs %}
    {% tab title="YAML" %}
    ```yaml
    attributes:
      temperature: { getter: read_temp, setter: set_temp }
    ```
    {% endtab %}

    {% tab title="JSON" %}
    ```json
    {
      "attributes": {
        "temperature": {
          "getter": "read_temp",
          "setter": "set_temp"
        }
      }
    }
    ```
    {% endtab %}
    {% endtabs %}
* **Multiple classes**\
  Import several classes by listing multiple module entries under `import`.
* **Plain classes vs. `SpxComponent`**\
  The importer supports both. For `SpxComponent` subclasses, SPX passes context automatically.

***

## Summary

* Keep topology in YAML/JSON (models, instances, connections), but implement behavior in Python where it’s more natural.
* Use the `import`/`python_file` bridge to map **attributes** and **methods** to your class.
* Call `prepare()` before use so the importer wires everything up.
* (Optional) Expose the same attributes over Modbus or other protocols for integration.
