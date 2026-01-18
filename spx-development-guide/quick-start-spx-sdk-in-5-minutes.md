---
description: '(file: examples/hello_world_sensor.py)'
icon: code
---

# Quick Start — SPX-SDK in 5 Minutes

> **Goal** 
>
> Feel the entire journey—from pip install to a running simulation—then see how easy it is to bolt on new physics with a single class.

### Prerequisites

| Tool   | Version    |
| ------ | ---------- |
| Python | `>=3.9` (tested `3.9–3.12`) |
| pip    | 23+        |

```bash
pip install --upgrade spx-sdk    # from PyPI
# or, for local dev
git clone https://github.com/HammerHeads-Engineers/spx-sdk.git
cd spx-sdk && pip install -e .
```

***

### **Hello-World Sensor (60 s kettle run)**

Create sensor.yaml

{% tabs %}
{% tab title="YAML" %}
```python
import yaml, numpy as np
from spx_sdk import Model

yaml_str = """
attributes:
  temperature: 25.0            # °C
actions:
  - function: $ext(temperature)
    call: "$in(temperature) + (100 - $in(temperature))            \
           * (1 - 0.945 ** $(.timer.time))"  # slows as it nears 100 °C
"""
sensor = Model("Sensor", yaml.safe_load(yaml_str))
sensor.prepare();
for t in np.arange(0, 60.1, 0.1):              # 0 → 60 s, 0.1 s ticks
    sensor["timer"]["time"] = t                # drive the built-in timer
    sensor.run()
    print(f"{t:4.1f}s ➜ {sensor['attributes']['temperature']['external_value']:.2f} °C")

```
{% endtab %}

{% tab title="JSON" %}
```python
import json, numpy as np
from spx_sdk import Model

json_str = json.dumps({
  "attributes": {"temperature": 25.0},
  "actions": [
    {
      "function": "$ext(temperature)",
      "call": "$in(temperature) + (100 - $in(temperature)) * (1 - 0.945 ** $(.timer.time))"
    }
  ]
})
model_def = json.loads(json_str)

# instantiate and run
sensor = Model(name="Sensor", definition=model_def)
sensor.prepare()
for t in np.arange(0, 60.1, 0.1):
    sensor["timer"]["time"] = t
    sensor.run()
    print(f"{t:5.1f}s → {sensor['attributes']['temperature']['external_value']:.2f}°C")

```
{% endtab %}

{% tab title="Python Dict" %}
```python
import numpy as np
from spx_sdk import Model

# 3) Pure Python dict definition
model_def = {
    "attributes": {"temperature": 25.0},
    "actions": [
        {
            "function": "$ext(temperature)",
            "call": "$in(temperature) + (100 - $in(temperature)) * (1 - 0.945 ** $(.timer.time))"
        }
    ]
}

# instantiate and run
sensor = Model(name="Sensor-Dict", definition=model_def)
sensor.prepare()
for t in np.arange(0, 60.1, 0.1):
    sensor["timer"]["time"] = t
    sensor.run()
    print(f"{t:5.1f}s → {sensor['attributes']['temperature']['external_value']:.2f}°C")

```
{% endtab %}
{% endtabs %}

What just happened?

| Piece                               | Purpose                                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------- |
| Model                               | Alias for BaseModel; auto-installs a timer and polling component.               |
| attributes:                         | Declares a temperature attribute (internal/external values handled for you).    |
| function action                     | Runs every tick; $in reads, $ext writes; $(.timer.time) fetches simulated time. |
| prepare() → run()->run()->run().... | Two-phase loop: resolve parameters, then execute actions.                       |

***

### **Extending in 30 Seconds**

_Add Newton-style cooling without touching core code._

```python
from spx_sdk import register_class
from spx_sdk.actions.action import Action

@register_class("heat_loss")
class HeatLoss(Action):
    """ΔT = −k · (T − ambient) each tick."""
    def _populate(self, d):
        self.k       = d.get("k",       0.01)
        self.ambient = d.get("ambient", 20.0)
        return super()._populate(d)

    def run(self, **_):
        T = self.resolve_param(self.params["T"])
        new_T = T - self.k * (T - self.ambient)
        return self.write_outputs(new_T)
```

Add it to the YAML—no other glue code required:

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - function: $ext(temperature)   # heating
    call: "$in(temperature) + (100 - $in(temperature)) \
           * (1 - 0.945 ** $(.timer.time))"
  - heat_loss: $ext(temperature)  # our new cooling
    T:       $ext(temperature)
    k:       0.01
    ambient: 22.0

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    {
      "function": "$ext(temperature)",
      "call": "$in(temperature) + (100 - $in(temperature)) * (1 - 0.945 ** $(.timer.time))"
    },
    {
      "heat_loss": "$ext(temperature)",
      "T": "$ext(temperature)",
      "k": 0.01,
      "ambient": 22.0
    }
  ]
}

```
{% endtab %}

{% tab title="Python Dict" %}
```python
{
    "actions": [
        {
            "function": "$ext(temperature)",
            "call": (
                "$in(temperature) + (100 - $in(temperature)) "
                "* (1 - 0.945 ** $(.timer.time))"
            )
        },
        {
            "heat_loss": "$ext(temperature)",
            "T":       "$ext(temperature)",
            "k":       0.01,
            "ambient": 22.0
        }
    ]
}

```
{% endtab %}
{% endtabs %}

Run the same loop—now the curve approaches an equilibrium that balances heating and cooling.

***

### **Next Steps 🚀**

| Want to…                         | Look at… |
| -------------------------------- | -------- |
| Build reusable parts             | link...  |
| Create rich conditional logic    | link...  |
| Drive real hardware or protocols | link...  |
| Unit-test your models            | link...  |

> **Remember** 
>
> Every class with @register\_class is auto-registered at package import. No dummy imports, no boilerplate.

Happy modeling!—the SPX-SDK team
