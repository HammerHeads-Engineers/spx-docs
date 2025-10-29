---
icon: satellite-dish
---

# Communication Adapters

`spx_core/communications` hosts production-ready protocol servers. Each adapter exposes the same YAML interface you experiment with in the SDK, but the server version adds concurrency, retries, metrics, and health checks.

The shared concepts:

* **Lifecycle**: adapters implement `prepare`, `start`, `run`, `stop`, `destroy`.
* **Mappings**: YAML entries map protocol requests to attribute wrappers or call handlers.
* **Overrides**: scenarios can adjust adapter properties at runtime (latency, disconnects).

Subpages cover the built-in adapters:

* [ASCII / SCPI](ascii.md)
* [HTTP](http.md)
* [Modbus](modbus.md)
* [MQTT](mqtt.md)

Tips:

* Keep protocol ports/config in `parameters` so deployments can override them per environment.
* Leverage scenarios for chaos testing (detach, delay spikes, message drops).
* Monitor adapter metrics exposed via the server API (request counts, error rates).
