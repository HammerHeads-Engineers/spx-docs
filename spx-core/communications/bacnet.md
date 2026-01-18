# BACnet/IP adapter

**YAML key:** `bacnet`

Expose BACnet/IP objects backed by SPX attributes (read/write mappings live under `objects.*.properties`).

## Minimal configuration

```yaml
attributes:
  room_temperature: 22.0
  fan_enable: 0

communication:
  - bacnet:
      host: 0.0.0.0
      port: 47808
      device:
        instance_id: 2001
        vendor_id: 999
        name: "SPX BACnet Simulator"
      objects:
        room_temp:
          type: analogInput
          instance: 2
          properties:
            presentValue:
              read: "#attr(room_temperature)"
            units: degreesCelsius
        fan_command:
          type: binaryOutput
          instance: 10
          priority: 8
          properties:
            presentValue:
              read: "#attr(fan_enable)"
              write: "#attr(fan_enable)"
              states:
                0: inactive
                1: active
            relinquishDefault: 0
```

## Notes

- Dependency: requires `bacpypes3` in the SPX Server environment.
- The full schema supports additional BACnet features (device metadata, schedules, alarms). See spx-examples for richer models.

## References

- Example models (spx-examples):
  - [`hvac_flexit_nordic__bacnet.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/hvac_flexit_nordic__bacnet.yaml)
  - [`fire_alarm_panel__bacnet.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/fire_alarm_panel__bacnet.yaml)
