# Integration with Other Systems

SPX integrates with external systems through the same interfaces your real devices use. In most projects, the integration boundary is a protocol adapter:

* Modbus: [Modbus Adapter](/broken/pages/HspwARSmThhECwKIDxp5)
* MQTT: [MQTT Adapter](/broken/pages/wQZmN7ix2NnrhI2FK9Mr)
* HTTP: [HTTP Adapter](/broken/pages/RlZU1sXYyJg1oMkOAkD1)
* ASCII/SCPI: [ASCII / SCPI Adapter](/broken/pages/ZHfz8dNOl5kwq5lKEQy5)
* BLE (via companion service): [BLE Adapter](spx-core/communications/ble.md)

## Recommended pattern

1. Keep the **Model** deterministic (driven by MiL tests).
2. Expose the model through the required protocol adapter.
3. Validate integration with an end-to-end test suite that runs in CI.

Start with: [Use in Unit Tests (MiL)](getting-started/use-in-unit-tests-mil.md).
