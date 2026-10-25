# Overview

SPX (SimplePhysX) is a deterministic simulation stack you can run locally (Docker) and drive from code for repeatable testing.

SPX is split into:

- **SPX Server**: runtime that loads **Models**, runs live **Instances**, executes **Scenarios**, serves **Snapshots**, and exposes a REST API (default `http://localhost:8000`).
- **SPX SDK**: author models/components in a structured way (YAML definitions + Python extension points).
- **SPX UI**: inspect Instances, attributes/state, scenarios, logs, and snapshots while debugging.

Core workflow (the “happy path”):

1. Install SPX with [SPX Setup](getting-started/installation-guide.md), then start the installed environment.
2. Load or edit a Model definition (YAML/Python).
3. Create an Instance.
4. Drive simulation time deterministically from tests (**MiL tests**) and validate outcomes.
5. Use Snapshots for reproducible starting states and fast iteration.

Start here:

- [Installation Guide](getting-started/installation-guide.md)
- [Build Your First Simulation](getting-started/build-your-first-simulation.md)
- [Snapshots — Getting Started](getting-started/snapshots-guide.md)
- [Use in Unit Tests (MiL)](getting-started/use-in-unit-tests-mil.md)

## Documentation and repository responsibilities

This portal is the canonical product documentation, maintained on `spx-docs/main`.
[Public spx-examples](https://github.com/HammerHeads-Engineers/spx-examples) owns
models, catalogs, profiles, runnable examples, runtime MCP modules and agent
working instructions. Its README links back here; its model and MCP reference
files are generated offline snapshots. The private `spx-installer` owns
installation, Python/MCP preparation, packaging, signing and release publication.

This edition targets installer **v1.1.0-rc.115**, server/UI **v1.0.0-rc.76**,
SDK **v1.0.0-rc.21** and Python client **1.0.0-rc.3**. See the
[release baseline](release-notes.md) before mixing independently published versions.
