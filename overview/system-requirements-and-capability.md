# System Requirements and Capability

This page lists the practical prerequisites for running SPX locally (Docker) and authoring/testing models from Python.

## Runtime prerequisites (SPX Server)

* **Docker Engine/Desktop** with **Docker Compose v2** (`docker compose`).
* A valid **SPX product key** available as `SPX_PRODUCT_KEY` (get it from `https://simplephysx.com`).
* Local port **8000** free (default SPX Server API).

If you enable protocol adapters, you may need to expose additional ports (for example Modbus TCP `502`, SCPI/ASCII instrument ports, MQTT, BLE adapter HTTP). Keep port mappings in your `docker-compose.yml` aligned with the models you run.

See: [Communication Adapters](/broken/pages/Xj0Kch85KiFEX0H4nFce).

## Authoring/testing prerequisites (SDK + MiL tests)

* **Python**: `>=3.9` (tested in CI on `3.9–3.12`).
* **Test runner**: `pytest` (recommended) for MiL test suites.
* **HTTP tooling**: `curl` or similar for quick API checks.

## Optional toolchain

* **SPX UI**: a modern browser (the UI talks to the SPX Server API).
* **BLE simulations**: `spx-ble-adapter` requires Node.js (see [BLE Adapter](../spx-core/communications/ble.md)).
