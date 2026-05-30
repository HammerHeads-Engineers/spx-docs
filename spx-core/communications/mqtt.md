# MQTT adapter

SPX Server ships two MQTT components:

- `mqtt` — single-broker MQTT client using bindings
- `mqtt-ha` — multi-broker MQTT with optional availability + Home Assistant discovery fan-out

## `mqtt` (single broker)

**YAML key:** `mqtt`

Example model (spx-examples):
[`library/domains/iot/generic/environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__mqtt.yaml)

```yaml
communication:
  - mqtt:
      broker: host.docker.internal
      port: 1883
      topic_prefix: spx/examples/env
      publish_interval: 0.5
      publish_jitter: 0.0
      response_delay: 0.0
      default_qos: 1
      default_retain: false
      payload_codec: text
      bindings:
        - name: temperature
          attribute: $ext(temperature_c)
          topic: telemetry/temperature_c
          direction: publish

        - name: setpoint
          attribute: $attr(target_c)
          topic: command/setpoint_c
          direction: subscribe
```

### Top-level fields

- `broker` (required): broker host name / IP (alias: `host`)
- `port` (default: `1883`)
- `keepalive` (default: `60`)
- `connect_timeout` (default: `10.0`)
- `topic_prefix` (default: empty) — prepended to every binding `topic`
- `default_qos` (default: `1`) — `0|1|2`
- `default_retain` (default: `true`)
- `publish_interval` / `publish_jitter` (seconds; defaults: `0.5` / `0.0`)
- `response_delay` (seconds; default: `0.0`) — artificial delay before publishing
- `payload_codec` (default: `text`) — `text|json|raw`
- Credentials (optional):
  - `username` / `password`
  - `credentials_file` (`.yaml`/`.yml`/`.json` with `username`/`password`)
  - `env_username_var` / `env_password_var`

### Bindings

Each entry under `bindings` maps a topic to an attribute reference:

- `topic` (required)
- `direction`: `publish|subscribe|both` (aliases map to outbound/inbound/bidirectional)
- `attribute` (shorthand) or `attributes` / `read_attribute` / `write_attribute`
- Optional per-binding overrides: `qos`, `retain`, `payload_codec`, `publish_interval`, `publish_jitter`, `response_delay`

Legacy config is still accepted and converted to bindings:

- `publishers:` + `subscribers:` → `bindings:`

### Scenarios

Use `detach` / `attach` to simulate broker disconnects:

```yaml
scenarios:
  mqtt_disconnect:
    duration: 4.0
    call:
      path: communication.mqtt.detach
      stop_path: communication.mqtt.attach
```

## `mqtt-ha` (multi broker + availability + discovery)

**YAML key:** `mqtt-ha`

Minimal example:

```yaml
communication:
  - mqtt-ha:
      brokers:
        - host: broker-a.local
          port: 1883
          client_id: spx-a
        - host: broker-b.local
          port: 1883
      availability:
        topic: ha/device/status
        online: ready
        offline: lost
        retain: true
        qos: 1
      discovery:
        prefix: homeassistant
        device_id: spx-device-1
        entities:
          - component: sensor
            object_id: temperature
            state_binding: temp_pub
            payload:
              unit_of_measurement: "°C"
      bindings:
        - name: temp_pub
          attribute: "#attr(sensor.temperature)"
          topic: telemetry/temp
          direction: publish
```

## Next steps on simplephysx.com

Explore the MQTT simulator workflow:

- [MQTT Simulator](https://www.simplephysx.com/mqtt-simulator)
