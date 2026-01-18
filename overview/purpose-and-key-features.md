# Key Features

SPX is built for building **testable simulation models** and validating them with deterministic, code-driven workflows.

## Deterministic simulation control

- Run SPX as a server process (typically in Docker).
- Drive simulation time explicitly from a client (MiL tests) instead of relying on wall-clock time.
- Inspect and mutate runtime state through the API and UI.

Start here:

- [Model-in-the-Loop (MiL) with SPX](../simulation-and-modeling/model-in-the-loop.md)
- [Using spx-python for Simulation](../simulation-and-modeling/using-spx-python.md)

## Model authoring (YAML + Python)

- Author models as YAML definitions (attributes, actions, timer, communication).
- Extend behavior with custom Python classes via the SDK registry.

Start here:

- [SPX SDK](../spx-development-guide/spx-sdk/README.md)
- [Extending Simulations](../simulation-and-modeling/extending-simulations/README.md)

## Protocol adapters and integrations

SPX ships with built-in communication adapters (e.g., Modbus, MQTT, HTTP, ASCII/SCPI, BLE) so your Software Under Test can talk to the simulation over the same interfaces as real hardware.

Start here: [Communication Adapters](../spx-core/communications/README.md).

## Scenarios, snapshots, and testing

- Use **Scenarios** to script repeatable events (fault injection, step changes, sequencing).
- Use **Snapshots** to capture/restore state for fast iteration and stable tests.
- Wire everything into `pytest`/CI using `docker compose` + MiL test helpers.

Start here:

- [Scenarios](../spx-core/system/scenarios.md)
- [Snapshots (Core)](../spx-core/snapshots.md)
- [Use in Unit Tests (MiL)](../getting-started/use-in-unit-tests-mil.md)
- [Snapshots — Getting Started](../getting-started/snapshots-guide.md)
