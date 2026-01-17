# Security Considerations

This page is a practical checklist for running SPX safely in dev and CI environments.

## Product key handling

- Treat `SPX_PRODUCT_KEY` as a secret.
- Do not commit it to git or bake it into images.
- Prefer `.env` locally and CI secrets in pipelines.

## Network exposure

- Do not expose the SPX Server API (`8000`) to the public internet.
- Bind protocol ports only when needed (Modbus/SCPI/MQTT/etc.) and prefer private networks/VPNs.

## Container hygiene

- Pin image tags in `docker-compose.yml` for reproducible builds.
- Keep dependencies for custom extensions explicit (`requirements.txt` next to extension code, where applicable).
