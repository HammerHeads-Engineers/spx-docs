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

- Bring the server up: `getting-started/installation-guide.md`
- Build a first Model + Instance: `getting-started/build-your-first-simulation.md`
- Make it testable: `getting-started/use-in-unit-tests-mil.md`
- Capture/restore state: `getting-started/snapshots-guide.md`
- Extend beyond YAML: `simulation-and-modeling/extending-simulations/README.md`
