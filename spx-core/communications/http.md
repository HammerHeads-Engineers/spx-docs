# HTTP endpoint adapter

**YAML key:** `http_endpoint` (from `spx-server/spx_core/communications/http/http_endpoint.py`)

Expose deterministic HTTP endpoints backed by attributes. Endpoints are served by FastAPI/uvicorn inside SPX Server.

## Minimal configuration

This example is taken from `spx-examples`:
[`library/domains/iot/generic/air_quality_station__http.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/air_quality_station__http.yaml)

```yaml
communication:
  - http_endpoint:
      host: 0.0.0.0
      port: 8092
      response_delay: 0.0
      response_jitter: 0.0
      endpoints:
        "/v1/air-quality/{profile}":
          method: GET
          alias:
            - "#attr(active_profile) = #param(profile)"
          response:
            profile: "#attr(active_profile)"
            current:
              timestamp: "#attr(current_timestamp)"
              pm2_5: "#attr(current_pm2_5)"

        "/simulator/profile":
          method: POST
          alias:
            - "#attr(active_profile) = #param(__body__.profile)"
          response:
            status: "ok"
            active_profile: "#attr(active_profile)"
```

## Schema (what SPX Server actually supports)

Top-level fields under `http_endpoint`:

- `host` (default: `0.0.0.0`)
- `port` (default: `8001`)
- `response_delay` / `response_jitter` (seconds; defaults: `0.0`)
- `endpoints`: mapping or list of endpoints

Per-endpoint fields:

- `path`: required when `endpoints` is a list (when `endpoints` is a mapping, the key is the path)
- `method` (or `type`): HTTP method(s). Accepts a string (`GET`) or a list (`[GET, POST]`). Default: `GET`.
- `status_code`: success status code (default: `200`)
- `alias`: optional list of assignments executed before rendering the response, for example:
  - `"#attr(setpoint) = #param(__body__.setpoint)"`
- `response`: any YAML structure. Strings may reference:
  - `#attr(name)` — an attribute value
  - `#param(name)` — a path/body parameter (see below)
- `http_code`: optional conditions that raise non-2xx codes (see server tests for the exact syntax).

## Path params and request body

- Path parameters come from `{param}` segments in the path (for example `{profile}`).
- For `POST`/`PUT`/`PATCH`, SPX parses JSON (or falls back to raw text) and exposes it as `__body__`.
  - Example: `#param(__body__.profile)` reads `{"profile": "..."}`.

## Contract (tests)

- `spx-server/tests/test_spx_core/test_communications/test_http/test_http_endpoint.py`
- `spx-server/tests/test_spx_core/test_communications/test_http/test_open_meteo_static_model.py`
