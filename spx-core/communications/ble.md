# BLE Adapter

The BLE adapter bridges SPX simulations with the standalone [`spx-ble-adapter`](https://github.com/HammerHeads-Engineers/spx-ble-adapter). It pushes your GATT layout and live attribute values over HTTP, exposing the simulation as a Bluetooth Low Energy peripheral that mobile apps can pair with.

## Run the companion service

The protocol talks to an external process, so start the adapter next to your SPX server:

```bash
git clone https://github.com/HammerHeads-Engineers/spx-ble-adapter.git
cd spx-ble-adapter
npm install         # first time
npm start           # sudo npm start on macOS when CoreBluetooth requires it
```

Defaults:

- HTTP listener: `http://127.0.0.1:8085`
- Advertised device name: `SPX-Sim`
- Health endpoint: `GET /health`

Point `adapter.baseUrl` at a reachable address (use `http://host.docker.internal:8085` when SPX runs inside Docker and the adapter runs on the host).

## Configuration example

{% tabs %}
{% tab title="YAML" %}
```yaml
attributes:
  temperature: 22.5
  setpoint: 24.0

communication:
  - ble:
      adapter:
        baseUrl: http://host.docker.internal:8085
        timeout: 3.0
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
          tolerance: 0.05
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
{% endtab %}

{% tab title="JSON" %}
```json
{
  "attributes": {
    "temperature": 22.5,
    "setpoint": 24.0
  },
  "communication": [
    {
          "ble": {
            "adapter": {
              "baseUrl": "http://host.docker.internal:8085",
              "timeout": 3.0,
              "polling": {
                "enabled": true,
            "interval": 1.0
          }
        },
        "device": {
          "name": "SpX Temperature Sensor"
        },
        "codecs": {
          "celsius": {
            "format": "utf8"
          }
        },
        "bindings": {
          "temperature": {
            "attribute": "$out(temperature)",
            "codecRef": "celsius",
            "tolerance": 0.05
          },
          "setpoint": {
            "attribute": "$in(setpoint)",
            "stateKey": "setpointC",
            "codecRef": "celsius"
          }
        },
        "services": [
          {
            "uuid": "181a",
            "name": "Environmental Sensing",
            "characteristics": [
              {
                "uuid": "2a6e",
                "name": "Temperature",
                "binding": "temperature",
                "properties": [
                  "read",
                  "notify"
                ],
                "notify": {
                  "triggers": [
                    "state"
                  ]
                }
              },
              {
                "uuid": "f0c09111-8b3a-4e69-bdd0-9f0f613d1a90",
                "name": "Setpoint",
                "binding": "setpoint",
                "properties": [
                  "read",
                  "write",
                  "notify"
                ],
                "onWrite": [
                  {
                    "action": "parse",
                    "type": "float",
                    "target": "state",
                    "key": "setpointC"
                  },
                  {
                    "action": "log",
                    "template": "[BLE] Setpoint -> {{value}}"
                  }
                ]
              }
            ]
          }
        ]
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}

## Key sections

- `adapter`: HTTP connection settings for the companion service and polling behaviour.
- `device`: advertised metadata (name, service UUIDs, manufacturer data).
- `codecs`: reusable encoders/decoders applied to characteristic values.
- `bindings`: maps between SPX attributes and adapter state keys.
- `services`: GATT services/characteristics exposed through the adapter.

### Adapter settings reference

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `adapter.baseUrl` | string | `http://127.0.0.1:8085` | Root for `/health`, `/config`, `/state`, `/events`. For Dockerised SPX use `http://host.docker.internal:8085`. |
| `adapter.timeout` | number | `2.0` seconds | Per-request timeout. Increase if the adapter runs remotely or handles large configs. |
| `adapter.polling.enabled` | boolean | `true` | Disable when BLE clients never write back (pure outbound telemetry). |
| `adapter.polling.interval` | number | `1.0` second | Delay between `GET /state` polls. Smaller values tighten feedback at the expense of HTTP load. |
| `adapter.polling.jitter` | number | `0.0` | Accepted for forward compatibility; reserved for staggered polling. |

The companion binary accepts `BLE_DEVICE_CONFIG=/path/to/config.json` to preload a profile. Once SPX calls `prepare()`, the pushed configuration replaces the runtime copy.

The `device` block mirrors directly into the adapter. Common fields include:

- `name`: advertised peripheral name (defaults to the SPX component name).
- `advertiseServiceUuids`: array of UUIDs to include in advertisements; omit to auto-derive.
- `manufacturerData`: raw bytes (array or Base64 string) inserted into advertising packets.
- `intervalMs`: advertising interval hint for the adapter (forwarded to bleno when supported).

### Bindings, direction, and codecs

- **Attribute references:** `$out(attr)` streams external values, `$in(attr)` applies inbound writes, `#attr(component.path)` reaches nested attributes explicitly.
- **Direction:** `outbound`, `inbound`, or `bidirectional` (default). Outbound bindings participate in `PUT /state`; inbound bindings consume data from `GET /state`.
- **stateKey:** optional override for the adapter-side key (defaults to the binding name).
- **Tolerance:** numeric guard band that suppresses small changes to reduce notification spam.
- **Codecs:** reuse a named codec (`codecRef`) or embed an inline definition. Supported formats in the adapter today include `utf8`, `sint16` (with `scale`), and `float`.

Snippet from `library/domains/ble/generic/vital_signs_monitor__ble_gatt.yaml`:

```yaml
bindings:
  heart_rate:
    attribute: $out(attributes.heartRateBpm)
    codecRef: heartRate
    tolerance: 1.0
  activity_intensity:
    attribute: $in(attributes.activityIntensity)
    codecRef: intensity
    direction: inbound
    stateKey: activityIntensity
```

### Defining services and characteristics

- **UUIDs:** accept 16-bit aliases (`"181a"`) or 128-bit UUIDs. Lowercase hex keeps output predictable. 16-bit values expand to the Bluetooth Base UUID (`0000xxxx-0000-1000-8000-00805f9b34fb`). If `device.advertiseServiceUuids` is omitted, the protocol derives it from your service list.
- **Properties:** pass through to bleno (`read`, `write`, `writeWithoutResponse`, `notify`, `indicate`) and wire the corresponding handlers automatically.
- **Value mapping:** when `binding` is present the protocol injects `{"source": "state", "key": stateKey}`. Provide explicit `value` blocks for literals or constant data.
- **Notify triggers:** defaults to `["state"]`. Add `"timer"` with `intervalMs` for periodic notifications even when the value does not change.
- **Descriptors:** support `0x2901` (Characteristic User Description) and `0x2904` (Characteristic Presentation Format) as structured objects. Raw buffers, arrays, numbers, and strings are also accepted.

Excerpt from the vital-signs service:

```yaml
services:
  - uuid: "f0c0a100-8b3a-4e69-bdd0-9f0f613d1a90"
    name: Vital Signs Service
    characteristics:
      - uuid: "f0c0a101-8b3a-4e69-bdd0-9f0f613d1a90"
        name: Body Temperature
        binding: body_temperature
        properties: [read, notify]
        codecRef: celsius
        descriptors:
          - uuid: "2901"
            value: "Body Temperature (°C)"
      - uuid: "f0c0a108-8b3a-4e69-bdd0-9f0f613d1a91"
        name: Activity Intensity
        binding: activity_intensity
        properties: [read, write, notify]
        codecRef: intensity
        notify:
          triggers: [state]
        onWrite:
          - action: parse
            type: float
            target: state
            key: activityIntensity
          - action: log
            template: "[BLE] Activity Intensity -> {{value}}"
```

### OnWrite actions

Actions execute sequentially when a BLE client writes:

- `parse`: convert the incoming payload to `float` or `int`, optionally clamp ranges (`clamp.min` / `clamp.max`), and write to adapter state (`target: state`, `key: ...`) or back into the action context.
- `log`: template-driven logging with placeholders such as `{{deviceName}}`, `{{uuid}}`, `{{value}}`, or `{{state}}` (JSON snapshot).

Compose actions to validate, clamp, and audit incoming data. If any step raises, the adapter reports a GATT write failure to the client.

## Lifecycle

When the simulation `prepare`s:

1. The protocol checks adapter health (`GET /health`).
2. Builds the combined payload (device metadata, initial state, services) and sends `PUT /config`.
3. Pushes current binding values with `PUT /state`.

During `run` (or while the worker thread is active after `start`):

- Outbound bindings push updates whenever values change beyond the configured `tolerance`.
- Inbound bindings (when polling enabled) are updated from `GET /state`.
- Adapter writes trigger `onWrite` workflows which can emit events back to SPX via polling.

Use model `scenarios` to detach or fault the protocol (e.g., override `communication.<name>.adapter.baseUrl` to an invalid host) and observe how clients react.

## Reference models

- `spx-examples/library/domains/ble/generic/temperature_sensor__ble_gatt.yaml`: minimal read/write sensor.
- `spx-examples/library/domains/ble/generic/vital_signs_monitor__ble_gatt.yaml`: multi-characteristic wearable with scenarios that drive activity profiles.

Import these into your models or use them as templates when defining new GATT services.

## Testing tips

- Pair with BLE inspectors (nRF Connect, LightBlue) to verify services and notifications while the simulation runs.
- Script mobile app flows against the adapter before hardware is available; you control both directions from SPX.
- Keep adapter logs enabled; they show inbound writes and state payloads, which helps tune codecs and tolerances.
