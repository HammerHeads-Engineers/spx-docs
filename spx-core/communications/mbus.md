# M-Bus adapters

SPX Server ships two M-Bus components:

- `mbus` — M-Bus master/client (serial / TCP / loopback transports)
- `mbus_server` — in-memory loopback server used for tests and tooling

## `mbus` (client)

**YAML key:** `mbus`

Minimal example (based on `spx-server` unit tests):

```yaml
attributes:
  flow_temp: 35.0

communication:
  - mbus:
      transport: tcp
      host: 127.0.0.1
      port: 10001
      poll_interval: 5.0
      bindings:
        - name: heat_meter
          primary_address: 5
          frames:
            - name: flow_temperature
              codec: float32
              direction: inbound
              attribute: "#attr(flow_temp)"
              poll_interval: 2.0
```

Notes:

- Serial transport requires an M-Bus library (see server code for the dependency guard).
- `loopback` transport is available for tests (attach an `mbus_server`).

## `mbus_server` (loopback server)

**YAML key:** `mbus_server`

```yaml
attributes:
  energy_kwh: 12.5

communication:
  - mbus_server:
      bindings:
        - name: water_meter
          primary_address: 1
          frames:
            - name: energy_total
              record_key: energy_total
              codec: float32
              direction: outbound
              attribute: "#attr(energy_kwh)"
```

## Contract (tests)

- `spx-server/tests/test_spx_core/test_communications/test_mbus/`
