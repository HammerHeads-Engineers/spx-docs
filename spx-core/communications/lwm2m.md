# LwM2M client adapter

**YAML key:** `lwm2m`

Simulated LwM2M device that registers against an LwM2M server and exposes resources via CoAP.

## Minimal configuration

```yaml
attributes:
  temperature: 24.2
  setpoint: 20.0

communication:
  - lwm2m:
      host: 0.0.0.0
      # Local bind port for the client (pick a free UDP port if your LwM2M server runs on localhost:5683).
      port: 56830
      server:
        host: 127.0.0.1
        # Remote LwM2M server (for example: Leshan).
        port: 5683
        endpoint: spx-demo-001
        lifetime: 60
        update_margin: 30
      bindings:
        - name: temp_sensor
          object_id: 3303
          instance_id: 0
          resource_id: 5700
          operation: read
          read_attribute: "#attr(temperature)"
        - name: setpoint
          object_id: 3308
          instance_id: 0
          resource_id: 5900
          operation: write
          write_attribute: "#attr(setpoint)"
```

## Notes

- Dependency: requires `aiocoap` (tests are skipped when it is missing).
- The binding schema is LwM2M-specific (`object_id` / `instance_id` / `resource_id` + `operation`).
- `spx-examples` currently contains an `lwm2m` model using a different (older) schema. Prefer the binding schema shown here until the example is aligned:
  - [`environment_sensor__lwm2m.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__lwm2m.yaml)
