# Use Case and Applications

SPX is typically used as a deterministic “plant/device” behind your real client code. The **quality gate** is a test suite (MiL tests) that drives time explicitly and asserts behavior.

Below are concrete, repo-grounded use cases (models and tests live in `spx-examples`).

## MiL integration tests for Modbus clients

- Template model: `spx-examples/library/domains/thermal_controllers/generic/thermal_controller__modbus.yaml`
- Your Software Under Test: a Modbus TCP client (PLC code, gateway, driver, etc.)
- SPX role: deterministic device state + faults + time control

Docs: `getting-started/add-communication-protocol.md`, `getting-started/use-in-unit-tests-mil.md`.

## Simulate SCPI/ASCII instruments for driver testing

- Template model: `spx-examples/library/domains/measurement_instruments/generic/multimeter__scpi.yaml`
- Your Software Under Test: instrument driver speaking SCPI over TCP
- SPX role: instrument state machine + predictable waveforms/scenarios

Docs: `spx-core/communications/ascii.md`, `getting-started/use-in-unit-tests-mil.md`.

## MQTT device telemetry regression tests

- Template model: `spx-examples/library/domains/iot/generic/environment_sensor__mqtt.yaml`
- Your Software Under Test: telemetry ingestion / rules engine / alerting
- SPX role: controllable publish cadence, payload values, and fault injection

Docs: `spx-core/communications/mqtt.md`.

## BLE device simulation for mobile apps and QA rigs

- Template model: `spx-examples/library/domains/ble/generic/temperature_sensor__ble_gatt.yaml`
- Companion process: `spx-ble-adapter` exposes a real BLE peripheral backed by SPX attributes

Docs: `spx-core/communications/ble.md`, `simulation-and-modeling/extending-simulations/ble-device-simulation.md`.

## Snapshot-driven regression suites

- Capture a known-good state as a Snapshot.
- Restore it before a test so every run starts from the same simulation state.

Docs: `getting-started/snapshots-guide.md`, `spx-core/snapshots.md`.
