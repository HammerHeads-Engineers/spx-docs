# PROFINET adapters

SPX Server ships:

- `profinet_server` — synchronises SPX attributes with PROFINET IO/record areas via a transport adapter
- `profinet_snap7_adapter` — Snap7-based transport adapter (Siemens PLC) used by `profinet_server`

## `profinet_server`

**YAML key:** `profinet_server`

Minimal example:

```yaml
communication:
  - profinet_server:
      cycle_time: 0.05
      device:
        host: 127.0.0.1
      bindings:
        - name: command_speed
          direction: outbound
          area: output
          slot: 1
          subslot: 1
          offset: 0
          length: 4
          codec: float
          read_attribute: "#attr(command.speed)"
        - name: status_word
          direction: inbound
          area: input
          slot: 1
          subslot: 1
          offset: 4
          length: 2
          codec: uint16
          write_attribute: "#attr(status.word)"
```

## `profinet_snap7_adapter` (transport)

**YAML key:** `profinet_snap7_adapter`

Use this adapter via `profinet_server.transport`:

```yaml
communication:
  - profinet_server:
      transport:
        class: profinet_snap7_adapter
        host: 192.168.0.10
        rack: 0
        slot: 1
        tcp_port: 102
        timeout: 5.0
      bindings: []
```

## Transport scope

The Snap7 transport uses the S7 protocol on TCP (typically 102). This does not
implement or certify a full PROFINET IO real-time device stack. Confirm the
transport required by your SUT; source-level adapter tests are not physical
PROFINET conformance tests.

## Notes

- `profinet_server` accepts either `bindings:` or legacy `mapping:` (auto-converted to bindings).
- `profinet_snap7_adapter` requires `python-snap7` when used.
