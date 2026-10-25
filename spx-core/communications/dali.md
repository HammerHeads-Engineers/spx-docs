# DALI-IP client adapter

**YAML key:** `dali`

Synchronise SPX attributes with a DALI-IP gateway by sending DALI frames (and optionally decoding replies).

## Minimal configuration

```yaml
attributes:
  level: 10
  power_w: 0.0

communication:
  - dali:
      transport: udp
      gateway_host: 127.0.0.1
      gateway_port: 55825
      poll_interval: 1.0
      response_timeout: 0.5
      bindings:
        - name: luminaire_5
          direction: outbound
          short_address: 5
          commands:
            - name: set_level
              opcode: 0xA3
              payload_codec: u8
              attribute: "#attr(level)"

        - name: meter_2
          direction: inbound
          short_address: 2
          commands:
            - name: read_power
              opcode: 0x90
              expects_reply: true
              payload_codec: u16
              attribute: "#attr(power_w)"
```

## Notes

- `transport`: `udp|tcp|serial`
- Gateway connection config is provided at the protocol level (`gateway_host`, `gateway_port`) or via the optional `gateway:` block.
- Bindings describe DALI targets (`short_address` / `group_address` / `broadcast` / `instance_id`) and the command list (`commands`).
