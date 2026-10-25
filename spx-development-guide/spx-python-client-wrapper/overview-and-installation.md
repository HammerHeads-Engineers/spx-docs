# Overview & Installation

## What the wrapper provides

The `spx_python` package wraps the SPX Server API v3 with a lightweight, dictionary-like client (`spx_python.client.SpxClient`). Every component exposed by the server becomes a mapping:

- `client["models"]` returns a client scoped to the models container.
- `client["instances"]["demo"]["attributes"]["temperature"].internal_value` reads an attribute directly.
- Methods exposed by a component (e.g., `reset`, `start`, `run`) are invoked via attribute lookup that returns a callable proxy.

Under the hood the client normalises faults, logs correlation identifiers, and supplies helpers for preparing models and instances from YAML files.

## Installation

`spx-python` is published on the internal package index. Install it into your virtual environment:

```bash
pip install spx-python
```

The package depends on:

- `requests` for HTTP transport.
- `PyYAML` for helper routines that load YAML models.

Both are installed automatically through the package metadata.

## Initialising a client

```python
import spx_python

client = spx_python.init(
    address="http://localhost:8000",
    product_key=os.environ["SPX_PRODUCT_KEY"],
)

# Read an attribute
temperature = client["instances"]["sensor"]["attributes"]["temperature"].internal_value

# Update an attribute
client["instances"]["sensor"]["attributes"]["setpoint"].internal_value = 37.5
```

`spx_python.init` wraps `spx_python.client.SpxClient` and accepts the same keyword arguments (for example a custom `http_client` for FastAPI’s `TestClient`, or `on_fault` hooks described in the advanced guide).

## Configuration toggles

Several behaviours can be controlled globally through environment variables or helper functions:

| Toggle | Env var | Helper | Purpose |
| --- | --- | --- | --- |
| Transparent mode | `SPX_TRANSPARENT` | `spx_python.set_global_transparent`, `spx_python.transparent_mode` | When enabled, newly created clients return no-ops instead of performing HTTP calls. Useful for dry-runs or unit tests without a live server. |
| Pretty error summaries | `SPX_PRETTY_ERRORS` | `spx_python.client.SpxClient(pretty_errors=...)` | Controls whether faults raise compact human-readable messages. Defaults to `True`. |
| Verbose fault logging | `SPX_CLIENT_FAULT_VERBOSE` | `spx_python.client.SpxClient(client_fault_verbose=...)` | When enabled, the client logs the full fault payload at error level (in addition to debug). Defaults to `False`. |

Example: make every client constructed inside a block transparent.

```python
from spx_python import transparent_mode, init

with transparent_mode(True):
    dry_run = init(product_key="dummy")
    assert not dry_run["instances"]  # returns another transparent client
```

You can still override the behaviour per client by passing explicit keyword arguments to `spx_python.init` or directly to `SpxClient`.

## Module layout

The package is split into focused modules:

- `spx_python.client` — the dictionary-like wrapper and error type (`SpxApiError`).
- `spx_python.transport` — HTTP helpers, fault normalisation, logging.
- `spx_python.faults` — shared formatting utilities for diagnostics.
- `spx_python.helpers` — high-level helpers used across the `spx-examples` regression tests (model loading, instance lifecycle, polling utilities).

The following pages break these modules down with examples and integration tips.
