# Overview

SPX (SimplePhysX) is a deterministic simulation stack you can run locally (Docker) and drive from code for repeatable testing.

SPX is split into:

- **SPX Server**: runtime that loads **Models**, runs live **Instances**, executes **Scenarios**, serves **Snapshots**, and exposes a REST API (default `http://localhost:8000`).
- **SPX SDK**: author models/components in a structured way (YAML definitions + Python extension points).
- **SPX UI**: inspect Instances, attributes/state, scenarios, logs, and snapshots while debugging.

Core workflow (the “happy path”):

1. Start SPX Server via `docker compose`.
2. Load or edit a Model definition (YAML/Python).
3. Create an Instance.
4. Drive simulation time deterministically from tests (**MiL tests**) and validate outcomes.
5. Use Snapshots for reproducible starting states and fast iteration.

Start here:

- `getting-started/installation-guide.md`
- `getting-started/build-your-first-simulation.md`
- `getting-started/snapshots-guide.md`
- `getting-started/use-in-unit-tests-mil.md`
