# MQTT Adapter

The MQTT adapter publishes telemetry and consumes commands via MQTT topics. It runs an asyncio client inside the core and integrates with diagnostics for connection monitoring.

## YAML structure

{% tabs %}
{% tab title="YAML" %}
```yaml
communication:
  mqtt:
    broker: mqtt://localhost:1883
    client_id: spx-sim
    topics:
      publish:
        - topic: spx/sim/temperature
          payload: "#out(attributes.temperature)"
          qos: 1
          retain: false
          period: 1.0
      subscribe:
        - topic: spx/sim/setpoint
          qos: 1
          handler:
            path: system.controllers.pid.update_setpoint
```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "communication": {
    "mqtt": {
      "broker": "mqtt://localhost:1883",
      "client_id": "spx-sim",
      "topics": {
        "publish": [
          {
            "topic": "spx/sim/temperature",
            "payload": "#out(attributes.temperature)",
            "qos": 1,
            "retain": false,
            "period": 1.0
          }
        ],
        "subscribe": [
          {
            "topic": "spx/sim/setpoint",
            "qos": 1,
            "handler": {
              "path": "system.controllers.pid.update_setpoint"
            }
          }
        ]
      }
    }
  }
}
```
{% endtab %}
{% endtabs %}

### Key fields

- `broker`: URI (`mqtt://host:port` or `mqtts://` for TLS).
- `client_id`: identifier; default random.
- `username` / `password`: credentials (optional).
- `topics.publish`: periodic publications.
  - `payload`: expression resolved each time (stringified JSON supported).
  - `period`: seconds between publishes; omit for publish-on-change.
- `topics.subscribe`: inbound topics.
  - `handler.path`: component method to call with message payload.
  - `qos`: MQTT QoS level.

### Payload formats

- Strings are sent as-is.
- For JSON, use the YAML multiline literal and ensure clients parse it accordingly.

```yaml
payload: |
  {
    "voltage": #out(attributes.voltage),
    "current": #out(attributes.current)
  }
```

```json
{
  "payload": "{\n  \"voltage\": #out(attributes.voltage),\n  \"current\": #out(attributes.current)\n}"
}
```

### Scenarios

{% tabs %}
{% tab title="YAML" %}
```yaml
scenarios:
  mqtt_disconnect:
    duration: 4.0
    call:
      path: communication.mqtt.disconnect
      stop_path: communication.mqtt.connect
  mqtt_latency:
    duration: 6.0
    overrides:
      communication.mqtt.publish_delay: 2.0
```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "scenarios": {
    "mqtt_disconnect": {
      "duration": 4.0,
      "call": {
        "path": "communication.mqtt.disconnect",
        "stop_path": "communication.mqtt.connect"
      }
    },
    "mqtt_latency": {
      "duration": 6.0,
      "overrides": {
        "communication.mqtt.publish_delay": 2.0
      }
    }
  }
}
```
{% endtab %}
{% endtabs %}

### Tips

- Use persistent sessions only when you need message replay after reconnect.
- Monitor diagnostics logs for connection loss or publish errors.
- Combine with actions to throttle telemetry based on system state (e.g., publish only when values change significantly).
