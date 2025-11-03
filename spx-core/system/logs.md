# Logs Buffer

`spx_core/system/logs.py` adds a `logs` component to every model and instance. It captures records emitted by the component’s logger into an in-memory deque so that the REST API and UI can stream diagnostics per instance without tailing external files.

## When it is created

- The `Model` loader (`model.py`) instantiates a `logs` child automatically, using the optional `model.logs` section from your YAML as configuration.
- Each model instance inherits its own `logs` child, so `/api/v3/system/logs` returns system-level output while `/api/v3/system/instances/<name>/logs` scopes to a specific instance.
- The component attaches a custom `logging.Handler` to the parent logger. It survives `stop()` so post-run faults are still captured until `destroy()`.

## Configuration example

{% tabs %}
{% tab title="YAML" %}
```yaml
model:
  name: ble_demo
  logs:
    max_entries: 2000         # retain 2k most recent entries
    level: DEBUG              # capture everything at DEBUG or higher
    format: "%(asctime)s %(levelname)s %(message)s"
    datefmt: "%Y-%m-%d %H:%M:%S"
    include_exception: true
    include_stack: false
    extra_fields: ["correlation_id", "request_id"]
  # ... the rest of the model definition ...
```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "model": {
    "name": "ble_demo",
    "logs": {
      "max_entries": 2000,
      "level": "DEBUG",
      "format": "%(asctime)s %(levelname)s %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S",
      "include_exception": true,
      "include_stack": false,
      "extra_fields": [
        "correlation_id",
        "request_id"
      ]
    }
  }
}
```
{% endtab %}
{% endtabs %}

### Configuration fields

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `max_entries` / `capacity` / `size` | integer | `500` | Maximum number of records kept in memory. Older entries are evicted FIFO. |
| `level` | string or int | `INFO` | Minimum severity captured. Accepts logging names (`DEBUG`, `WARNING`, …) or numeric levels. |
| `format` | string | `%(asctime)s %(levelname)s %(name)s %(message)s` | Renderer passed to `logging.Formatter`. |
| `datefmt` / `date_format` | string | `None` | Optional date format fed to the formatter. |
| `include_exception` | boolean | `true` | Store formatted tracebacks when `exc_info` is present. |
| `include_stack` | boolean | `false` | Preserve `stack_info` for records that capture it. |
| `extra_fields` | sequence of strings | `[]` | Additional `LogRecord` attributes to persist (e.g., `correlation_id`). Non-JSON values are stringified. |

You can adjust `max_entries` at runtime via the API (`PATCH /.../logs` with `{"attr": {"max_entries": {"value": 1000}}}`) and the component resizes its internal deque without dropping the most recent entries.

## Entry schema

The `logs.tail()` API returns a list of dictionaries with the following keys:

- `id`: monotonically increasing sequence number.
- `timestamp`: Unix epoch seconds (float).
- `asctime`: UTC ISO-8601 string with millisecond precision.
- `relative_ms`: milliseconds since the logging system started.
- `level` / `levelno`: severity name and numeric value.
- `logger`: `logging.Logger` name that emitted the record.
- `thread`, `process`: human-readable thread and process names.
- `message`: plain message (`record.getMessage()`).
- `rendered`: final formatter output (includes format template).
- `exception`: formatted traceback when `include_exception` is true and the record has `exc_info`.
- `stack`: captured stack trace when `include_stack` is true.
- Custom fields listed in `extra_fields` plus common diagnostics (`correlation_id`, `component`, `path`) when present on the record.

All payloads are JSON-safe; non-serialisable values are converted to their `repr()`.

## API surface

Two public methods are exposed via the component API:

- `tail(limit=50, level=None)`: return the most recent entries up to `limit`. When `level` is provided, only entries at or above that severity are returned.
- `clear()`: wipe the buffer. Equivalent to `reset()`, but leaves the handler attached so collecting resumes immediately.

Typical REST calls:

```bash
# Fetch component metadata (current size, level, etc.)
curl -H "Authorization: Bearer …" \
     http://localhost:8000/api/v3/system/logs

# Retrieve the last 100 WARNING+ entries
curl -X POST -H "Authorization: Bearer …" \
     -H "Content-Type: application/json" \
     -d '{"kwargs": {"limit": 100, "level": "WARNING"}}' \
     http://localhost:8000/api/v3/system/logs/method/tail

# Clear instance-specific logs
curl -X POST -H "Authorization: Bearer …" \
     http://localhost:8000/api/v3/system/instances/foo_inst/logs/method/clear
```

The same interface is used by the CLI and UI panels, enabling per-instance log viewers without shell access to the host.

## Usage tips

- Set `level: DEBUG` temporarily during QA to capture verbose diagnostics, then revert to `INFO` or `WARNING` to avoid filling the buffer.
- Populate `extra_fields` with identifiers (e.g., `correlation_id`) to correlate simulator logs with API requests or external tooling.
- Combine instance-level logs with scenarios: trigger a scenario that emits warnings, then query `/logs/method/tail` inside automated tests to assert the right message appeared.
- Use `include_exception: false` when you need to keep payloads compact (for embedded dashboards) and rely on `message` + `rendered` for context.

## Testing references

Integration tests in `tests/test_spx_server/test_api_v3/test_basic_model.py` cover:

- `tail()` against the system-level component (`test_logs_component_tail`).
- Severity filtering via the `level` argument (`test_logs_component_level_filter`).
- Instance-scoped retrieval (`test_instance_logs_tail`).

Consult those tests for end-to-end examples of exercising the API through HTTP.
