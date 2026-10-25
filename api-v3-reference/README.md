# API v3 reference

The baseline is SPX Server **v1.0.0-rc.76**. Its hierarchy API is rooted at
`http://localhost:8000/api/v3/system`. The existing GitBook OpenAPI integration
is named `hammerheadsengineers-api`; keep this identity when importing an update.
The reproducible [OpenAPI export](openapi.json) comes from the exact server
commit recorded in `sources.json` and includes public health/version routes.

## Authentication and route shapes

Send `Authorization: Bearer <SPX_PRODUCT_KEY>` for API v3 operations. Health and
version discovery routes are public. Never put a real key in documentation or a
query string. A missing/malformed bearer token and a rejected token can produce
different 401/403 responses; inspect the status and structured diagnostics.

| Operation | Route shape |
| --- | --- |
| Inspect root | `GET /api/v3/system` |
| Inspect a node | `GET /api/v3/system/{path}` |
| Read a property | `GET /api/v3/system/{path}/attr/{name}` |
| Update a property | `PUT /api/v3/system/{path}/attr/{name}` |
| Update a node | `PUT /api/v3/system/{path}` |
| Invoke a method | `POST /api/v3/system/{path}/method/{name}` |
| Invoke a root method | `POST /api/v3/system/method/{name}` |
| Delete a node | `DELETE /api/v3/system/{path}` |

Use the schema's request bodies rather than inventing a PATCH API. Component
state/properties, children and exposed methods are distinct. For an attribute's
simulation value, descend to `instances/<id>/attributes/<attribute>` and choose
`internal_value` or `external_value` explicitly where appropriate.

The dynamic hierarchy schema describes route templates; available component
methods and payload meanings depend on the runtime tree. Inspect the node or
use the matching **spx-python 1.0.0rc3** client. See
[Code Examples](code-examples.md) and the [model reference](../simulation-and-modeling/model-definition-reference.md).

## Updating the schema

Maintainers run `scripts/export_openapi.py --server <authorized-local-server-repo>`
using the pinned server dependency environment. It reads the exact manifest
commit and imports both actual routers. Public CI validates the committed
schema and provenance without any private source access or credentials.
Import this file into the existing `hammerheadsengineers-api` specification in
GitBook, then verify its rendered operations before publication.
