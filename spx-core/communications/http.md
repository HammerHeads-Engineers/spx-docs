# HTTP Adapter

The HTTP adapter exposes REST endpoints backed by your simulation. It builds on FastAPI inside the server core.

## Configuration example

{% tabs %}
{% tab title="YAML" %}
```yaml
communication:
  http_api:
    host: 0.0.0.0
    port: 8080
    base_path: "/sim"
    routes:
      get:/temperature:
        response: "#out(attributes.temperature)"
      post:/setpoint:
        body: json
        handler:
          path: system.controllers.pid.update_setpoint

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "communication": {
    "http_api": {
      "host": "0.0.0.0",
      "port": 8080,
      "base_path": "/sim",
      "routes": {
        "get:/temperature": {
          "response": "#out(attributes.temperature)"
        },
        "post:/setpoint": {
          "body": "json",
          "handler": {
            "path": "system.controllers.pid.update_setpoint"
          }
        }
      }
    }
  }
}

```
{% endtab %}
{% endtabs %}

### Key fields

- `host` / `port`: bind address and port.
- `base_path`: prefix for all routes.
- `routes`: mapping of `<method>:<path>` to handlers.
  - `response`: return an attribute or literal.
  - `handler.path`: call a method on a component or custom module.
  - `body`: decode request body (`json`, `form`, `raw`).
  - `status`: override HTTP status.

### Authentication & headers

Use `headers` to add fixed headers; integrate with server middleware for auth (`spx_server` provides plugins for API keys, tokens).

{% tabs %}
{% tab title="YAML" %}
```yaml
headers:
  Access-Control-Allow-Origin: "*"

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "headers": {
    "Access-Control-Allow-Origin": "*"
  }
}

```
{% endtab %}
{% endtabs %}

### Streaming / SSE

For high-frequency data, use MQTT or WebSockets. The HTTP adapter suits control plane operations (setpoints, snapshots, config queries).

### Scenarios

{% tabs %}
{% tab title="YAML" %}
```yaml
scenarios:
  http_503:
    duration: 5.0
    overrides:
      communication.http_api.status_override: 503

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "scenarios": {
    "http_503": {
      "duration": 5.0,
      "overrides": {
        "communication.http_api.status_override": 503
      }
    }
  }
}

```
{% endtab %}
{% endtabs %}

### Tips

- Document your API in OpenAPI format and keep YAML aligned.
- Guard handlers with diagnostics (`@guard(prefix="api.")`) to capture faults.
- Return typed JSON (numbers, booleans) to make client validation easier.
