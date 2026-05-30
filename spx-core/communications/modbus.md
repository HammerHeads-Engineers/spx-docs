# Modbus adapters

SPX Server provides three Modbus components:

- `modbus_slave` — Modbus TCP slave/server based on `pymodbus`
- `modbus_tcp` — Modbus TCP slave/server based on `modbus-tk` (legacy/compat; avoid for new models)
- `modbus_master` — Modbus TCP master/client that polls and/or writes bindings

## Addressing vocabulary

SPX uses short area codes (the same values appear in `spx-examples`):

- `h_r` — holding registers
- `i_r` — input registers
- `c_o` — coils
- `d_i` — discrete inputs

Value codecs commonly used in mappings/bindings:

- `float`, `bool`, `int_16`, `int_32`, `uint_16`, `uint_32`, `str`, `raw`

Addresses can be a single integer or a `[start, end]` pair (use a pair for multi-register values like `float`).

## `modbus_slave` (pymodbus server)

**YAML key:** `modbus_slave`

Example model (spx-examples):
[`library/domains/iot/generic/energy_meter_iem3000__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/energy_meter_iem3000__modbus.yaml)

```yaml
communication:
  - modbus_slave:
      host: 0.0.0.0
      # If omitted, SPX auto-picks the first free port >= 5020 for this host.
      port: 5023
      unit_id: 1
      zero_fill: true
      # Legacy format (accepted): mapping → converted internally to bindings.
      mapping:
        current_l1_a: { address: [3000, 3001], group: i_r, type: float }
        energy_import_kwh: { address: [45100, 45101], group: h_r, type: float }
```

Connectivity simulation:

- `detach()` enters “blackhole” mode (keeps TCP listener, suppresses responses → client timeouts).
- `attach()` exits blackhole mode and restarts the server to drop stale connections.

```yaml
scenarios:
  modbus_timeouts:
    duration: 5.0
    call:
      path: communication.modbus_slave.detach
      stop_path: communication.modbus_slave.attach
```

### Shared server behavior (multiple unit IDs on one port)

In current SPX Server runtime, `modbus_slave` instances sharing the same `host:port` reuse one shared TCP server and register separate `unit_id` contexts.

- This allows multiple models/devices to be exposed on the same Modbus TCP port.
- Register map isolation remains per `unit_id`.
- Duplicate `unit_id` on the same `host:port` is rejected (runtime error / API validation failure).

Operational note:

- `attach()` may trigger a server restart only when this protocol instance is the sole owner on that port (to avoid dropping connections for other unit IDs).

## `modbus_tcp` (modbus-tk server)

**YAML key:** `modbus_tcp`

> **Legacy adapter**: `modbus_tcp` exists for backward compatibility. Avoid it for new models; prefer `modbus_slave` for Modbus TCP server simulations.

Example model (spx-examples):
[`library/domains/thermal_controllers/generic/thermal_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/thermal_controller__modbus.yaml)

```yaml
communication:
  - modbus_tcp:
      host: 0.0.0.0
      port: 502
      id: 1
      poll_interval: 0.25
      response_delay: 0.0
      mapping:
        temperature: { address: [0, 1], group: h_r, type: float }
        power_on: { address: [6, 6], group: c_o, type: uint_16 }
```

Connectivity simulation uses `detach()` / `attach()` (removes/re-adds the slave from the shared Modbus master).

## `modbus_master` (client / poller)

**YAML key:** `modbus_master`

For a guided controller example, see
[Use SPX as a Modbus Client / PLC Controller](../../getting-started/modbus-client-controller.md).

Minimal example:

```yaml
communication:
  - modbus_master:
      poll_interval: 0.2
      timeout: 1.0
      bindings:
        - name: temperature_in
          host: 127.0.0.1
          port: 1502
          slave_id: 1
          area: h_r
          address: 300
          length: 2
          codec: float
          direction: inbound
          attribute: "#attr(temp_read)"

        - name: coil_out
          host: 127.0.0.1
          port: 1502
          slave_id: 1
          area: c_o
          address: 4
          length: 1
          codec: bool
          direction: outbound
          attribute: "#attr(alarm_write)"
```

Notes:

- Dependency: `modbus_master` uses `modbus_tk` (`TcpMaster`) under the hood (same family as `modbus_tcp`). If `modbus_tk` is missing, reads/writes will fail.
- Per-binding `host` / `port` / `slave_id` let one `modbus_master` talk to multiple devices.
- `direction`: `inbound` (read → write attribute), `outbound` (read attribute → write registers/coils), `bidirectional` (both). If omitted, SPX defaults to `inbound` for polling.

### Top-level fields

- `host` / `port` — default connection target for bindings (defaults: `127.0.0.1:502`)
- `timeout` — per-operation timeout in seconds (default: `1.0`)
- `poll_interval` — default poll interval in seconds (default: `0.2`)
- `ops_per_cycle` — max binding ops per worker cycle (default: `16`)
- `max_retries` / `retry_delay` — retry policy for one read/write attempt (defaults: `1` / `0.05`)
- `max_failures` — after this many failures the binding is disabled (default: `3`)
- `min_poll_interval` — lower bound for polling cadence (default: `0.05`)

### Binding fields

Each entry under `bindings` is a Modbus master binding:

- Connection overrides: `host`, `port`, `slave_id`
- Register selection: `area` (alias: `group`), `address` (int or `[start, end]`), `length`
- Encoding: `codec` (alias: `type`), `bit_order` (alias: `byte_order`)
- Attribute mapping: `attribute` (shorthand) or explicit `read_attribute` / `write_attribute`
- Timing/stability overrides: `poll_interval`, `timeout`, `max_retries`, `retry_delay`, `max_failures`

Write semantics:

- Coils (`area: c_o`) and holding registers (`area: h_r`) are writable.
- Discrete inputs (`d_i`) and input registers (`i_r`) are read-only (outbound writes will error).
- Codec/length must match (for example `float` requires `length: 2`; `uint_16` requires `length: 1`).
