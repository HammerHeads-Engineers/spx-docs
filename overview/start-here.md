# Start here (by role)

Use this page to pick the shortest “golden path” based on what you’re building.

Common prerequisites:

- Docker + Docker Compose v2 (`docker compose`)
- `SPX_PRODUCT_KEY` in your environment
- Optional: `SPX_BASE_URL` (defaults to `http://localhost:8000`)

## Reference repository: spx-examples

For the latest runnable models, installer profiles, generated bundle tooling,
and MiL tests, use the public
[spx-examples repository](https://github.com/HammerHeads-Engineers/spx-examples).

## LLM / Agent workflow

Goal: use Codex, Claude Code, or another MCP-capable LLM client to inspect and
control a local SPX runtime through MCP.

1. Install and start SPX: [Installation Guide](../getting-started/installation-guide.md)
2. Create the MCP workspace: [Connect an LLM with SPX MCP](../getting-started/connect-llm-with-spx-mcp.md)
3. In your MCP client, use the generated workspace to inspect server health,
   list models and instances, and make runtime changes through SPX MCP tools

## Integrator (protocol + SUT client)

Goal: run SPX Server, expose a protocol adapter, and point your client/driver at it.

1. Start the server: [Installation Guide](../getting-started/installation-guide.md)
2. Build a minimal model + instance: [Build Your First Simulation](../getting-started/build-your-first-simulation.md)
3. Choose an adapter + expose ports: [Choose a protocol adapter](../getting-started/choose-a-protocol-adapter.md)
4. Use a known-good example model for your protocol (from `spx-examples`
   `develop`):
   - Modbus: [`energy_meter_iem3000__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/energy/meter/schneider/energy_meter_iem3000__modbus.yaml)
   - MQTT: [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/environment/sensor/generic/environment_sensor__mqtt.yaml)
   - SCPI/ASCII: [`multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/instrument/generic/multimeter__scpi.yaml)
5. If something fails, start with: [Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md)

## Ready pack walkthrough

Goal: launch a ready-to-test stack with models, services, and optional UI.

1. Install and start SPX: [Installation Guide](../getting-started/installation-guide.md)
2. Walk through the ready smart-building stack:
   [Smart Building Pack: First Run Walkthrough](../getting-started/first-run-smart-building-pack.md)
3. For custom pack/profile generation, use the advanced reference:
   [Installer and Packs (spx-examples)](../getting-started/installer-and-packs.md)

## Developer (model authoring + extensions)

Goal: author models and reusable custom logic (components/actions) safely and test-gate changes.

1. Understand core terms: [Core Concepts](../simulation-and-modeling/core-concepts.md)
2. Learn the SDK building blocks: [SPX SDK](../spx-development-guide/spx-sdk/README.md)
3. Add custom Python logic: [Extend with a Custom Component](../getting-started/extend-with-custom-component.md)
4. Packaging/imports:
   - [Registry](../spx-development-guide/spx-sdk/registry.md)
   - [Imports](../spx-development-guide/spx-sdk/imports/README.md)
5. Validate with tests: [Testing and Validation](../testing-and-validation.md)

## QA/CI (MiL tests + snapshots)

Goal: run deterministic MiL suites locally and in CI, with reproducible starting state.

1. Drive SPX from tests: [Use in Unit Tests (MiL)](../getting-started/use-in-unit-tests-mil.md)
2. Wire into pipelines: [CI/CD Setup (GitHub Actions)](../getting-started/ci-cd-setup-github-actions.md)
3. Use Snapshots as fixtures when needed: [Snapshots — Getting Started](../getting-started/snapshots-guide.md)
4. Pin versions and upgrade safely: [Release Notes](../release-notes.md)
