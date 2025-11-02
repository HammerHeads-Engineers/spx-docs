# BLE Device Simulation Walkthrough

This guide builds on SPX custom components to expose a virtual device as a Bluetooth Low Energy (BLE) peripheral. You will wire a model to the `ble` communication protocol, drive a companion `spx-ble-adapter` process, and verify the interaction using a mobile BLE explorer. The walkthrough starts from the temperature sensor template and then expands toward the richer vital-signs demo.

---

## Scenario overview

**Goal:** deliver a software-only twin of a BLE sensor so mobile apps and test rigs can iterate before physical hardware exists.

**Key pieces:**

- SPX simulation with controllable attributes (`temperature`, `setpoint`, etc.).
- `ble` protocol inside `spx_core`, which keeps SPX attributes in sync with the adapter state.
- Standalone [`spx-ble-adapter`](../../spx-ble-adapter/README.md) process that speaks CoreBluetooth (macOS) or BlueZ (Linux) to expose a GATT peripheral.
- BLE client (nRF Connect, LightBlue, custom QA app) that connects and exercises the device.

---

## Prerequisites

- Node.js 16+ with build tools (the adapter depends on `@abandonware/bleno`).
- Bluetooth enabled on the host. On macOS grant Terminal (or your shell) Bluetooth permissions; some systems require `sudo`.
- SPX server running locally or via Docker. If SPX is inside Docker, ensure it can reach the adapter with `http://host.docker.internal:8080`.
- `spx-python` or REST tooling to load the model.
- A BLE inspection app on a phone/tablet (nRF Connect, LightBlue, or similar).

---

## 1. Start from a minimal model

Copy or import the library template `spx-examples/library/ble/generic/ble_temperature_sensor.yaml`. The relevant pieces:

```yaml
attributes:
  temperature: 22.5
  setpoint: 24.0

actions:
  - function: $out(temperature)
    call: "22.0 + 0.2 * sin($(.timer.time))"

timer:
  dt: 0.5
```

The action generates a slow waveform for `temperature`. `setpoint` stays writable so you can push new targets from a connected client.

---

## 2. Attach the BLE communication block

Append the `ble` adapter definition under `communication` (excerpted from the template):

```yaml
communication:
  - ble:
      adapter:
        baseUrl: http://host.docker.internal:8080   # use http://127.0.0.1:8080 if everything runs on the same host
        polling:
          enabled: true
          interval: 1.0
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

Bindings determine how SPX attributes map to the adapter state:

- `temperature` flows outbound (`$out`) and pushes notifications.
- `setpoint` flows inbound (`$in`). Any write from a BLE client is parsed to float and stored in the adapter, which the protocol reads back and applies to the attribute.

---

## 3. Launch the companion adapter

Run the adapter in a separate shell:

```bash
cd ../spx-ble-adapter
npm install          # first time
npm start            # add sudo on macOS if CoreBluetooth requires it
```

Watch the logs. You should see the adapter listening on port `8080` and waiting to load a configuration.

---

## 4. Load and run the simulation

With SPX server running, use `spx-python` to register the model and create an instance:

```python
import os, yaml
import spx_python

client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ.get("SPX_PRODUCT_KEY", ""),
)

with open("library/ble/generic/ble_temperature_sensor.yaml", "r", encoding="utf-8") as f:
    model_def = yaml.safe_load(f)

client["models"]["BleTemp"] = model_def
client["instances"]["ble-temp"] = "BleTemp"
inst = client["instances"]["ble-temp"]

client.prepare()

# Advance the timer to produce data and trigger notifications.
for step in range(1, 31):
    inst["timer"]["time"] = step * inst["timer"].get("dt", 0.5)
    client.run()
```

During `prepare()` the `ble` protocol will:

1. `GET /health` on the adapter.
2. Push the GATT layout and initial state via `PUT /config`.
3. Sync current attribute values with `PUT /state`.

Subsequent `run()` calls maintain the link by pushing outbound changes and polling inbound state.

---

## 5. Pair and validate from a BLE client

1. Open your BLE explorer app.
2. Scan for peripherals; the adapter advertises as `SpX Temperature Sensor` (or override via `device.name`).
3. Connect and browse the Environmental Sensing service (`0x181A`).
4. Enable notifications on `0x2A6E` (Temperature) and watch values update as the simulation runs.
5. Write a UTF-8 value (e.g., `"25.5"`) to the custom setpoint characteristic (`f0c09111-8b3a-4e69-bdd0-9f0f613d1a90`). The adapter logs the parsed value, and the SPX attribute `setpoint` updates on the next poll cycle.

If you run inside Docker, use port forwarding or `host.docker.internal` so the adapter can reach the SPX server.

---

## 6. Handling inbound control with scenarios

Use `scenarios` to script BLE-side events. Example:

```yaml
scenarios:
  mobile_override:
    enabled: true
    duration: 15.0
    overrides:
      $in(setpoint): 28.0
```

Triggering `mobile_override` mimics a mobile app write without real hardware. This is helpful for regression tests or CI smoke checks.

---

## 7. Expanding to multi-sensor wearables

The vital-signs template (`library/ble/generic/ble_vital_signs_monitor.yaml`) demonstrates a fuller device:

- Multiple attributes (`heartRateBpm`, `bloodOxygenPercent`, `batteryLevelPercent`, etc.) driven by custom actions that model physiology.
- Rich codec definitions (`percentage`, `bloodPressure`, `intensity`) so each characteristic formats data appropriately.
- Descriptors (`0x2901`) with user-friendly strings and `notify` triggers that push updates on every state change.
- Writable characteristics (activity intensity) that feed back into the simulation via `onWrite` parsing and logging.

Study the bindings section to see how each attribute ties to a reusable codec. Use this as a blueprint when adding new services or custom UUIDs.

---

## 8. Troubleshooting

- **Adapter logs `health check failed`:** confirm `adapter.baseUrl` is reachable from SPX and that `npm start` is running. For Docker, expose port `8080` and use `http://host.docker.internal:8080`.
- **Mobile app cannot see the peripheral:** verify Bluetooth permissions, ensure no previous instance is still advertising, and check for OS-level restrictions when running under `sudo`.
- **Writes do not change SPX attributes:** make sure the binding uses `$in(...)` or a bidirectional reference, and that polling is enabled (`polling.enabled: true`).
- **Notifications stop after a few minutes:** the adapter stops when the subscriber disconnects. Confirm the mobile client keeps the connection alive and the simulation continues to call `client.run()`.

---

## Next steps

- Layer custom descriptors (`0x2904`) to declare units and formats for advanced clients.
- Forward adapter `POST /events` into your telemetry pipeline for audit trails.
- Combine BLE communication with other protocols (HTTP, MQTT) in the same model to test cross-channel coordination.
