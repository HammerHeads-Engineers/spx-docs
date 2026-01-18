# Integration with Other Systems

SPX integrates with external systems through the same interfaces your real devices use. In most projects, the integration boundary is a protocol adapter:

- Modbus: [Modbus Adapter](spx-core/communications/modbus.md)
- MQTT: [MQTT Adapter](spx-core/communications/mqtt.md)
- HTTP: [HTTP Adapter](spx-core/communications/http.md)
- ASCII/SCPI: [ASCII / SCPI Adapter](spx-core/communications/ascii.md)
- BLE (via companion service): [BLE Adapter](spx-core/communications/ble.md)

## Recommended pattern

1. Keep the **Model** deterministic (driven by MiL tests).
2. Expose the model through the required protocol adapter.
3. Validate integration with an end-to-end test suite that runs in CI.

Start with: [Use in Unit Tests (MiL)](getting-started/use-in-unit-tests-mil.md).
