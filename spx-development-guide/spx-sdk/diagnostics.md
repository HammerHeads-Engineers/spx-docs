# Diagnostics Module

The diagnostics helpers catch failures in SPX components, turn them into rich `FaultEvent` objects, and emit structured logs without forcing you to wire your own error plumbing. Use them whenever a component touches unpredictable inputs (fieldbus traffic, file IO, third-party SDKs) or when you want reproducible breadcrumbs in support tickets.

## Core building blocks

- `guard(...)`: decorator for synchronous or asynchronous component methods. It wraps the body, catches exceptions, enriches them with component metadata, and either re-raises a `SpxFault` or swallows after emitting the event.
- `trace(...)`: context manager for inner blocks that deserve their own breadcrumb (e.g., a Modbus request or PLC command).
- `call(...)`: helper when you cannot use a decorator but still want guard-like behaviour around an arbitrary callable.
- `autoguard_lifecycle(cls, ...)`: bulk-wraps lifecycle methods (`prepare`, `start`, `run`, ...) on your component subclass.
- `SpxFault`: exception subclass that stores event/action labels, severity, HTTP status codes, breadcrumbs, and the original stack trace. Calling `.to_event()` converts it into a serialisable `FaultEvent`.
- `diagnostics.bus.publish(event)`: default publisher that logs JSON to the `spx.diagnostics` logger; you can monkey-patch it with your own transport.
- `diagnostics.context`: correlation-ID helpers (`use_correlation_id`, `wrap_with_correlation`, `CorrelationFilter`) so logs and HTTP responses share the same request identifier.

## Guarding a component method

```python
from spx_sdk.components import SpxComponent
from spx_sdk.diagnostics import guard, trace, SpxFault, FaultSeverity


class HeaterDriver(SpxComponent):
    @guard(prefix="heater.", http_status=503)
    def start(self) -> None:
        # Bubble SpxFault to surface a 503 upstream, but swallow transient network noise.
        with trace(self, action="heater.connect", bubble=False, severity=FaultSeverity.WARN):
            self._bus.open()                     # emits WARN breadcrumb on failure, continues

        with trace(self, action="heater.self_test"):
            ok = self._run_self_test()           # crash => raises SpxFault(ERROR, bubble=True)
            if not ok:
                raise SpxFault(
                    event="self_test_failed",
                    action="heater.self_test",
                    component=self,
                    severity=FaultSeverity.ERROR,
                    extra={"last_result": ok},
                    http_status=422,
                )

    def _run_self_test(self) -> bool:
        ...
```

What you get out of the box:

- The `start()` decorator emits `lifecycle` breadcrumbs and sets `action="heater.start"` automatically.
- If `_bus.open()` raises anything, the `trace` block adds a breadcrumb, emits a warning event, and suppresses the exception so the component can decide what to do next.
- Any other exception bubbles as `SpxFault` with `event="operation_failed"` and a JSON serialisation available via `.to_event().to_dict()`.
- HTTP handlers (e.g., FastAPI routes) can catch `SpxFault`, call `.to_event()`, and return a 4xx/5xx payload using the stored `http_status`.

## Auto-guard lifecycle hooks

Manually decorating every lifecycle method is repetitive. Call `autoguard_lifecycle()` once in your subclass definition:

```python
from spx_sdk.components import SpxComponent
from spx_sdk.diagnostics import autoguard_lifecycle


class Mixer(SpxComponent):
    def prepare(self): ...
    async def start(self): ...
    def run(self): ...


autoguard_lifecycle(Mixer, prefix="mixer.", methods=("prepare", "start", "run"))
```

Each listed method is wrapped exactly once; rerunning the helper is idempotent thanks to the internal `_spx_guard_wrapped` marker.

## Correlation IDs in practice

Attach request IDs to diagnostics so back-end logs, API responses, and client bug reports line up:

```python
from fastapi import FastAPI
from spx_sdk.diagnostics import guard
from spx_sdk.diagnostics.context import use_correlation_id, wrap_with_correlation, CorrelationFilter

api = FastAPI()

@api.middleware("http")
async def add_correlation_id(request, call_next):
    header = request.headers.get("X-Correlation-ID")
    with use_correlation_id(header, generate_if_missing=True) as cid:
        response = await call_next(request)
        if cid:
            response.headers["X-Correlation-ID"] = cid
        return response

@api.get("/mixers/{uid}")
@guard("api.get_mixer", http_status=500)
def get_mixer(uid: str):
    # Any guard/trace invoked later reuses the same correlation id.
    ...
```

For background tasks spawned from a request, wrap callables with `wrap_with_correlation()` so they preserve the originating ID.

```python
pool.submit(wrap_with_correlation(self._refresh_cache))
```

Add `CorrelationFilter` to your logging handlers to inject `%(correlation_id)s` into each log line.

## Emitting events elsewhere

By default, events are logged as `FAULT { ...json... }`. To forward them to another system (DataDog, OTLP, MQTT), replace the publisher early in your service bootstrap:

```python
from spx_sdk.diagnostics import bus

def publish(event):
    payload = event.to_dict()
    exporter.send(payload)          # push to your telemetry pipeline

bus.publish = publish              # monkey-patch the module-level function
```

Because guards import `diagnostics.bus` lazily, your override is picked up automatically.

## Working with FaultEvent payloads

`SpxFault.to_event()` returns a `FaultEvent` instance while `diagnostics.bus.publish()` receives the same object. Useful fields:

- `severity`: `FaultSeverity.ERROR/WARN/INFO`
- `when`: UTC ISO timestamp
- `breadcrumbs`: list of `{when, component, path, action}` entries accumulated by guards and traces
- `component`: captures `name`, `path`, `state`, `uid` (when available)
- `error`: nested structure with exception type, message, Python traceback, and chained causes
- `extra`: free-form dict for domain-specific metadata

Serialise with `.to_dict()` or `.to_headpoint()` depending on your downstream consumer.

When you raise your own `SpxFault`, favour `raise SpxFault.from_exc(exc, ...)` (available via `SpxFault.from_exc`) to retain the original exception as `__cause__`. Guards will enrich and optionally emit the event without losing the stack trace.
