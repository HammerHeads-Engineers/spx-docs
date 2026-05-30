# KNX/IP adapters

SPX Server ships two KNX components:

- `knx_ip` — KNXnet/IP client (talks to a router/gateway)
- `knx_ip_simulator` — in-memory KNX bus simulator for local testing

## `knx_ip` (KNXnet/IP client)

**YAML key:** `knx_ip`

Example model (spx-examples):
[`library/domains/iot/generic/room_controller__knx.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/room_controller__knx.yaml)

```yaml
communication:
  - knx_ip:
      router:
        host: knx_gateway
        port: 3671
        route_back: true
      poll_interval: 0.3
      bindings:
        - name: room_temperature
          direction: outbound
          group_address: "2/0/1"
          dpt: 9.001
          read_attribute: "#attr(room_temperature_c)"
        - name: setpoint_command
          direction: bidirectional
          group_address: "2/0/2"
          dpt: 9.001
          read_attribute: "#attr(room_command_c)"
          write_attribute: "#attr(room_command_c)"
```

Notes:

- Dependency: `knx_ip` requires `xknx` in the SPX Server environment.
- Use `dpt` (for example `9.001`) or `value_codec` (for example `bool`, `uint8`) to control encoding.

## `knx_ip_simulator` (in-memory bus)

**YAML key:** `knx_ip_simulator`

```yaml
communication:
  - knx_ip_simulator:
      poll_interval: 0.5
      bindings:
        - name: room_temperature
          direction: bidirectional
          group_address: "2/0/1"
          dpt: 9.001
          read_attribute: "#attr(room_temperature_c)"
          write_attribute: "#attr(room_temperature_c)"
```

## Next steps on simplephysx.com

Explore the KNX simulator workflow:

- [KNX Simulator](https://www.simplephysx.com/knx-simulator)
