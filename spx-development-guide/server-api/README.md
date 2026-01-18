# Server API

SPX Server exposes a versioned REST API used by:

- `spx-python` (the Python client wrapper),
- the SPX UI,
- and any custom tooling that needs to load models, operate instances, or fetch logs.

## Defaults

- Base URL (local): `http://localhost:8000`
- API v3 base path: `/api/v3`

## References

- API reference: [API Reference](../../api-v3-reference/README.md) (OpenAPI is embedded under this chapter in the GitBook navigation)
- Python wrapper: [SPX-PYTHON](../spx-python-client-wrapper/README.md)
- Common endpoints: [System Runtime](../../spx-core/system/README.md)
