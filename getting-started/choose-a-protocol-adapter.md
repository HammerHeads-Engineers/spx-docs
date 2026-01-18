---
description: Pick the right communication adapter (Modbus, ASCII/SCPI, MQTT, BLE, HTTP) for your simulated device and your SUT.
icon: plug
---

# Choose a protocol adapter

SPX models can expose signals over protocol adapters so your **Software Under Test (SUT)** can talk to a simulation as if it were real hardware.

Use this page to pick the adapter that matches your client/driver, then follow either:

- the adapter reference docs under [Communication Adapters](../spx-core/communications/README.md), or
- a runnable baseline from `spx-examples` (models + tests).

## Quick routing

| Adapter | When to use | Docs | Example model (spx-examples) |
|---|---|---|---|
| Modbus TCP | PLC/HMI/device drivers using Modbus | [Modbus](../spx-core/communications/modbus.md) | [`thermal_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/thermal_controller__modbus.yaml) |
| ASCII / SCPI | Lab instruments, SCPI drivers | [ASCII](../spx-core/communications/ascii.md) | [`multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/measurement_instruments/generic/multimeter__scpi.yaml) |
| MQTT | IoT telemetry pipelines and brokers | [MQTT](../spx-core/communications/mqtt.md) | [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__mqtt.yaml) |
| BLE | Mobile apps and BLE test rigs | [BLE](../spx-core/communications/ble.md) | [`temperature_sensor__ble_gatt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/ble/generic/temperature_sensor__ble_gatt.yaml) |
| HTTP endpoint | Simple REST callbacks / webhooks | [HTTP](../spx-core/communications/http.md) | [`air_quality_station__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/air_quality_station__http.yaml) |

## Note on ports (Docker)

Protocol adapters listen on TCP/UDP ports **in the SPX Server container**. If your SUT runs on the host, you must expose the adapter port(s) in your `docker-compose.yml`.

For a working baseline, `spx-examples/docker-compose.yml` already exposes common ports (API `8000`, Modbus `502`, SCPI/ASCII `5025`, ...).

## Next steps

- Example tutorial: [Add a Modbus TCP/IP to Your Simulation](add-communication-protocol.md)
- Deterministic QA flow: [Use in Unit Tests (MiL)](use-in-unit-tests-mil.md)
