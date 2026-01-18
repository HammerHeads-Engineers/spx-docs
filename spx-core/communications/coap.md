# CoAP server adapter

**YAML key:** `coap_server`

Expose CoAP resources over UDP and map requests onto SPX attributes using resource/binding definitions.

## Minimal configuration

Based on `spx-server/tests/test_spx_core/test_communications/test_coap/test_coap_integration.py`:

```yaml
attributes:
  temperature: 23.5
  setpoint: 18.0

communication:
  - coap_server:
      host: 127.0.0.1
      port: 5683
      default_payload_codec: json
      resources:
        - name: process
          path: [process]
          bindings:
            - name: temperature_get
              method: get
              direction: outbound
              read_attribute: "#attr(temperature)"
              payload_codec: json
              path: [temperature]
            - name: setpoint_put
              method: put
              direction: inbound
              write_attribute: "#attr(setpoint)"
              payload_codec: json
              path: [setpoint]
```

## Notes

- Dependency: requires `aiocoap` (tests are skipped when it is missing).
- Bindings support `get`, `put`, and `observe` (see the server tests for the exact schema).

## Contract (tests)

- `spx-server/tests/test_spx_core/test_communications/test_coap/`
