# Common Issues and Solutions

## `docker compose up` fails / container conflicts

- **Container name conflict** (for example `"/spx-server" is already in use"`): stop/remove the old container or tear down the other compose project:
  - `docker rm -f spx-server`
  - `docker compose down --remove-orphans`

## SPX Server is not reachable on `http://localhost:8000`

- Check containers: `docker compose ps`
- Check logs: `docker compose logs --tail=200 --no-color spx-server`
- Port collision: change the host mapping in `docker-compose.yml` (for example `18000:8000`).

## `SPX_PRODUCT_KEY` missing / invalid

- Local: set `SPX_PRODUCT_KEY` in your shell or `.env` file (Compose reads it automatically).
- CI: store `SPX_PRODUCT_KEY` as a secret and export it in the job environment (`getting-started/ci-cd-setup-github-actions.md`).
- Symptoms include authentication failures and tests returning 401/403/404 depending on the endpoint.

## Tests are flaky / non-deterministic

- Remove wall-clock sleeps and always drive simulated time (`instance["timer"]["time"] = ...` then `client.run()`).
- Keep `timer.dt` explicit in the model.
- Use Snapshots for stable starting conditions (`getting-started/snapshots-guide.md`).

## Custom extensions not found (“unknown action/class”)

- Ensure the `.py` file lives under a configured extensions directory mounted into the server (commonly `./extensions`).
- Reload modules before creating new instances:
  - `client.reload_modules()` (see `getting-started/extend-with-custom-component.md`)
- Check server logs for import errors and missing dependencies.

## “Adapter can’t reach host” (Docker networking)

When SPX runs in Docker but a companion service runs on the host (common for BLE):

- Use `host.docker.internal` as the host address (where supported) instead of `127.0.0.1`.
- Expose the backend port on the host and point the model configuration at it.

See: `spx-core/communications/ble.md`.

## Protocol port not exposed (Modbus/SCPI/etc.)

- If the model enables a protocol adapter, the host port must be mapped in `docker-compose.yml`.
- Confirm your `ports:` mappings and keep them aligned with the model’s configured port numbers.

See: `spx-core/communications/README.md`.
