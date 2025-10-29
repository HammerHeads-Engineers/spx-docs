# Modbus Adapter

The Modbus adapter presents registers and coils so external PLCs or software masters can interact with your simulation.

## YAML structure

```yaml
communication:
  modbus_tcp:
    host: 0.0.0.0
    port: 502
    unit_id: 1
    mapping:
      voltage:
        group: holding
        address: 0
        type: float
      heater_on:
        group: coils
        address: 10
        type: bool
```

```json
{
  "communication": {
    "modbus_tcp": {
      "host": "0.0.0.0",
      "port": 502,
      "unit_id": 1,
      "mapping": {
        "voltage": {
          "group": "holding",
          "address": 0,
          "type": "float"
        },
        "heater_on": {
          "group": "coils",
          "address": 10,
          "type": "bool"
        }
      }
    }
  }
}
```

### Key fields

- `host` / `port`: bind address, default 0.0.0.0:502.
- `unit_id`: Modbus unit/slave ID.
- `mapping`: one entry per attribute.
  - `group`: `holding`, `input`, `coils`, or `discrete`.
  - `address`: starting register/coil address.
  - `type`: numeric or boolean encoding (`uint16`, `float`, `bool`, etc.).
  - Optional `length` for arrays.

### Read/write behavior

- Reads return `external_value` unless overridden by scenarios.
- Writes update `external_value` and trigger hooks (`on_external_set`).
- Use actions to propagate external writes to internal state if needed.

### Endianness & packing

The adapter supports standard Modbus packing. For custom packing, implement a small wrapper action that translates external writes into structured values.

### Scenarios

```yaml
scenarios:
  modbus_disconnect:
    duration: 3.0
    call:
      path: communication.modbus_tcp.detach
      stop_path: communication.modbus_tcp.attach
  modbus_noise:
    duration: 5.0
    overrides:
      communication.modbus_tcp.response_delay: 0.5
```

```json
{
  "scenarios": {
    "modbus_disconnect": {
      "duration": 3.0,
      "call": {
        "path": "communication.modbus_tcp.detach",
        "stop_path": "communication.modbus_tcp.attach"
      }
    },
    "modbus_noise": {
      "duration": 5.0,
      "overrides": {
        "communication.modbus_tcp.response_delay": 0.5
      }
    }
  }
}
```

### Tips

- Keep addresses contiguous for performance.
- Document register maps alongside YAML so firmware teams stay in sync.
- Use unit tests with a Modbus client library (`pymodbus`, `modbus-tk`) to validate behavior before deploying.
