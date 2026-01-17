# Integration with Other Systems

SPX integrates with external systems through the same interfaces your real devices use. In most projects, the integration boundary is a protocol adapter:

- Modbus: `spx-core/communications/modbus.md`
- MQTT: `spx-core/communications/mqtt.md`
- HTTP: `spx-core/communications/http.md`
- ASCII/SCPI: `spx-core/communications/ascii.md`
- BLE (via companion service): `spx-core/communications/ble.md`

## Recommended pattern

1. Keep the **Model** deterministic (driven by MiL tests).
2. Expose the model through the required protocol adapter.
3. Validate integration with an end-to-end test suite that runs in CI.

Start with: `getting-started/use-in-unit-tests-mil.md`.
