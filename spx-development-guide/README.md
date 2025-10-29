---
description: >-
  “Think of it as LEGO® for hardware simulation – snap a few bricks together,
  press Run, and your virtual device comes alive.”
---

# Build Simulations with SPX

### 1. What is SPX‑SDK?

SPX‑SDK is the extension kit for the SPX simulation platform.

It lets you describe digital twins of sensors, controllers, and whole machines in a few lines of YAML or Python, plug them into your software exactly as you would real hardware (TCP, UART, CAN, …), and run full Model‑in‑the‑Loop tests long before a prototype reaches your desk.

***

### 2. Why should I care?

* Faster R\&D – validate ideas hours after the design meeting, not weeks after PCB delivery.
* Edge‑case coverage – inject impossible faults (broken thermocouple at 150 °C) without risking smoke.
* CI/CD friendly – headless simulations run on every commit, preventing regressions in control logic.
* Pluggable – your domain‑specific quirks (custom protocol, exotic physics) are just another brick.

***

### 3. The 60‑second tour

{% tabs %}
{% tab title="YAML" %}
```yaml
# models.yaml
TemperatureSensor:
  attributes:
    temperature: 25.0
    heating_power:
      default: 0.0
      hooks: { on_set: [refresh_model] }
  actions:
    - function: $in(temperature)
      call: $in(temperature) + 0.5 *
            (0.6 * $in(heating_power) - 0.02 * ($in(temperature) - 25))

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "TemperatureSensor": {
    "attributes": {
      "temperature": 25.0,
      "heating_power": {
        "default": 0.0,
        "hooks": {
          "on_set": [
            "refresh_model"
          ]
        }
      }
    },
    "actions": [
      {
        "function": "$in(temperature)",
        "call": "$in(temperature) + 0.5 * (0.6 * $in(heating_power) - 0.02 * ($in(temperature) - 25))"
      }
    ]
  }
}

```
{% endtab %}

{% tab title="Python Dict " %}
```python
models = {
    "TemperatureSensor": {
        "attributes": {
            "temperature": 25.0,
            "heating_power": {
                "default": 0.0,
                "hooks": {
                    "on_set": ["refresh_model"]
                }
            }
        },
        "actions": [
            {
                "function": "$in(temperature)",
                "call": "$in(temperature) + 0.5 * (0.6 * $in(heating_power) - 0.02 * ($in(temperature) - 25))"
            }
        ]
    }
}

```
{% endtab %}
{% endtabs %}

```python
# run.py
from spx_core.system.model import Model
import yaml, numpy as np

system = Model("TempCtrl", yaml.safe_load(open("models.yaml")))
for t in np.linspace(0, 600, 300):
    system["timer"]["time"] = t
    system.prepare(); system.run()
print(system["instances"]["sensor"]["attributes"]["temperature"].external_value)
```

_No firmware‑side changes – your app still speaks the same protocol._

***

### 4.Simulation Building Blocks

| Concept          | What it represents                                                    | In-code example                               |
| ---------------- | --------------------------------------------------------------------- | --------------------------------------------- |
| Model            | Blueprint of a device: attributes, actions and hooks                  | `TemperatureSensor, PowerSupply`              |
| Instance         | One concrete copy of a model inside a running simulation              | `sensor, supply`                              |
| Attribute        | Piece of state with _internal_ (physical) and _external_ (I/O) values | `temperature, power_on`                       |
| Action           | Rule that evolves an attribute over time                              | `ramp, noise, pid, custom spring_mass_damper` |
| Connection       | Virtual wire linking two attributes in different instances            | `sensor_to_controller`                        |
| Hook / Condition | Event engine for side-effects or safety logic                         | `refresh_model, emergency_shutdown`           |
| Communication    | ...                                                                   | `modbus_tcp, http, mqtt`                      |

_All elements are serialised to YAML, version-controlled in Git and reloadable at runtime, so a change in one brick immediately propagates through the whole virtual system._

***

### 5. Extending the toolbox

```python
from spx_sdk.components import SpxComponent
from spx_sdk.registry import register_class

@register_class(name="spring_mass_damper")
class SpringAction(SpxComponent):
    def run(self, *args, **kw):
        # custom physics here …
        pass
```

* @register\_class publishes new Actions, Hooks, Conditions, Protocol adapters, etc.
* Drop‑in adapters let you expose models over a new field‑bus without touching the core.
* Templates generate hundreds of parametrised instances from one definition.

***

### 6. Typical Engineer Workflow

1.  Describe your devices

    Write or generate a YAML file for each model. Keep it human-readable; reviewers can diff it like source code.
2.  Compose the system

    List instances and connections in the same YAML. Add optional _Conditions_ for failsafes.
3. Run the simulation

```python
system = Model("TempCtrl", yaml.safe_load(open("system.yaml")))
for t in np.linspace(0, 600, 300):
    system["timer"]["time"] = t
    system.prepare(); system.run()
```

_Your application talks to the simulator over the normal protocol – no firmware changes needed._

4. Inspect & iterate

* Read attributes live (system\["instances"]\["sensor"]\["attributes"]\["temperature"].external\_value).
* Stream data to Grafana/Prometheus or plot it with Plotly.
* Tweak YAML, hot-reload, rerun.

5. Automate in CI/CD

Headless runner spins up the same YAML on every commit; unit tests assert that, e.g., power\_on is forced False when temperature ≥ 80 °C.

5. Extend when necessary

Need exotic physics or a proprietary bus? Create a new Action or Protocol Adapter with @register\_class, drop it into YAML, and keep building.

> Result: a repeatable, hardware-free test loop that turns “What if…?” into a five-minute experiment instead of a costly lab session.

***

### 7. Next steps

1. Clone examples from the repo and run them locally.
2. Tweak one brick – add a noise action or new Hook and watch the behaviour change.
3. Integrate the simulator in your test harness; flip the real hardware switch when you’re confident.

***

#### Remember

_You don’t have to wrestle with a full‑blown physics engine._

Start small, extend when needed, and keep stacking those LEGO® bricks. Happy simulating!
