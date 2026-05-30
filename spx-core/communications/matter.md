# Matter adapter

**YAML key:** `matter`

Map SPX attributes to Matter cluster attributes/commands via a `python-matter-server` controller (WebSocket).

## Minimal configuration

Example model (spx-examples):
[`library/domains/building/thermostat/generic/thermostat__matter.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/building/thermostat/generic/thermostat__matter.yaml)

```yaml
communication:
  - matter:
      controller:
        ws_url: "ws://matter-server:5580/ws"
        connect_timeout: 10.0
        poll_interval: 2.0
        only_on_change: true
      default_payload_codec: json
      bindings:
        - name: temperature_report
          direction: outbound
          node_id: "0x1234"
          endpoint: 1
          cluster: TemperatureMeasurement
          attribute: MeasuredValue
          read_attribute: "#attr(measured_value_raw)"
        - name: heating_setpoint
          direction: bidirectional
          node_id: "0x1234"
          endpoint: 1
          cluster: Thermostat
          attribute: OccupiedHeatingSetpoint
          read_attribute: "#attr(heating_setpoint_raw)"
          write_attribute: "#attr(room_command_raw)"
```

## Notes

- Dependency: requires `python-matter-server` (and its `chip` dependencies) in the SPX Server environment.
- `node_id` accepts integers or hex strings (`0x...`).
