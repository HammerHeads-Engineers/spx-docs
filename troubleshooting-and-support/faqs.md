# FAQs

## Do I need the UI to run tests?

No. The UI is optional. MiL tests should talk to SPX Server via the API (usually through `spx-python`).

## How do I keep simulations deterministic?

- Drive time explicitly from the client/test (set `instance["timer"]["time"]`, call `client.run()`).
- Avoid wall-clock sleeps for simulation behavior.
- Use Snapshots for stable starting states.

See: `getting-started/use-in-unit-tests-mil.md`, `getting-started/snapshots-guide.md`.

## Where does `SPX_PRODUCT_KEY` come from?

Retrieve it from your account at `https://simplephysx.com` and inject it as an environment variable (`SPX_PRODUCT_KEY`) for both Docker Compose and tests.

## Where do custom extensions live?

Put Python files under an extensions directory (commonly `./extensions`) that is mounted into the SPX Server container, then reload modules.

See: `getting-started/extend-with-custom-component.md`.

## What should I commit to git?

- Model YAML (and any snapshots you intentionally use as test fixtures).
- Extension code under `extensions/`.
- MiL tests (`pytest`) that validate the model behavior.

## Which Python versions are supported?

Docs and reference repos target **Python 3.9–3.12**. Use `>=3.9` unless a specific repo pins tighter constraints.

See: `overview/system-requirements-and-capability.md`.

## What is the canonical server URL / how do I change it?

- Default local base URL is `http://localhost:8000`.
- If you map the container to a different host port (for example `18000:8000`), point your client at that port.
- In examples, use `SPX_BASE_URL` to override the default base URL.

See: `getting-started/installation-guide.md`.

## How do I pin versions (server image + Python clients)?

- Pin the server image tag in `docker-compose.yml` (for example `simplephysx/spx-server:<tag>`).
- Pin `spx-python`/`spx-sdk` versions in your Python environment (`requirements.txt`/`pyproject.toml`).
- Treat `spx-examples` tags as a known-good baseline for models/tests.

See: `release-notes.md`.

## How do I validate model YAML before running it?

Two common approaches:

- If you develop in `spx-examples`, run: `python tools/validate_models.py`
- If you use the SDK directly, use the validation rules documented in: `spx-development-guide/spx-sdk/validation.md`

## What does a `422` from the API usually mean?

Most often it’s a model/definition validation failure (wrong YAML shape, missing keys, unknown classes).

Start with:

- `docker compose logs --tail=200 --no-color spx-server`
- `spx-development-guide/spx-sdk/validation.md`

## How do I run MiL tests in CI?

Use the same loop you use locally:

1. `docker compose up -d`
2. wait for `http://localhost:8000/` to respond
3. run `pytest`
4. `docker compose down`

See: `getting-started/ci-cd-setup-github-actions.md`.

## When should I use Snapshots?

Use Snapshots to:

- start tests from a known-good state without replaying long warmups,
- debug a failing test by capturing and sharing the exact state.

See: `getting-started/snapshots-guide.md`.

## How do I debug protocol adapter issues (ports, networking)?

- Confirm the adapter port is exposed on the host (`docker compose ps`).
- If the adapter talks to a host-side service, don’t use `127.0.0.1` from inside Docker; prefer `host.docker.internal` (where supported).

See: `spx-core/communications/README.md`.

## What should I include in a support request?

Follow the checklist in: `troubleshooting-and-support/how-to-get-support.md`.
