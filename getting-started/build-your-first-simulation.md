---
description: >-
  Connect your Python code to a running SPX Server and perform a 10-second
  “smoke test”.
icon: python
---

# Build your first simulation

Make sure the server is running

{% code title="macOS/Linux" %}
```bash
export SPX_PRODUCT_KEY="YOUR_REAL_KEY"
docker compose up -d
```
{% endcode %}

{% code title="Windows PowerShell" %}
```powershell
$env:SPX_PRODUCT_KEY = "YOUR_REAL_KEY"
docker compose up -d
```
{% endcode %}

Server should be reachable at http://localhost:8000/

```bash
curl http://localhost:8000
```

Result message in the shell should look like below:

{% code overflow="wrap" %}
```bash
{"message":"Welcome to SPX Server API","server_version":"0.2.1-alpha.1","api_version":"v3","supported_versions":["v3"]}
```
{% endcode %}

Install the SPX-Python client

```sh
pip install spx-python
```

Connect from Python (smoke test)

{% code title="spx_smoke_test.py" %}
```python
import os 
import spx_python
client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ.get("SPX_PRODUCT_KEY")  #  required env var
)
print(client.keys())  # e.g., ['models', 'instances', 'timer', 'polling']
```
{% endcode %}

## Your first simulation — PT100‑style temperature sensor

This mini‑simulation models a **PT100‑like temperature probe** with two effects:

- A **deterministic ramp with overshoot** that drives the probe’s true temperature over time (the simulation logic). 
- **Proportional standard noise** applied only to the reported temperature, so the visible output becomes noisier as the temperature rises, while the internal logic remains stable and deterministic.

In practice, the ramp updates the internal value, and the noise is added to the external value. This separation makes the behavior easy to reason about: you can clearly see both **stabilization** (from the ramp profile) and **noise growth** (from proportional noise) in logs or plots.

**Why this is useful**
- Great for verifying **set‑point detection** (e.g., “has the system reached 100 °C?”) under realistic measurement noise.
- Lets you test **hysteresis**, **debouncing**, and **noise immunity** in your SUT without touching the underlying simulation logic.
- Deterministic stepping (we advance `timer.time` in fixed increments) makes results reproducible across runs.

```python
# This example defines a PT100-like sensor model with composite actions
# (ramp, noise). Internal temperature is driven by actions; external
# temperature can include noise without affecting internal logic.

import os 
import spx_python
import yaml

client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ.get("SPX_PRODUCT_KEY")  #  required env var
)

pt_100_yaml = '''
attributes:
  temperature: 0.0
actions:
  - { ramp: $in(temperature), stop_value: 150, duration: 5, type: overshoot, overshoot: 5 }
  - { noise: $out(temperature), std: 0.01, mode: proportional }
'''

# Parse YAML and register the model
model_def = yaml.safe_load(pt_100_yaml)
client["models"]["pt_100"] = model_def

# Create an instance and step it deterministically
client["instances"]["pt100_1"] = "pt_100"
inst = client["instances"]["pt100_1"]

client.prepare()
for k in range(1, 101):  # simulate ~10 seconds with dt=0.1
    t = k * 0.1
    inst["timer"]["time"] = t
    client.run()

# Read both layers: internal (true state) vs external (noisy presentation)
print("internal temperature:", inst["attributes"]["temperature"].internal_value)
print("external temperature:", inst["attributes"]["temperature"].external_value)
```

### Extend: add a sawtooth action and disable the ramp


The next snippet shows how to **add a new action** to the running model and **toggle an existing one**. We add a **sawtooth** generator that drives the internal temperature, then **disable** the existing ramp. The noise action remains active on the external value.


**Why this variant is useful**
Switching off the ramp and keeping **saw + noise** changes the character of the test: instead of validating stabilization to a set‑point, you now emulate a **cyclic thermal process** with a sawtooth profile (e.g., periodic heat‑up followed by a reset/cool‑down). This lets you:
- Validate SUT algorithms for **cycle detection** and **period measurement** (is the process truly periodic?).
- Check compliance with expected **sawtooth shape** — amplitude, slope (slew), and overshoot/undershoot tolerances.
- Test robustness of **threshold logic** (correct edge detection, debouncing, avoiding false cycles under noise).
- Compare measured cycle parameters against a **spec** to accept/reject a run (QA workflow).

In short, you move from a “reach set‑point and hold” scenario to a **repeating sawtooth**, which is a common pattern in thermal cycling and endurance tests.

```python
import os
import spx_python
import yaml

client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ.get("SPX_PRODUCT_KEY")  #  required env var
)

pt_100_yaml = '''
attributes:
  temperature: 0.0
actions:
  - { saw: $attr(temperature), stop_value: 14, period: 5 }
  - { ramp: $in(temperature), stop_value: 150, duration: 5, type: overshoot, overshoot: 5 }
  - { noise: $out(temperature), std: 0.01, mode: proportional }
'''

# Parse YAML and register the model
model_def = yaml.safe_load(pt_100_yaml)
client["models"]["pt_100"] = model_def

# Create an instance and step it deterministically
client["instances"]["pt100_1"] = "pt_100"
inst = client["instances"]["pt100_1"]

# 2) Disable the ramp action to keep only: saw + noise
inst["actions"]["ramp"].enabled = False

# 3) Reset/prepare and run again deterministically to observe the behavior
client.prepare()
for k in range(1, 101):  # ~10 seconds with dt=0.1
    t = k * 0.1
    inst["timer"]["time"] = t
    client.run()

print("(saw only) internal:", inst["attributes"]["temperature"].internal_value)
print("(saw only) external:", inst["attributes"]["temperature"].external_value)

# Tip: re-enable the ramp at any time
# inst["actions"]["ramp"].enabled = True
# inst["actions"]["saw"].enabled = False
```