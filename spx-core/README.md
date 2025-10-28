---
icon: circuit-board
---

# SPX-CORE

The SPX Server ships with a high-performance core that executes your models in production. Think of it as the runtime counterpart to the SDK: the YAML you author locally is loaded here and translated into worker processes, protocol adapters, and snapshots.

This section maps each core module to its responsibilities and shows how to configure it.

## What lives in SPX-CORE?

- **System runtime:** orchestrates models, instances, timers, scenarios, and connections.
- **Actions library:** built-in behaviors (ramps, PID, noise, overrides) that mutate attributes over time.
- **Communication adapters:** Modbus, ASCII/SCPI, HTTP, MQTT.
- **Snapshots:** capture and restore full simulation state.
- **Extensibility hooks:** load custom Python modules, install dependencies, and register new components.

Use the SDK for prototyping; deploy the same definitions to the core when you need concurrency, networking, and observability.

## What is next?

- [System Runtime](system.md)
- [Actions Library](actions.md)
- [Communication Adapters](communications/README.md)
- [Snapshots](snapshots.md)
- [Extending the Core](extending.md)
