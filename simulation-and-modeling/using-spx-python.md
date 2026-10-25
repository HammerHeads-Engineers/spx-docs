# Using spx-python for Simulation

spx-python is a **Pythonic wrapper around the SPX Server API**. It exposes the SPX system as a **dictionary-like tree** so you can build, control, and inspect simulations directly from Python. With spx-python you can:

- Create models and instantiate them,
- Read/write attributes (internal/external),
- Control simulation time deterministically,
- Run Model-in-the-Loop (MiL) tests, inject faults, and verify outcomes.

> **Key idea:** your production app (SUT) talks to the simulation over the real protocol (MQTT/HTTP/…); meanwhile your **tests** use spx-python as a **control channel** to set parameters, advance time, and check results.

---

## Purpose

spx-python provides **deterministic, programmable control** over SPX simulations:

- Build systems programmatically (models → instances → connections),
- Manipulate parameters and states during execution,
- Advance time explicitly for **reproducible** scenarios,
- Automate MiL tests and edge-case validation,
- Prototype scenarios quickly without hardware.

---

## Installation and Setup

Install from PyPI:

```bash
pip install spx-python
```

Connect to a running SPX Server:

```python
import os
import spx_python

client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ.get("SPX_PRODUCT_KEY", ""),
)

# The client is dict-like. You can inspect top-level keys:
print(list(client.keys()))  # e.g. ['models', 'instances', 'connections', 'timer', 'polling']
```

---

## Core Concepts Recap (client view)

- **Models** – reusable templates. Create/replace with:  
  `client["models"]["MyModel"] = {...}`
- **Instances** – live objects created from models:  
  `client["instances"]["sensor"] = "MyModel"`
- **Attributes** – named values on instances, accessed via:  
  `inst["attributes"]["temperature"].internal_value` (read/write)  
  `inst["attributes"]["temperature"].external_value` (read/write)
- **Connections** – links between attributes across instances:  
  `client["connections"]["c1"] = {"from": "#ext(a.b)", "to": "#in(c.d)"}`
- **Time & run loop** – you advance time and run explicitly:  
  `inst["timer"]["time"] = t; client.prepare(); client.run()`

---

## Quick Start Example (end‑to‑end)

Minimal heater model that raises temperature based on power:

```python
import os
import spx_python

client = spx_python.init("http://localhost:8000", os.environ.get("SPX_PRODUCT_KEY", ""))

# 1) Define a model
client["models"]["Heater"] = {
    "attributes": {
        "temperature": 25.0,
        "power": 0.0,          # control input
    },
    "actions": [
        # temperature <- temperature + 0.2 * power
        {"function": "#ext(temperature)", "call": "#ext(temperature) + 0.2 * #ext(power)"}
    ],
    "timer": {"dt": 0.5},
}

# 2) Create an instance
client["instances"]["room"] = "Heater"
room = client["instances"]["room"]

# 3) Control via internal/external values
room["attributes"]["power"].internal_value = 3.0

# 4) Prepare and step the simulation
client.prepare()
for i in range(6):
    room["timer"]["time"] = (i + 1) * room["timer"].get("dt", 0.5)
    client.run()

print("T =", room["attributes"]["temperature"].external_value)
```

**What to notice**
1) You **assign** a Python dict to `client["models"]["Heater"]`.  
2) You **instantiate** by assigning the model name under `client["instances"]`.  
3) You **set inputs** via `internal_value` or `external_value`.  
4) You **drive time** through `instance["timer"]["time"]` and call `client.run()`.  
5) You **read outputs** from `external_value`.

---

## Attribute Access Cheat Sheet

```python
inst = client["instances"]["room"]

# Read current values
T_int = inst["attributes"]["temperature"].internal_value
T_ext = inst["attributes"]["temperature"].external_value

# Write values
inst["attributes"]["power"].internal_value = 1.5
inst["attributes"]["power"].external_value = 1.5  # both styles are supported
```

> Conventionally, **inputs** are written to `internal_value` and **reported/observable** values are read from `external_value`. Your model can map them as needed.

---

## Multiple Instances and Connections

Create two instances and wire them together:

```python
# Producer: a simple ramp source
client["models"]["Ramp"] = {
    "attributes": {"y": 0.0},
    "actions": [
        {"function": "#ext(y)", "call": "#ext(y) + 1.0"}
    ],
    "timer": {"dt": 1.0},
}

# Consumer: holds an input 'u'
client["models"]["Sink"] = {"attributes": {"u": 0.0}}

client["instances"]["src"] = "Ramp"
client["instances"]["dst"] = "Sink"

# Connect src.y --> dst.u
client["connections"]["c1"] = {
    "from": "#ext(src.y)",
    "to":   "#in(dst.u)"
}

client.prepare()
for t in (1, 2, 3):
    client["instances"]["src"]["timer"]["time"] = float(t)
    client["instances"]["dst"]["timer"]["time"] = float(t)
    client.run()

print(client["instances"]["dst"]["attributes"]["u"].external_value)  # should follow the ramp
```

---

## Using spx-python in MiL Tests (pytest)

Deterministic MiL test that advances time and asserts behavior:

```python
import os
import spx_python
import pytest

@pytest.fixture(scope="module")
def client():
    c = spx_python.init("http://localhost:8000", os.environ.get("SPX_PRODUCT_KEY", ""))
    yield c

def test_heater_increases_temperature(client):
    client["models"]["Heater"] = {
        "attributes": {"temperature": 25.0, "power": 0.0},
        "actions": [
            {"function": "#ext(temperature)", "call": "#ext(temperature) + 0.5 * #ext(power)"}
        ],
        "timer": {"dt": 0.2},
    }
    client["instances"]["uut"] = "Heater"
    inst = client["instances"]["uut"]

    inst["attributes"]["power"].internal_value = 2.0
    client.prepare()

    # advance 1 second in 5 equal steps
    for k in range(1, 6):
        inst["timer"]["time"] = k * 0.2
        client.run()

    temp = inst["attributes"]["temperature"].external_value
    assert temp > 25.0
```

> Your **SUT** can run alongside this test and communicate with the model over the real protocol. The test remains in full control of **time** and **parameters** via spx-python.

---

## LLM Integration and Test Logging Patterns

When you drive SPX with LLM-powered tooling or build test automation, keep these
patterns in mind:

- Treat the client as a dictionary-like tree (`models`, `instances`, `attributes`).
- Keep secrets out of code and examples: set `SPX_PRODUCT_KEY` (and optionally
  `SPX_BASE_URL`) in the environment.
- Prefer helper functions in `spx_python.helpers` for idempotent setup and
  polling (for example: `load_model`, `ensure_model`, `create_instance`,
  `wait_for_attribute_value`, `wait_for_state`).
- For structured test logging, use the helper utilities (for example:
  `spx_log_test_case`, `spx_append_attribute_value`) instead of rolling your own.
- Integration tests should **skip** when `SPX_PRODUCT_KEY` is missing or the
  server is unavailable.

Minimal pytest skip guard:

```python
import os
import pytest

if not os.environ.get("SPX_PRODUCT_KEY"):
    pytest.skip("SPX_PRODUCT_KEY not set", allow_module_level=True)
```

---

## Fault Injection and Edge Cases

Inject a sensor fault mid-run and verify system response:

```python
client["models"]["Sensor"] = {
    "attributes": {"value": 0.0},
    "actions": [{"function": "#ext(value)", "call": "#ext(value) + 0.1"}],
    "timer": {"dt": 0.1},
}
client["instances"]["s1"] = "Sensor"
s1 = client["instances"]["s1"]

client.prepare()
for i in range(5):
    s1["timer"]["time"] = (i + 1) * 0.1
    client.run()

# Inject fault
s1["attributes"]["value"].external_value = 999.0

for i in range(5, 10):
    s1["timer"]["time"] = (i + 1) * 0.1
    client.run()
```

---

## Hot‑Reloading Components (server endpoint)

If your server exposes an admin **reload** endpoint (e.g., `system.reload`), call it before creating new instances to make freshly registered components available. spx-python focuses on the system tree; for custom admin endpoints use `requests`:

```python
import requests

address = "http://localhost:8000"
resp = requests.post(f"{address}/system/reload")
resp.raise_for_status()
```

---

## Best Practices

- **Deterministic time**: always set `instance["timer"]["time"]` before `client.run()`. Keep `timer.dt` consistent for repeatability.
- **Small, focused models**: compose simple units for clearer tests and faster iterations.
- **Separate channels**: let the SUT use the protocol channel; keep spx-python for control/observation.
- **Version scenarios**: store model defs and test seeds in your repo for stable CI.

---

## Further Reading

- [Core Concepts](./core-concepts.md)
- [Model‑in‑the‑Loop](./model-in-the-loop.md)
- API v3 Reference (server endpoints specific to your deployment)
