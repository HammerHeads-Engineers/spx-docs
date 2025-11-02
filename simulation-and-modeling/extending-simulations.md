# Extending Simulations (Writing Custom Components)

This page explains **why** and **how** to extend SPX simulations by writing custom components. Extensions let you model device physics, bridge to real hardware or protocols, inject faults, and encapsulate reusable domain logic. Once registered, your component behaves like any built‑in block and can be used from YAML, controlled deterministically via the same client libraries (e.g., `spx-python`).

> **Deterministic control remains the same.** Time progression and attribute updates are still driven from the client (e.g., setting `instance["timer"]["time"]` and calling `client.run()`), so your extensions integrate seamlessly into Model‑in‑the‑Loop workflows.

---

## When to Extend vs. Use Built‑ins
Use **built‑ins** (attributes, actions, conditions, hooks) when:
- Your behavior is a straightforward expression or a set/value action.
- You can model logic directly in YAML with `function`/`set` actions and simple wiring.

Create a **custom component** when you need:
- Non‑trivial **stateful** behavior (buffers, integrators, hybrid logic).
- **Integration** with external systems (hardware drivers, protocol stacks).
- **Performance** or specialized math that is awkward in YAML.
- **Reusable** domain logic shared across multiple models.
- Precise **I/O mapping** or lifecycle control (`start/stop/destroy`).

---

## Component Anatomy
A custom component is a Python class registered in the SPX registry and loaded at runtime.

- **Registration**: decorate with `@register_class(name="...")` so YAML can instantiate it by name.
- **Populate**: `_populate(definition)` — read parameters from the YAML definition, set defaults, allocate internal structures.
- **Prepare**: `prepare()` — initialize/reset internal state; must be **idempotent**.
- **Run**: `run()` — execute one simulation step; read inputs, update internal state, write outputs.
- **Lifecycle** (optional): `start()`, `stop()`, `destroy()` for long‑running resources.
- **Attributes**: read/write via `internal_value` (for internal math) and `external_value` (for exposed outputs).

### Internal vs. External values
- `internal_value` is the value used by the **simulation logic** and calculations — the “true” state.
- `external_value` is what you **expose outward** (e.g., protocol layer); it may include noise, scaling, or other transformations **without affecting the internal state** unless you explicitly choose to.

**One‑way update rule:**
```
internal_value  →  external_value   ✅ (auto‑propagates when external is not overridden)
external_value  →  internal_value   ❌ (does not propagate back)
```
This separation lets you add output effects (noise/faults) safely, while keeping the core simulation stable and controllable.

---

## Minimal Example (Plugin): Moving Average Filter
**File:** `examples/plugins/moving_average.py`
```python
# All comments in English only.
from collections import deque
from typing import Optional

from spx_sdk.registry import register_class
from spx_sdk.components import SpxComponent


@register_class(name="moving_average")
class MovingAverage(SpxComponent):
    """Simple moving-average filter component.
    Config in YAML under this node:
      - source_attr: parent attribute name to read (e.g., "raw_signal")
      - target_attr: parent attribute name to write (e.g., "filtered_signal")
      - attributes.window: window size (int), default 5
    """

    def _populate(self, definition):
        super()._populate(definition)
        d = definition or {}
        self.source_attr = d.get("source_attr", "input")
        self.target_attr = d.get("target_attr", "output")
        self._buf: Optional[deque] = None

    def prepare(self, *args, **kwargs) -> bool:
        super().prepare(*args, **kwargs)
        attrs = self.get("attributes", None)
        window = 5
        if attrs and "window" in attrs.children:
            window = int(attrs.internal.get("window", 5))
        self._buf = deque(maxlen=window)
        return True

    def run(self, *args, **kwargs) -> bool:
        super().run(*args, **kwargs)
        if self.parent is None:
            return True

        p_attrs = self.parent.get("attributes", None)
        if p_attrs is None:
            return True

        # Read input as an *external* value; internal math stays isolated
        sample = p_attrs.external.get(self.source_attr, None)
        if sample is None:
            return True

        self._buf.append(float(sample))
        avg = sum(self._buf) / len(self._buf)

        # Write to parent's *external* for presentation; internal state stays in the buffer
        p_attrs.external[self.target_attr] = avg
        return True
```

---

## Using the Component in YAML
{% tabs %}
{% tab title="YAML" %}
```yaml
# examples/models/mavg_demo.yaml
attributes:
  raw_signal:
    type: float
    default: 0.0
  filtered_signal:
    type: float
    default: 0.0

# Create a simple signal as an example
actions:
  - function: $ext(raw_signal)
    call: "sin($(.timer.time)) + 0.2 * sin(10 * $(.timer.time))"

# Our plugin: reads raw_signal and writes filtered_signal
moving_average:
  source_attr: raw_signal
  target_attr: filtered_signal
  attributes:
    window:
      type: int
      default: 8

timer:
  dt: 0.05

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "attributes": {
    "raw_signal": {
      "type": "float",
      "default": 0.0
    },
    "filtered_signal": {
      "type": "float",
      "default": 0.0
    }
  },
  "actions": [
    {
      "function": "$ext(raw_signal)",
      "call": "sin($(.timer.time)) + 0.2 * sin(10 * $(.timer.time))"
    }
  ],
  "moving_average": {
    "source_attr": "raw_signal",
    "target_attr": "filtered_signal",
    "attributes": {
      "window": {
        "type": "int",
        "default": 8
      }
    }
  },
  "timer": {
    "dt": 0.05
  }
}

```
{% endtab %}
{% endtabs %}

> After importing the module `examples.plugins.moving_average`, the class is registered under the name `moving_average`, so the YAML node works immediately.

---

## Running and Testing via spx-python
```python
# All comments in English only.
import os, yaml
import spx_python

# 1) Connect to the server
client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ.get("SPX_PRODUCT_KEY", ""),
)

# 2) Ensure plugin is imported on the server (hot-reload or preload)
#    For example, call the admin reload endpoint from your tooling if needed.

# 3) Load model definition and create an instance
with open("examples/models/mavg_demo.yaml", "r", encoding="utf-8") as f:
    model_def = yaml.safe_load(f)

client["models"]["MavgDemo"] = model_def
client["instances"]["demo"] = "MavgDemo"
inst = client["instances"]["demo"]

# 4) Prepare and step deterministically
client.prepare()
for k in range(1, 51):
    t = k * inst["timer"].get("dt", 0.05)
    inst["timer"]["time"] = t
    client.run()

print("filtered:", inst["attributes"]["filtered_signal"].external_value)
```

---

## Hot‑Reloading the Extension
If your server exposes an admin endpoint (e.g., `system.reload`), you can reload plugins at runtime:
```python
# All comments in English only.
import requests

address = "http://localhost:8000"
resp = requests.post(f"{address}/system/reload")
resp.raise_for_status()
```
After reload, any modules that register classes with `@register_class(...)` become available to models without restarting the server.

---

## Best Practices
- Keep simulation math on `internal_value`; present noisy/transformed outputs via `external_value`.
- Make your time step explicit with `timer.dt`; never rely on real sleeps inside `run()`.
- Keep `_populate` tolerant of missing fields; keep `prepare()` **idempotent**; make `run()` side‑effects intentional and minimal.
- Expose tunables (gains, window sizes, flags) as attributes so they can be changed from the client.
- Add light logging only where it helps diagnose scenarios; avoid noisy logs in tight `run()` loops.

---

## Troubleshooting
- **My plugin name is not recognized in YAML** → Ensure the module is imported and the class is decorated with `@register_class(name="...")`. Use the server’s reload endpoint if needed.
- **Outputs don’t change** → Verify that `run()` reads the correct source attribute and that you advance `timer.time` before calling `client.run()`.
- **Noise feeds back into logic** → Write noise to `external_value`; keep `internal_value` for core logic. Remember the one‑way update rule.

## Simulating Bluetooth Low Energy Devices
SPX now provides a `ble` communication protocol that synchronizes model attributes with the standalone [`spx-ble-adapter`](../spx-ble-adapter/README.md). The adapter exposes your simulation as a live GATT peripheral, so you can pair real mobile apps or BLE test clients with your virtual hardware before silicon exists.

### Prerequisites
- Run the adapter next to SPX (Node.js 16+, Bluetooth enabled on the host). On macOS you may need elevated rights for CoreBluetooth.
- Default HTTP endpoint is `http://127.0.0.1:8080`. Use `http://host.docker.internal:8080` when SPX runs inside Docker but the adapter runs on the host.

```bash
cd ../spx-ble-adapter
npm install         # once
npm start           # or: sudo npm start on macOS
```

### Define the BLE communication block
Add a `ble` item under `communication` to push attributes into adapter state and describe the GATT surface. The definition below mirrors `spx-examples/library/ble/generic/ble_temperature_sensor.yaml`.

```yaml
attributes:
  temperature: 22.5
  setpoint: 24.0

communication:
  - ble:
      adapter:
        baseUrl: http://host.docker.internal:8080
        polling:
          enabled: true
          interval: 1.0      # seconds between GET /state for inbound updates
      device:
        name: SpX Temperature Sensor
      codecs:
        celsius:
          format: utf8
      bindings:
        temperature:
          attribute: $out(temperature)
          codecRef: celsius
        setpoint:
          attribute: $in(setpoint)
          stateKey: setpointC
          codecRef: celsius
      services:
        - uuid: "181a"
          name: Environmental Sensing
          characteristics:
            - uuid: "2a6e"
              name: Temperature
              binding: temperature
              properties: [read, notify]
              notify:
                triggers: [state]
            - uuid: "f0c09111-8b3a-4e69-bdd0-9f0f613d1a90"
              name: Setpoint
              binding: setpoint
              properties: [read, write, notify]
              onWrite:
                - action: parse
                  type: float
                  target: state
                  key: setpointC
                - action: log
                  template: "[BLE] Setpoint -> {{value}}"
```

- `adapter`: connection details plus optional `polling` settings. Disable polling when the flow is outbound-only.
- `bindings`: map SPX attributes to BLE state keys. Direction defaults to bidirectional; set `direction: outbound` or `direction: inbound` to narrow the flow. Inline codecs or reference entries under `codecs` to convert values.
- `services`: copies directly to the adapter GATT profile. Bindings inject live values, and `onWrite` actions execute on the adapter whenever a client writes.

### Reuse and extend the library templates
- `spx-examples/library/ble/generic/ble_temperature_sensor.yaml` offers a minimal read/write sensor that pairs with the adapter defaults.
- `spx-examples/library/ble/generic/ble_vital_signs_monitor.yaml` layers richer physiology, multiple codecs, and attribute-driven scenarios (`scenarios.*`) to stress mobile dashboards.

Import these fragments into your own models or use them as references for custom UUIDs, codec definitions, and event handling.

### Testing tips
- After `client.prepare()` the `ble` protocol pushes the GATT definition and initial state via `PUT /config` and `PUT /state`.
- Use a BLE explorer (nRF Connect, LightBlue, etc.) to confirm services and receive `notify` updates as your simulation runs.
- Writes from the client propagate through the adapter back into SPX attributes (e.g., the setpoint above), letting you validate app-to-device flows end to end.

For a step-by-step tutorial that builds the peripheral from scratch, see [BLE Device Simulation Walkthrough](extending-simulations/ble-device-simulation.md).

---
