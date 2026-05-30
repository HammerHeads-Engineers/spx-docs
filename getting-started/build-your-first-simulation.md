---
description: >-
  Start from a running SPX Server and perform a small PT100-style simulation
  smoke test from Python.
icon: python
---

# Build your first simulation

This page assumes SPX Server is already running at `http://localhost:8000`.
Start it from one of these supported places:

- Installed SPX environment: run `SPX Setup`, let it start the stack, or run
  `SPX Start`.
- Generated installer bundle: from the generated folder, run `./spx-start.sh`
  on macOS/Linux or `pwsh ./spx-start.ps1` on Windows.
- `spx-examples` development checkout: from the `spx-examples` repo root, create
  `.env` with `SPX_PRODUCT_KEY=...`, then run `docker compose up --detach`.

Do not run `docker compose up` from the `spx-docs` repository. The Compose files
and runnable examples live in the generated bundle or in `spx-examples`.

## Verify the server

Set your product key for local scripts:

macOS/Linux:

```bash
export SPX_PRODUCT_KEY="YOUR_REAL_KEY"
export SPX_BASE_URL="${SPX_BASE_URL:-http://localhost:8000}"
```

Windows PowerShell:

```powershell
$env:SPX_PRODUCT_KEY = "YOUR_REAL_KEY"
$env:SPX_BASE_URL = "http://localhost:8000"
```

Check health:

```bash
curl -fsS http://localhost:8000/health
```

Expected response includes:

```json
{"status":"ok","server_version":"<version>","api_version":"v3"}
```

Install the Python client and YAML dependency in your local virtual environment:

```bash
pip install spx-python pyyaml
```

Quick client smoke test:

```python
import os
import spx_python

client = spx_python.init(
    address=os.environ.get("SPX_BASE_URL", "http://localhost:8000"),
    product_key=os.environ["SPX_PRODUCT_KEY"],
)

print(client.keys())  # e.g. ['models', 'instances', 'timer', 'polling']
```

## Your first simulation: PT100-style temperature sensor

The minimal simulation below registers a PT100-like temperature sensor model,
creates one instance, advances deterministic time, and reads internal vs
external temperature values.

This is the documentation-sized version of the runnable
`spx-examples/examples/core/first_simulation.py` example.

```python
import os
import spx_python
import yaml

client = spx_python.init(
    address=os.environ.get("SPX_BASE_URL", "http://localhost:8000"),
    product_key=os.environ["SPX_PRODUCT_KEY"],
)

pt_100_yaml = """
attributes:
  temperature: 0.0
actions:
  - { ramp: $in(temperature), stop_value: 150, duration: 5, type: overshoot, overshoot: 5 }
  - { noise: $out(temperature), std: 0.01, mode: proportional }
"""

model_def = yaml.safe_load(pt_100_yaml)
client["models"]["pt_100"] = model_def

client["instances"]["pt100_1"] = "pt_100"
inst = client["instances"]["pt100_1"]
temperature = inst["attributes"]["temperature"]
timer = inst["timer"]

client.prepare()
for step in range(1, 101):
    t = step * 0.1
    timer.time = t
    client.run()

print("internal temperature:", temperature.internal_value)
print("external temperature:", temperature.external_value)
```

The internal value is the deterministic simulation state. The external value is
the value exposed after the `noise` action, which is useful for testing logic
that must tolerate measurement variation.

## Run the full example from spx-examples

For plotting and a longer console trace, run the canonical example from
`spx-examples`:

```bash
cd /path/to/spx-examples
export SPX_PRODUCT_KEY="YOUR_REAL_KEY"
docker compose up --detach
python examples/core/first_simulation.py
```

The script writes an interactive Plotly chart to
`examples/core/first_simulation.html`.

## Try protocol examples next

Once the server is running, use the installer packs for protocol services:

- Smart Building Pack for MQTT, BACnet, KNX, OPC UA, Matter, Home Assistant, and
  Modbus examples.
- Embedded Lab Pack with `scpi_lab` for SCPI/ASCII instruments and Modbus lab
  devices.
- Industrial IIoT Pack with `process_cell_quickstart` or
  `modbus_master_plc_demo` for factory/process examples.

See [Installer and packs](installer-and-packs.md) and
[Industry packs and profiles](../usage-scenarios-and-examples/industry-packs.md).
