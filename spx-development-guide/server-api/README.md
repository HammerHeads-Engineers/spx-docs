# Server API

SPX Server exposes a versioned REST API used by:

- `spx-python` (the Python client wrapper),
- the SPX UI,
- and any custom tooling that needs to load models, operate instances, or fetch logs.

## Defaults

- Base URL (local): `http://localhost:8000`
- API v3 base path: `/api/v3`

## Authentication

- API v3 uses Bearer authentication (`Authorization: Bearer <SPX_PRODUCT_KEY>`).
- OpenAPI defines this as a global `bearerAuth` security scheme.
- Calls without a valid bearer token return authorization errors (typically `401`/`403`).

## Root endpoint payload

`GET /` includes runtime/license metadata such as:

- `plan`
- `expiration_date`
- `license_user`

## References

- API reference: [API Reference](../../api-v3-reference/README.md) (OpenAPI is embedded under this chapter in the GitBook navigation)
- Python wrapper: [SPX-PYTHON](../spx-python-client-wrapper/README.md)
- Common endpoints: [System Runtime](../../spx-core/system/README.md)
