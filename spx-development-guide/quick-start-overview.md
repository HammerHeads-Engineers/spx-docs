---
description: Build a virtual device in minutes, test firmware in seconds.
---

# Quick-Start Overview

### 1. Why SPX?

Hardware tests slow projects down. SPX lets you swap the real device for a digital twin that speaks the same protocol and behaves like the physical unit — including corner cases you cannot trigger on the bench.

Key wins

* Faster iteration – run Model‑in‑the‑Loop tests straight from CI/CD.
* Better coverage – inject failures (over‑temperature, packet loss) safely.
* Open architecture – extend everything: physics, protocols, hooks.

***

### 2. Three concepts you need to know

| Term      | What it is                                           | One‑line memory hook             |
| --------- | ---------------------------------------------------- | -------------------------------- |
| Model     | Blueprint of a device (attributes + actions + logic) | _“CAD file for behaviour.”_      |
| Instance  | Live copy of a model running in a simulation         | _“Device on the lab desk.”_      |
| Attribute | Piece of state with internal & external value        | _“Register you can read/write.”_ |

Everything in SPX descends from `SpxComponent`; collections are auto‑loaded by `SpxContainer`. You rarely touch those bases directly — the DSL takes care of it.

***

### 3. Hello‑World sensor in 15 lines

{% tabs %}
{% tab title="YAML" %}
```yaml
# models/TemperatureSensor.yaml
attributes:
  temperature: 25.0
actions:
  - ramp:     $attr(temperature)
    stop_value: 100
    duration:   5          # seconds
```
{% endtab %}

{% tab title="JSON" %}
```
{}
```
{% endtab %}

{% tab title="Python" %}
model = {

}
{% endtab %}
{% endtabs %}

```python
from spx_core.system.model import Model
import yaml, numpy as np

sensor = Model("Temp", yaml.safe_load(open("models/TemperatureSensor.yaml")))

for t in np.linspace(0, 6, 60):
    sensor["timer"]["time"] = t
    sensor.prepare(); sensor.run()
    print(sensor["attributes"].external["temperature"])
```

No special SDK calls, no hand wiring — the YAML is enough.

***

### 4. Need something special? Extend, don’t rewrite

```python
@register_class(name="spray_cooler")
class SprayCoolerAction(Action):
    def prepare(self, **kw):
        super().prepare(**kw)
        self.kw = self.params.get("coeff", 0.8)

    def run(self, **kw):
        temp = self.resolve_param(self.params["input"])
        return super().run(result=temp * self.kw)
```

Now drop it into YAML:

```python
actions:
  - spray_cooler: $attr(temperature)
    input: $attr(temperature)
    coeff: 0.6
```

***

### 5. Cheat‑sheet for busy engineers

* Add a device: create a folder, add model.yaml, reference it under instances: in your system file.
* Read/Write values: instance\["attributes"].external\["speed"] (external) or .internal\[...].
* Hot‑reload parameters: edit YAML, rerun prepare(); state persists unless you call reset().
* Toggle features: component.enabled = False skips its lifecycle without tearing it out of the tree.
* Debug: set SPX\_LOG=debug to get per‑component logs.

***

### 6. Next steps

1. Clone the example repo and run python examples/pid\_loop.py.
2. Change one attribute, re‑run, watch graphs update.
3. Skim the Component & Container pages to see how hooks and auto‑loading work.
4. Write your first custom Action or Hook — it’s just a subclass with @register\_class.

Happy modelling — and faster shipping!
