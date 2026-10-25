# How to Get Support

When escalating an issue (internally or to the vendor), include enough detail to reproduce it without guesswork.

## Include this checklist

- **What you expected vs what happened** (one paragraph, include exact error text).
- **SPX Server image tag** from your `docker-compose.yml` (for example `simplephysx/spx-server:...`).
- **SPX Server logs**: `docker compose logs --tail=500 --no-color spx-server`
- **Your compose file** (or the diff from the recommended baseline).
- **Model definition(s)** and the exact steps to load them.
- **MiL test** or minimal script that reproduces the issue (preferred over screenshots).
- **Environment**: OS, Docker version, Python version, `spx-python` version.
- **Networking details** if a protocol adapter is involved (ports, host/container addresses).

## Quick minimal repro template

1. `docker compose up -d`
2. Run `pytest -k <failing_test>` or run the minimal `spx-python` script.
3. Attach the artifacts listed above.
