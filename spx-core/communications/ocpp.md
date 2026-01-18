# OCPP 1.6J adapter

**YAML key:** `ocpp`

OCPP adapter that can run as a Charge Point (`role: charge_point`) or as a Central System (`role: central_system`).

## Minimal configuration (Charge Point)

Example model (spx-examples):
[`library/domains/energy/emobility/evse__ocpp.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/energy/emobility/evse__ocpp.yaml)

```yaml
communication:
  - ocpp:
      role: charge_point
      endpoint: "ws://localhost:9000/ocpp"
      subprotocol: "ocpp1.6"
      charge_point_id: "spx-evse-01"
      bindings:
        boot_notification:
          direction: outbound
          frame_type: call
          action: BootNotification
          payload:
            chargePointVendor: "#attr(cp_vendor)"
            chargePointModel: "#attr(cp_model)"
```

## Minimal configuration (Central System)

Example model (spx-examples):
[`library/domains/energy/emobility/csms__ocpp.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/energy/emobility/csms__ocpp.yaml)

```yaml
communication:
  - ocpp:
      role: central_system
      server:
        host: 0.0.0.0
        port: 9000
        path: "/ocpp"
        subprotocol: "ocpp1.6"
      bindings:
        boot_request:
          direction: inbound
          frame_type: call
          action: BootNotification
          payload:
            chargePointVendor: "#attr(last_boot_vendor)"
            chargePointModel: "#attr(last_boot_model)"
```

## Notes

- Dependency: requires the Python `ocpp` package in the SPX Server environment.
- `bindings` can be a mapping (as shown) or a list; the binding schema is defined in `spx-server/spx_core/communications/ocpp/bindings.py`.

## Contract (tests)

- `spx-server/tests/test_spx_core/test_communications/test_ocpp/`
