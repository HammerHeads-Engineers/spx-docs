# Advanced & Best Practices

The client exposes extensibility points for fault handling, custom transports, and resilient integration tests. This page distils lessons from `tests/test_client_exceptions.py`, `tests/test_transport.py`, and the regression suites in `spx-examples`.

---

## Fault handling strategy

All HTTP errors bubble up as `spx_python.client.SpxApiError`. The exception includes:

- `response` — the original `requests.Response`.
- `fault` — normalised diagnostics (`type`, `event`, `http_status`, `error`, `component`, `breadcrumbs`, …).
- `correlation_id` — extracted from the `X-Correlation-Id` header when present.

```python
from spx_python.client import SpxApiError

try:
    client["instances"]["ghost"] = "NoSuchClass"
except SpxApiError as exc:
    print("Status:", exc.fault["http_status"])
    print("Summary:", exc.fault["error"]["message"])
    print("Correlation-ID:", exc.correlation_id)
```

The transport recognises multiple shapes:

- Native SPX `{"type": "fault", ...}` payloads.
- RFC 7807 `application/problem+json` responses (including custom `extensions`).
- FastAPI defaults (`{"detail": ...}`).
- Plain-text or empty bodies.

See `tests/test_transport.py::ExtractFaultTests` for examples.

### Pretty vs. legacy messages

By default the exception message is a concise summary such as:

```
422 validation: Template 'heater': schema_violation at templates.heater.actions[0] (component=models.heater, action=upsert, cid=abc123)
```

Set `pretty_errors=False` when you prefer the legacy `"METHOD URL -> STATUS"` string (helpful for log diffing). This mirrors the check in `tests/test_transport.py::test_perform_request_raises_plain_message_when_pretty_disabled`.

### Verbose logging and fault hooks

`SpxClient(..., on_fault=callable)` receives a dictionary with the normalised fault plus request metadata before it is logged or raised. Exceptions thrown by the hook are suppressed, as proven in `tests/test_transport.py::EmitFaultEventTests`.

```python
def record_fault(payload):
    metrics.increment("spx.client_fault", tags={"status": payload["fault"]["http_status"]})

client = spx_python.init(
    address=BASE_URL,
    product_key=PRODUCT_KEY,
    on_fault=record_fault,
    client_fault_verbose=True,   # log full fault at ERROR level
)
```

Setting `client_fault_verbose=True` mirrors the behaviour of `SPX_CLIENT_FAULT_VERBOSE=1`: the full JSON payload is printed at `.error` instead of `.debug`.

---

## Custom HTTP transports

The client accepts any object exposing `request(method, url, headers=None, **kwargs)`. In unit tests you can inject FastAPI’s `TestClient` or a mock:

```python
from fastapi.testclient import TestClient as FastAPITestClient
from myapi import app

http = FastAPITestClient(app)
client = spx_python.init(address="http://testserver", product_key="token", http_client=http)
```

All transport plumbing flows through `spx_python.transport.perform_request`, giving you consistent fault handling without rewriting test code. Refer to `tests/test_client_unit.py::ClientUnitTests.test_request_merges_headers` for the way headers are assembled before delegating to `perform_request`.

---

## Working with transparent mode

Transparent mode is handy for CLI tooling or dry-run scripts that should not fail when the server is offline. Combine `transparent_mode(True)` with explicit clients when you need both behaviours in the same process:

```python
with transparent_mode(True):
    preview = spx_python.init(product_key="dummy")
    preview["models"]["draft"] = {"attributes": {"a": 1}}  # silently ignored

live = spx_python.init(product_key=REAL_TOKEN, transparent=False)
```

Remember to reset global state in fixtures (`set_global_transparent(False)`), just like `tests/test_client_unit.py::TestGlobalTransparentControls.tearDown`.

---

## Reliable integration test patterns

`spx_python.helpers` underpins the end-to-end tests in `spx-examples`. Key practices:

1. **Deterministic model updates** — use `helpers.ensure_model` or `load_model`. They fingerprint definitions (SHA-256 of the sorted JSON) so models are only re-uploaded when the file changes.
2. **Instance lifecycle orchestration** — `ensure_instance` supports `recreate=True`, attribute overrides, and idempotent `start()` calls. The helper tolerates transient errors by retrying lookups (`_fetch_instance_with_retry`).
3. **Wait utilities instead of sleeps** — `wait_for_condition`, `wait_for_attribute`, and `wait_for_state` poll with configurable intervals to reduce flakiness, as demonstrated in BLE and Modbus SUT tests under `spx-examples/tests`.
4. **Automated bootstrapping** — `bootstrap_model_instance` returns `(client, instance, model_changed)` so tests can selectively reset hardware facades when a definition changes (`test_ble_vital_signs_monitor_sut.py`).

```python
from spx_python.helpers import bootstrap_model_instance, wait_for_state

client, instance, changed = bootstrap_model_instance(
    spx_module=spx_python,
    product_key=PRODUCT_KEY,
    base_url=BASE_URL,
    model_path=Path("library/modbus/vacuum.yaml"),
    model_key="tests_modbus_vacuum",
    instance_key="tests_modbus_vacuum_inst",
)

wait_for_state(instance, {"RUNNING"}, timeout=10.0)
```

When cleaning up, follow the pattern from `tests/test_helpers.py::TestHelperIntegration.tearDown`: stop instances first, then delete them, and finally remove models. This prevents background polling threads from acting on removed models.

---

## Additional tips

- **JSON snapshots for debugging** — `str(client)` serialises the current path as formatted JSON, which is extremely useful when logging state from CI failures (`tests/test_basic_spx_python.py::test_str_method`).
- **Attribute fallbacks** — `client.get("path", default)` is safer than direct indexing when you expect optional components.
- **Concurrency considerations** — the client itself is thread-safe for read-only operations, but long-lived instances should be wrapped in application-level locks when mutating shared attributes.
- **Version checks** — access `spx_python.__version__` to pin expected behaviour when writing compatibility tests.

Keeping these practices in mind helps you reuse the SPX Python wrapper effectively across microservices, hardware simulators, and automated QA suites.
