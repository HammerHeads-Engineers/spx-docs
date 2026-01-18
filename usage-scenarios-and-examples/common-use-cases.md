# Guided Use Cases & Scenarios

This page focuses on scenario-driven engineering workflows (integrators/dev/QA), grounded in the runnable reference repo: [`spx-examples`](https://github.com/HammerHeads-Engineers/spx-examples).

## Common Use Cases

### 1. Validate a device driver against virtual hardware

1. Pick a template model from `spx-examples/library/domains/...` (Modbus, SCPI/ASCII, MQTT, BLE).
2. Start SPX Server via Docker Compose and expose the required protocol ports.
3. Load the model, create an Instance, and drive deterministic time from tests (MiL).
4. Use Scenarios to cover happy-path and fault modes (disconnects, delays, spikes).
5. Debug with API state + server logs; keep the workflow repeatable in CI.

### 2. Run QA smoke tests in CI (MiL)

- `docker compose up -d` → wait for `GET /health` → run `pytest` → `docker compose down`.
- Store `SPX_PRODUCT_KEY` in the CI secret store; inject it into the job environment.
- Pin versions explicitly (server image tag + Python dependencies) so tests stay reproducible.

### 3. Onboard engineers with a safe sandbox

- Start from one model + one scenario.
- Make one change (attribute, mapping, scenario override) and re-run the same tests.

See: [Use in Unit Tests (MiL)](../getting-started/use-in-unit-tests-mil.md), [Snapshots — Getting Started](../getting-started/snapshots-guide.md), [Communication Adapters](../spx-core/communications/README.md).

## Step-by-Step Walkthroughs

### End-to-end: SCPI multimeter smoke test (spx-examples)

Files used:

- Model: [`library/domains/measurement_instruments/generic/multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/measurement_instruments/generic/multimeter__scpi.yaml)
- Test: [`tests/shared/integration/scpi_multimeter_sut_example.py`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/tests/shared/integration/scpi_multimeter_sut_example.py)

This flow is a good baseline for “driver vs virtual hardware” integration testing:

1. Start SPX Server and verify it’s healthy.
2. Register the model + create an instance.
3. Discover the effective ASCII/SCPI port from the instance (the model auto-assigns starting at 5025).
4. Run protocol-level assertions and scenario-driven faults.

#### Run locally

```bash
git clone https://github.com/HammerHeads-Engineers/spx-examples.git
cd spx-examples

cat <<'EOF' > .env
SPX_PRODUCT_KEY=REPLACE_ME
# SPX_BASE_URL=http://localhost:8000
EOF

poetry install --with dev
docker compose up -d
curl -fsS http://localhost:8000/health

poetry run pytest -q tests/shared/integration/scpi_multimeter_sut_example.py
```

Scenarios covered by this example (see the model YAML):

- `voltage_static`
- `ascii_disconnect`
- `ascii_response_delay_spike`
- `discharge_spike`

#### Debug checklist

```bash
docker compose ps
docker compose logs --tail=200 --no-color spx-server
```

### Scenario Blueprint Template

Use this checklist when creating scenarios for other models:

| Step | Questions | Notes |
|------|-----------|-------|
| Define intent | What user story are we simulating? | e.g. "Operator reads voltage while unplugging sensor." |
| Select assets | Which YAML model and scenarios support it? | Start with `spx-examples/library/domains/...`. |
| Identify actors | Which services or scripts will interact with the model? | REST client, SCPI CLI, Modbus master. |
| Script stimuli | Which API/protocol calls drive the scenario? | Document command sequences. |
| Expected results | What readings/logs confirm success? | Use attribute wrappers or protocol responses. |
| Fault coverage | How do we simulate edge cases? | Add scenario overrides or temporary detachments. |
| Cleanup | How do we reset the model? | Call `stop()` on scenarios or reload the model. |

### Tips for Junior Engineers / QA

- Start with one scenario and make the happy-path pass before layering faults.
- Use the `spx-examples` repo as a library; copy models into your project as needed.
- When results look odd, inspect live instance state via `spx-python` and server logs.
- Commit updates to scenarios alongside test scripts so the team reviews both.
