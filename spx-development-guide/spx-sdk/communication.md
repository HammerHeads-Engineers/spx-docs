---
icon: satellite-dish
---

# Communication

Communication components expose simulations over fieldbus protocols (Modbus, MQTT, HTTP, etc.) so real software can talk to your model. In the SDK the core abstraction is `Protocol`, a lightweight `SpxComponent` subclass that you extend for each transport. The SPX Server ships production-grade protocol adapters; the SDK version focuses on quick prototyping and test doubles.

## Declaring protocols in YAML

```yaml
communication:
  modbus_tcp:
    class: ModbusServer
    host: 127.0.0.1
    port: 5020
    mapping:
      temperature: { address: 0, group: holding, type: float }
      heater_on: { address: 10, group: coils, type: bool }

  http_api:
    class: SimpleHttp
    base_path: "/sim"
```

- `communication` sits next to `attributes`, `actions`, and other containers inside a model definition.
- Each child entry instantiates a protocol component registered under `communication` (for example `ModbusServer`, `SimpleHttp`).
- Your protocol class decides which fields it consumes (`host`, `port`, `mapping`, ...).

JSON equivalent:

```json
{
  "communication": {
    "modbus_tcp": {
      "class": "ModbusServer",
      "host": "127.0.0.1",
      "port": 5020,
      "mapping": {
        "temperature": { "address": 0, "group": "holding", "type": "float" },
        "heater_on": { "address": 10, "group": "coils", "type": "bool" }
      }
    },
    "http_api": {
      "class": "SimpleHttp",
      "base_path": "/sim"
    }
  }
}
```

## Implementing a custom protocol

Create a subclass of `Protocol`, register it, and implement the lifecycle methods you need (`prepare`, `start`, `run`, `stop`, `destroy`). Decorate the methods with `@guard(prefix="lifecycle.")` so diagnostics capture failures.

```python
from spx_sdk.communication.protocol import Protocol
from spx_sdk.registry import register_class
from spx_sdk.diagnostics import guard


@register_class(name="SimpleHttp")
class SimpleHttp(Protocol):
    def _populate(self, definition):
        super()._populate(definition)
        self.host = definition.get("host", "127.0.0.1")
        self.port = definition.get("port", 8080)
        self.base_path = definition.get("base_path", "/")

    @guard(prefix="lifecycle.")
    def start(self):
        self._server = build_app(self.base_path, model=self.parent)
        self._server.start(self.host, self.port)
        return True

    @guard(prefix="lifecycle.")
    def stop(self):
        if getattr(self, "_server", None):
            self._server.stop()
        return True
```

Inside your protocol you can reach the model via `self.parent`, resolve attributes (`self.parent["attributes"]`), or trigger hooks. Tests in `tests/test_communication/test_protocol.py` show how guard-wrapped lifecycle methods surface `SpxFault` events when something goes wrong.

## Managing children and teardown

`Protocol` inherits from `SpxComponent`, so it can host nested components (for example connection pools, request handlers). The default `delete_child` implementation is defensive: it attempts to call the child's `destroy()` method and, even if that raises, it still detaches the child while emitting diagnostics. Refer to `test_delete_child_swallow_failure_but_detach` in the test suite.

Standard lifecycle methods return `True` by default. Override only what you need; the base implementation already participates in the component state machine (`prepare`, `start`, `run`, `pause`, `stop`, `reset`, `destroy`).

## SDK vs. server adapters

- **SDK goals:** quick mocks, deterministic unit tests, rapid iteration when designing new protocol mappings.
- **Server goals:** high-performance networking, concurrency, security features, hot reload. When you ship to production, rely on the server's built-in adapters or deploy your custom adapter there.
- **Shared definitions:** the YAML/JSON schema is consistent. Anything you test locally using your SDK protocol should drop into the server configuration with identical keys. If you need server-only fields (TLS, clustering), guard them behind conditionals in your authoring tooling.

## Best practices

- Wrap lifecycle methods with `@guard(prefix="lifecycle.", http_status=500)` so unexpected errors surface as structured `FaultEvent`s.
- Keep protocol classes thin; delegate business logic to actions, hooks, or separate services so swapping transports is easy.
- When exposing attributes, use the wrappers (`attr.internal`, `attr.external`) rather than mutating values directly; this keeps hooks and diagnostics intact.
- For tests, instantiate your protocol directly and call lifecycle methods to verify mapping behaviour without spinning up the full server stack.
