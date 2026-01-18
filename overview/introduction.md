# Introduction

## What is SPX?

SPX is a deterministic simulation stack you can run locally and drive from code. You author **Models**, start live **Instances** on the **SPX Server**, and step simulation time explicitly from a client (for example, `spx-python`) so tests are repeatable.

## Mental model

- **Model**: a definition (usually YAML, optionally backed by custom Python components) describing attributes, actions, timers, communications, and scenarios.
- **Instance**: a running copy of a Model with state you can inspect/mutate.
- **Scenario**: a repeatable script of events (fault injection, parameter changes, sequencing).
- **MiL test**: a Model-in-the-Loop test that drives SPX deterministically as the plant/device while your Software Under Test acts as the real client.
- **Snapshot**: a captured simulation state you can restore to get a known starting point.

## Where to start

- Bring the server up: [Installation Guide](../getting-started/installation-guide.md)
- Build a first Model + Instance: [Build Your First Simulation](../getting-started/build-your-first-simulation.md)
- Make it testable: [Use in Unit Tests (MiL)](../getting-started/use-in-unit-tests-mil.md)
- Capture/restore state: [Snapshots — Getting Started](../getting-started/snapshots-guide.md)
- Extend beyond YAML: [Extending Simulations](../simulation-and-modeling/extending-simulations/README.md)
