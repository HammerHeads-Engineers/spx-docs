# OPC UA server adapter

**YAML key:** `opcua_server`

Expose an OPC UA server (`opc.tcp://...`) and map nodes to SPX attributes.

## Minimal configuration

Example model (spx-examples):
[`library/domains/iot/generic/production_workcell__opcua.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/production_workcell__opcua.yaml)

```yaml
communication:
  - opcua_server:
      endpoint: opc.tcp://0.0.0.0:4841/spx/workcell
      namespace_uri: urn:spx:examples:opcua:workcell
      security:
        policy: NoSecurity
        user_tokens:
          - type: anonymous
      sections:
        - name: station
          browse_path: ["Workcell"]
          bindings:
            - name: MachineState
              direction: outbound
              attributes: "#attr(machine_state)"
              node:
                browse_path: ["State"]
                data_type: String
            - name: StationMode
              direction: bidirectional
              read_attribute: "#attr(station_mode)"
              write_attribute: "#attr(station_mode)"
              node:
                browse_path: ["Mode"]
                data_type: String
```

## Notes

- Dependency: requires `asyncua` in the SPX Server environment.
- Bindings support either `attributes` (single attribute) or explicit `read_attribute` / `write_attribute` for bidirectional nodes.

## Next steps on simplephysx.com

Explore the OPC UA simulator workflow:

- [OPC UA Simulator](https://www.simplephysx.com/opc-ua-simulator)
