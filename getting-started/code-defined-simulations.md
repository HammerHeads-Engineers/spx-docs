---
title: Code‑Defined Simulations (Load Python Classes as Models)
description: Build model logic directly in Python and plug it into SPX via YAML/JSON — an alternative to fully declarative models.
---

# Code‑Defined Simulations (Load Python Classes as Models)

Sometimes writing the whole model in YAML/JSON is not the most convenient choice — especially if the core logic is easier to express in Python.  
With **code‑defined simulations**, you implement your model behavior in a Python class and then **import** it into the SPX graph using a small declarative snippet.

This page shows a compact, end‑to‑end example based on a simple “temperature sensor”.

---

## When to use it

- You prefer Python for complex logic or reuse existing libraries.
- You want strict typing, tooling, and unit tests around your model logic.
- You still want the **system structure** (models/instances/connections) to remain declarative and portable.

---

## 1) Write the Python class

Create a file (e.g. `extensions/py_temp_sensor.py`) with your model logic:

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

> You can pass constructor args later from YAML/JSON (see `init` below).

---

## 2) Declare it in YAML (or JSON)

Here is a minimal model that exposes one attribute (`temperature`) and **imports** the Python class with `import` (aka `python_file`) to bind that attribute to the class’ property:

```yaml
# system.yaml (snippet)
models:
  PySensorModel:
    attributes:
      temperature: 25.0
    import:                          # alias for "python_file"
      ./extensions/py_temp_sensor.py:
        class: PyTempSensor
        # optional constructor parameters
        init:
          kwargs:
            start: 25.0
            drift: 0.0
        # map SPX attribute <-> Python property / getters
        attributes:
          temperature: { property: temperature }

instances:
  - sensor: PySensorModel
```

**How it works**

- The `import` section uses the path to your `.py` file as a key and provides:
  - `class`: the class to instantiate from that module
  - `init`: optional `args/kwargs` passed to `__init__`
  - `attributes`: mapping of SPX attribute names to either:
    - `{ property: <python_property_name> }`, or
    - `{ getter: <method>, setter: <method> }`
- Under the hood this is handled by the `python_file` component, which loads the module, creates the object, and wires attributes during `prepare()`.

> Tip: You can use multiple module entries if you want to import several classes.

---

## 3) Make sure your extension directory is loaded

Point SPX at your extension directory and (re)load modules. Depending on your setup you can do this via API v3 or the Python client.

### Via Python client

```python
from spx_python import SPXPython

client = SPXPython("http://localhost:8000", product_key="YOUR_KEY")

# Point to the directory that contains your Python files
client["system"].call("reload_modules", kwargs={"directories": ["./extensions"]})
```

### Via API v3 (generic methods)

```
POST /api/v3/system/method/reload_modules
{
  "kwargs": { "directories": ["./extensions"] }
}
```

> SPX can also scan nested packages; if a package includes a `requirements.txt`,
> those dependencies can be installed/loaded per your environment policy.

---

## 4) Run and inspect

After the import and reload:

- Your instance `sensor` is created from `PySensorModel`.
- The model’s SPX attribute `temperature` is **linked** to `PyTempSensor.temperature`.

You can verify over the generic API:

```
GET /api/v3/system/instances/sensor/attr/temperature
```

Or adjust it:

```
PUT /api/v3/system/instances/sensor/attr/temperature
{ "value": 42.0 }
```

If you exposed a helper like `tick()`, you can call it via methods:

```
POST /api/v3/system/instances/sensor/method/tick
```

---
## 5) (Optional) Expose your Python‑backed attributes over Modbus

You can build **hybrid** models: keep the **logic** in Python, while exposing selected attributes via industrial protocols such as **Modbus**.  
Below is a minimal example that starts a Modbus TCP server and publishes `sensor.temperature` as a holding register. Add a `communications` list with a single `modbus_tcp` entry and map the attribute under `mapping`.

> The exact keys may vary across SPX releases; consult the dedicated **Modbus** guide for the full matrix of options.  
> This example illustrates the concept and the typical shape of the configuration.

```yaml
# Add to your system.yaml
models:
  PySensorModel:
    attributes:
      temperature: 25.0
    import:
      ./extensions/py_temp_sensor.py:
        class: PyTempSensor
        init:
          kwargs: { start: 25.0, drift: 0.0 }
        attributes:
          temperature: { property: temperature }
    communications:
    - modbus_tcp:
        mapping:
          temperature: { address: [0, 1], group: h_r, type: uint_32 }

instances:
  - sensor: PySensorModel
```

**How it works**

- Your instance `sensor` runs Python logic (from `PyTempSensor`), updating `temperature`.


> Tip: You can export multiple attributes by adding more register entries. It’s common to use `encode/scale` to represent floats in fixed‑point registers.

## Advanced options

- **Getter/Setter mapping**  
  Instead of a property you can wire explicit functions:
  ```yaml
  attributes:
    temperature: { getter: read_temp, setter: set_temp }
  ```

- **Multiple classes**  
  Import several classes by listing multiple module entries under `import`.

- **Plain classes vs. SPX components**  
  The importer supports both plain Python classes and classes derived from `SpxComponent`.  
  For `SpxComponent` subclasses, the framework passes context automatically.

---

## Summary

- Keep your **structure** declarative in YAML/JSON (models, instances, connections).
- Put the **behavior** in Python classes when it’s more convenient.
- Use the `import`/`python_file` component to bridge both worlds.
- Reload modules and run — you now have a code‑defined simulation that remains portable and testable.
