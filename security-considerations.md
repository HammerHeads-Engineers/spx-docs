# Security Considerations

This page is a practical checklist for running SPX safely in dev and CI environments.

## Product key handling

- Treat `SPX_PRODUCT_KEY` as a secret.
- Do not commit it to git or bake it into images.
- Prefer `.env` locally and CI secrets in pipelines.

## Network exposure

- Do not expose the SPX Server API (`8000`) to the public internet.
- Bind protocol ports only when needed (Modbus/SCPI/MQTT/etc.) and prefer private networks/VPNs.

## Browser access and CORS

For browser clients (SPX UI, internal tools), configure CORS explicitly in deployment:

- `SPX_CORS_ALLOW_ORIGINS` - comma-separated allowlist (`*` allowed for permissive setups)
- `SPX_CORS_ALLOW_CREDENTIALS` - `1` or `0`
- `SPX_CORS_ALLOW_ORIGIN_REGEX` - optional regex allowlist

Notes:

- If `SPX_CORS_ALLOW_ORIGINS=*`, credentials are disabled for standards-compliant behavior.
- Prefer explicit origin allowlists in shared or production-like environments.

Example (`docker-compose.yml`):

```yaml
services:
  spx-server:
    environment:
      SPX_CORS_ALLOW_ORIGINS: "http://localhost:3000,http://127.0.0.1:3000"
      SPX_CORS_ALLOW_CREDENTIALS: "1"
      # SPX_CORS_ALLOW_ORIGIN_REGEX: "^https?://192\\.168\\.\\d+\\.\\d+(:\\d+)?$"
```

## Container hygiene

- Pin image tags in `docker-compose.yml` for reproducible builds.
- Keep dependencies for custom extensions explicit (`requirements.txt` next to extension code, where applicable).
