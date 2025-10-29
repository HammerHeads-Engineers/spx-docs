---
icon: puzzle-piece-simple
---

# Extend with a Custom Component

SPX lets you add **custom components** so you can model behaviors that go beyond the built‑ins. In this guide we’ll create a tiny extension that simulates **contact faults** on a PT100 sensor (random spikes or drop‑to‑zero events), load it into a running SPX Server, and use it in a model.

> This article is part of **Getting Started**. It focuses on a minimal, code‑defined workflow.

---

## What you’ll build

- A YAML model that references a new action called `contact_fault`
- A Python implementation of that action (a custom **extension**)
- A short script that:
  - connects to the SPX Server via `spx_python`
  - **reloads extensions** from the configured directories (e.g. `./extensions`)
  - runs a **deterministic time** simulation (you control the clock)

---

## 1) Define the model in YAML

We’ll model a PT100‑like sensor and apply a few actions: a saw, a ramp with overshoot, proportional noise, and our new **contact_fault** action that injects spikes/drops.

{% tabs %}
{% tab title="YAML" %}
```yaml
models:
  pt100_sensor:
    attributes:
      temperature: 0.0
    actions:
      - { saw: $attr(temperature), stop_value: 14, period: 5 }
      - { ramp: $attr(temperature), stop_value: 150, duration: 5, type: overshoot, overshoot: 5 }
      - { noise: $ext(temperature), std: 0.01, mode: proportional }
      - { contact_fault: $ext(temperature), spike_value: 500.0 }  # custom extension

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "models": {
    "pt100_sensor": {
      "attributes": {
        "temperature": 0.0
      },
      "actions": [
        { "saw": "$attr(temperature)", "stop_value": 14, "period": 5 },
        { "ramp": "$attr(temperature)", "stop_value": 150, "duration": 5, "type": "overshoot", "overshoot": 5 },
        { "noise": "$ext(temperature)", "std": 0.01, "mode": "proportional" },
        { "contact_fault": "$ext(temperature)", "spike_value": 500.0 }
      ]
    }
  }
}

```
{% endtab %}
{% endtabs %}


**Why `$ext(...)`?** We typically map fault injections to the *external* view of an attribute so core logic remains stable while the presented value exhibits faults.

---

## 2) Implement the custom action (`contact_fault.py`)

Create `./extensions/contact_fault.py`:

```python
# Minimal implementation of a custom action that simulates intermittent
# contact faults on a PT100-like sensor. It randomly injects either a
# drop-to-zero or a spike to a configured value.

import random
from spx_sdk.actions import Action
from spx_sdk.registry import register_class


@register_class(name="contact_fault")
class ContactFault(Action):
    """Randomly injects spikes/drops into the target signal.

    Parameters from YAML:
      - probability (float): chance to inject a fault each run(). Default: 0.01
      - spike_value (float): value for spike events. Default: 1000.0
      - drop_ratio (float): probability of drop vs spike. Default: 0.5
      - seed (int|None): RNG seed for reproducibility. Default: None
    """

    def _populate(self, definition):
        # sensible defaults
        self.probability = 0.01
        self.spike_value = 1000.0
        self.drop_ratio = 0.5
        self.seed = None
        super()._populate(definition)

    def prepare(self):
        super().prepare()
        random.seed(self.seed)

    def run(self):
        faulted = False
        for output in self.outputs.values():
            if random.random() < float(self.probability):
                if random.random() < float(self.drop_ratio):
                    output.set(0.0)
                else:
                    output.set(float(self.spike_value))
                faulted = True
        return faulted
```

> You can organize extensions as single files **or** full folders/repositories. If an extension folder contains a `requirements.txt`, SPX will attempt to install those dependencies (subject to your server configuration/permissions).

---

## 3) Load the extension in a running SPX Server

Use **spx_python** to connect and then **reload modules**. By default the server scans the configured *extensions directories* (e.g., `./extensions` in the working directory). Ensure your `contact_fault.py` lives in one of those directories.

```python
# SPDX-License-Identifier: MIT
import os
import yaml
import spx_python

spx_python.set_global_transparent(False)  # optional: request server-side execution visibility
product_key = os.environ["SPX_PRODUCT_KEY"]

# Connect to local SPX Server
wrapper = spx_python.init(address="http://localhost:8000", product_key=product_key)

# Reload/scan extension modules from the configured directories (e.g. ./extensions)
wrapper.reload_modules()
```

> **Note**  
> If your extension lives elsewhere, add that directory to the server’s extension search paths (per your deployment settings) before calling `reload_modules()`.

---

## 4) Create a model and run a *deterministic time* simulation

Deterministic means **you** control the clock — the simulation advances when you set `timer.time` and call `run()`.

```python
# Define the PT100 model with our contact_fault action
pt_100_yaml = '''
attributes:
  temperature: 0.0
actions:
  - { saw: $attr(temperature), stop_value: 14, period: 5 }
  - { ramp: $attr(temperature), stop_value: 150, duration: 5, type: overshoot, overshoot: 5 }
  - { noise: $ext(temperature), std: 0.01, mode: proportional }
  - { contact_fault: $ext(temperature), spike_value: 500.0 }
'''

data = yaml.safe_load(pt_100_yaml)

# Register a model and create an instance
wrapper["models"]["pt_100_1"] = data
wrapper["instances"]["test_pt_100"] = "pt_100_1"
instance = wrapper["instances"]["test_pt_100"]

# Deterministic time: disable background polling/timers and drive the clock
instance["polling"].disable()
instance.reset()
instance.prepare()

# Advance time explicitly and run the model
import numpy as np
times = np.linspace(0, 10, 1000)
temperatures = []
temperatures_raw = []

for t in times:
  instance["timer"].time = t
  instance.run()
  temperatures.append(instance["attributes"]["temperature"].external_value)
  temperatures_raw.append(instance["attributes"]["temperature"].internal_value)
```

(Optional) Plot with Plotly:

```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=times, y=temperatures, mode='lines', name='Temperature'))
fig.add_trace(go.Scatter(x=times, y=temperatures_raw, mode='lines', name='Temperature Internal'))
fig.update_layout(
    title='PT100 with contact faults (deterministic time)',
    xaxis_title='Time (s)',
    yaxis_title='Temperature (°C)',
    showlegend=True
)
fig.show()
```

---

## Troubleshooting

- **“Module not found / class not registered”**  
  Ensure your file is inside a configured extensions directory and that you called `wrapper.reload_modules()` after adding it. Check server logs for import errors.

- **Dependencies missing**  
  If your extension needs packages, provide a `requirements.txt` in the extension folder. Whether installs are allowed depends on your server configuration.

- **No spikes visible**  
  Increase `probability` or set a lower `drop_ratio` to bias spikes. You can also set `seed` for reproducible runs.

- **Real‑time vs deterministic time**  
  This example uses deterministic control (`timer.time` + `run()`). For real‑time/polling modes, you would enable polling and use `start()`/`stop()` instead.

---

## Next steps

- Package your extension as a reusable repo and point the server to it
- Add unit tests for your custom component
- Use labels/notes in snapshots to track experiments and reload setups quickly

Happy extending! 🎛️
