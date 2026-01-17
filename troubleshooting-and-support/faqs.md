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
