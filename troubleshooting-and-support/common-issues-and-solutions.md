# Common Issues and Solutions

Use this page as a practical runbook for local development and CI.

First commands to run:

- `docker compose ps`
- `docker compose logs --tail=200 --no-color spx-server`

## `docker compose up` fails (container conflicts / compose not installed)

- **Symptom**: `docker: Error response from daemon: Conflict. The container name "/spx-server" is already in use` or `docker compose: command not found`.
- **Likely cause**: leftover containers from a previous run, or Docker Compose v2 is not installed/enabled.
- **Fix**:
  - Stop/remove old containers: `docker compose down --remove-orphans`
  - If the name is still taken: `docker rm -f spx-server`
  - Verify compose is available: `docker compose version`

## Setup wizard fails to start (`spx-setup.*` / `spx-install.*`)

- **Symptom**: the installer exits with missing Python modules or cannot find `docker`.
- **Likely cause**: Python or pip is missing, or the required modules are not installed.
- **Fix**:
  - Verify Python and pip: `python --version` and `python -m pip --version`
  - Install modules: `python -m pip install --user pyyaml colorama`
  - If you need a custom interpreter, set `PYTHON_BIN` before running the installer.

## `spx-start` fails with missing Python modules

- **Symptom**: `spx-start` reports missing `requests` or `spx_python`.
- **Likely cause**: required Python modules are not installed for the interpreter used by the script.
- **Fix**:
  - Install dependencies: `python -m pip install --user requests spx-python`
  - Set `PYTHON_BIN` to the correct interpreter and re-run `spx-start`.

## BLE adapter not running in installer bundles

- **Symptom**: BLE models fail and the start script prints `npm not available; skipping BLE adapter start`.
- **Likely cause**: Node.js and npm are missing, or the BLE adapter was not installed.
- **Fix**:
  - Install Node.js and re-run `spx-start`, or
  - Regenerate the bundle without BLE services if you do not need them.

## PowerShell scripts blocked by execution policy

- **Symptom**: Windows refuses to run `spx-install.ps1` or `spx-start.ps1`.
- **Likely cause**: PowerShell execution policy prevents running local scripts.
- **Fix**:
  - Run with `pwsh -ExecutionPolicy Bypass -File spx-install.ps1`
  - Do the same for `spx-start.ps1` if needed.

## SPX Server is not reachable on `http://localhost:8000`

- **Symptom**: browser/curl returns “connection refused” or times out.
- **Likely cause**: the container is not running, the API port is not mapped, or port `8000` is already used by another process.
- **Fix**:
  - Check container status: `docker compose ps`
  - Check logs: `docker compose logs --tail=200 --no-color spx-server`
  - If you changed the host port (e.g. `18000:8000`), point clients at the new URL:
    - set `SPX_BASE_URL=http://localhost:18000`

## API calls fail with auth errors (`401`/`403`) or tests fail early

- **Symptom**: endpoints reject requests; tests fail before any model logic runs.
- **Likely cause**: `SPX_PRODUCT_KEY` is missing/invalid.
- **Fix**:
  - Local: export `SPX_PRODUCT_KEY` (or put it in `.env` so Compose picks it up).
  - Installer bundles: update `.env` in the generated folder (it defaults to `REPLACE_ME`).
  - CI: store `SPX_PRODUCT_KEY` as a secret and inject it in the job env (see [CI/CD Setup (GitHub Actions)](../getting-started/ci-cd-setup-github-actions.md)).

## Model load fails with `422` / validation errors

- **Symptom**: loading a Model via API returns `422` (or server logs show `ValidationError` paths).
- **Likely cause**: YAML shape does not match the expected schema (missing keys, wrong list vs mapping), or the model references an unregistered custom class/action.
- **Fix**:
  - Inspect the server error details: `docker compose logs --tail=200 --no-color spx-server`
  - If you are authoring in `spx-examples`, run its validator before starting the server: `python tools/validate_models.py`
  - For SDK schema rules, see: [Validation](../spx-development-guide/spx-sdk/validation.md)

## Tests are flaky / non-deterministic

- **Symptom**: the same MiL test sometimes passes and sometimes fails.
- **Likely cause**: wall-clock sleeps, nondeterministic randomness, or background loops that advance state outside the test’s control.
- **Fix**:
  - Drive time explicitly from tests (MiL): set timer attributes (if present) and call `client.run()` in a loop.
  - Seed any RNG used by model logic during prepare-time.
  - Use Snapshots for stable starting states: [Snapshots — Getting Started](../getting-started/snapshots-guide.md)

## Custom extensions not found (“unknown action/class”)

- **Symptom**: errors like “unknown class”, “unknown action”, or import failures in logs.
- **Likely cause**: the extension file is not mounted into the container, or the registry/modules were not reloaded.
- **Fix**:
  - Ensure `./extensions` (or your chosen folder) is mounted into the server container (see [Installation Guide](../getting-started/installation-guide.md)).
  - Reload modules before creating new instances: `client.reload_modules()` (see [Extend with a Custom Component](../getting-started/extend-with-custom-component.md))
  - Inspect import errors: `docker compose logs --tail=200 --no-color spx-server`

## “Adapter can’t reach host” (Docker networking)

- **Symptom**: a protocol adapter or companion service (MQTT broker, BLE adapter, etc.) works on the host but fails from SPX running in Docker.
- **Likely cause**: `127.0.0.1` inside a container is not the host loopback.
- **Fix**:
  - Use `host.docker.internal` as the host address (where supported), or run the service inside the same compose network.
  - Ensure the service port is published on the host and the model points to it.

## Protocol port not exposed (Modbus/SCPI/MQTT/etc.)

- **Symptom**: the SUT cannot connect to the simulated device port.
- **Likely cause**: the model enables a protocol adapter, but the host port is not mapped in `docker-compose.yml`.
- **Fix**:
  - Confirm port mappings: `docker compose ps`
  - Update `ports:` in `docker-compose.yml` to expose the required ports (see [Communication Adapters](../spx-core/communications/README.md)).

## BLE simulations fail to connect to the BLE adapter

- **Symptom**: BLE models fail at startup or BLE operations time out.
- **Likely cause**: `spx-ble-adapter` is not running/reachable, or the model points at the wrong host/port.
- **Fix**:
  - Confirm the adapter is running and reachable on the configured port (default `8085` in the adapter docs).
  - Verify the model’s BLE configuration matches your deployment network (host vs container).
  - See: [BLE Adapter](../spx-core/communications/ble.md)

## CI fails intermittently (“server not ready”)

- **Symptom**: CI fails with connection errors right after `docker compose up -d`.
- **Likely cause**: tests start before the server finishes booting.
- **Fix**:
  - Add a readiness loop that polls `http://localhost:8000/` before running tests (see [CI/CD Setup (GitHub Actions)](../getting-started/ci-cd-setup-github-actions.md)).
