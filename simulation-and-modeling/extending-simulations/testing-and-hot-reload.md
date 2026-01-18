# Testing & Hot-Reload

The fastest extension loop is:

1. edit Python code under an extensions directory (for example `./extensions/`),
2. reload extensions in the running server,
3. run a MiL test (pytest) that drives time deterministically and asserts behavior.

## Minimal workflow

### 1) Start SPX Server

Use your project’s `docker-compose.yml`:

```bash
docker compose up -d
```

### 2) Reload extensions

If you use `spx-python`, reload from the configured extensions directories:

```python
import os
import spx_python

client = spx_python.init(
    address=os.environ.get("SPX_BASE_URL", "http://localhost:8000"),
    product_key=os.environ["SPX_PRODUCT_KEY"],
)

client.reload_modules()
```

See: [Extend with a Custom Component](../../getting-started/extend-with-custom-component.md).

### 3) Run MiL tests

Run the test suite that loads the model, creates an instance, steps time, and asserts outputs:

```bash
pytest
```

See: [Use in Unit Tests (MiL)](../../getting-started/use-in-unit-tests-mil.md).

## Common failure modes

- **“Unknown action / class name”**: module not in an extensions directory, or reload wasn’t called. Check server logs for import errors.
- **Changes not taking effect**: reload extensions before creating new instances (some runtimes bind classes during instance creation).
- **Non-deterministic tests**: remove wall-clock sleeps and always drive `timer.time` from the test.
