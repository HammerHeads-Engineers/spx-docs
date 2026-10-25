# SNMP adapters

SPX Server ships two SNMP components:

- `snmp` — SNMP client (UDP / loopback transports)
- `snmp_server` — in-memory loopback server used for tests and tooling

## `snmp` (client)

**YAML key:** `snmp`

Minimal example (UDP transport):

```yaml
attributes:
  temperature: 0.0

communication:
  - snmp:
      transport: udp
      host: 192.168.1.50
      port: 161
      version: v2c
      community: public
      poll_interval: 5.0
      bindings:
        - name: temp_read
          direction: inbound
          operation: get
          oid: 1.3.6.1.4.1.9999.1.0
          codec: float32
          attribute: "#attr(temperature)"
```

## `snmp_server` (loopback server)

**YAML key:** `snmp_server`

```yaml
attributes:
  setpoint: 20.0

communication:
  - snmp_server:
      transport: loopback
      bindings:
        - name: temp_setpoint
          direction: inbound
          operation: set
          oid: 1.3.6.1.4.1.9999.1.1
          codec: float32
          attribute: "#attr(setpoint)"
```

## Notes

- UDP transport uses `pysnmp` under the hood (see server code for supported SNMPv2c/SNMPv3 fields).
- Loopback transport is used by unit tests (attach a server to the client).
