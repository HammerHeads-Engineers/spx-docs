---
icon: satellite-dish
---

# Communication

Communication components expose simulations over fieldbus protocols (Modbus, MQTT, HTTP, etc.) so real software can talk to your model.

- **SPX Server** ships production-grade protocol adapters (see [Communication Adapters](../../spx-core/communications/README.md)).
- **SPX SDK** provides the `Protocol` base class so you can implement custom transports (prototypes, test doubles, lab-only bridges).

## Declaring adapters in a model

{% tabs %}
{% tab title="YAML" %}
```yaml
attributes:
  temperature: 21.5

communication:
  - modbus_slave:
      host: 0.0.0.0
      port: 5020
      mapping:
        temperature: { address: [0, 1], group: h_r, type: float }

  - http_endpoint:
      host: 0.0.0.0
      port: 8001
      endpoints:
        "/v1/temperature":
          method: GET
          response:
            temperature: "#attr(temperature)"
```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "attributes": {
    "temperature": 21.5
  },
  "communication": [
    {
      "modbus_slave": {
        "host": "0.0.0.0",
        "port": 5020,
        "mapping": {
          "temperature": { "address": [0, 1], "group": "h_r", "type": "float" }
        }
      }
    },
    {
      "http_endpoint": {
        "host": "0.0.0.0",
        "port": 8001,
        "endpoints": {
          "/v1/temperature": {
            "method": "GET",
            "response": {
              "temperature": "#attr(temperature)"
            }
          }
        }
      }
    }
  ]
}
```
{% endtab %}
{% endtabs %}

- Each adapter entry is instantiated from the registry using its YAML key (`@register_class(name="...")`).
- Adapter schemas are defined by the server implementation and tested in `spx-server/tests/test_spx_core/test_communications/**`.
- For adapter-specific configuration, use the reference pages under [Communication Adapters](../../spx-core/communications/README.md).

## Implementing a custom protocol

Create a subclass of `Protocol`, register it, and implement the lifecycle methods you need (`prepare`, `start`, `run`, `stop`, `destroy`). Decorate the methods with `@guard(prefix="lifecycle.")` so diagnostics capture failures.

```python
from spx_sdk.communication.protocol import Protocol
from spx_sdk.registry import register_class
from spx_sdk.diagnostics import guard


@register_class(name="simple_http")
class SimpleHttpProtocol(Protocol):
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

You can instantiate your custom protocol in model YAML using the same registry key:

```yaml
communication:
  - simple_http:
      host: 127.0.0.1
      port: 8080
      base_path: /sim
```

Inside your protocol you can reach the model via `self.parent`, resolve attributes (`resolve_attribute_reference_hierarchical(self.parent, ref)`), or trigger hooks. SDK tests show how guard-wrapped lifecycle methods surface faults:
[`tests/test_communication/test_protocol.py`](https://github.com/HammerHeads-Engineers/spx-sdk/blob/main/tests/test_communication/test_protocol.py)

## Managing children and teardown

`Protocol` inherits from `SpxComponent`, so it can host nested components (for example connection pools, request handlers). The default `delete_child` implementation is defensive: it attempts to call the child's `destroy()` method and, even if that raises, it still detaches the child while emitting diagnostics. Refer to `test_delete_child_swallow_failure_but_detach` in the test suite.

Standard lifecycle methods return `True` by default. Override only what you need; the base implementation already participates in the component state machine (`prepare`, `start`, `run`, `pause`, `stop`, `reset`, `destroy`).

## SDK vs. server adapters

- **SDK goals:** quick mocks, deterministic unit tests, rapid iteration when designing a protocol mapping.
- **Server goals:** production networking, concurrency, and built-in adapters with contract tests.
- **Shared mechanism:** both rely on the same registry pattern (`@register_class(name="...")`) and the `Protocol` base.

## Best practices

- Wrap lifecycle methods with `@guard(prefix="lifecycle.", http_status=500)` so unexpected errors surface as structured `FaultEvent`s.
- Keep protocol classes thin; delegate business logic to actions, hooks, or separate services so swapping transports is easy.
- When exposing attributes, use the wrappers (`attr.internal`, `attr.external`) rather than mutating values directly; this keeps hooks and diagnostics intact.
- For tests, instantiate your protocol directly and call lifecycle methods to verify mapping behaviour without spinning up the full server stack.
