# Protocol Adapters

Extending SPX with a new protocol adapter lets you bridge simulations to bespoke transports—legacy serial buses, proprietary gateways, or vendor-specific SDKs. This guide distils common patterns from the built-in adapters (`ascii`, `http_endpoint`, `modbus_tcp`, `mqtt`, `ble`) so you can author your own protocol component with minimal guesswork.

---

## Anatomy of a protocol component

Every adapter is a subclass of `spx_sdk.communication.protocol.Protocol` and registered with the SDK so YAML definitions can instantiate it:

```python
from spx_sdk.communication.protocol import Protocol
from spx_sdk.registry import register_class

@register_class(name="my_transport")
class MyTransport(Protocol):
    def _populate(self, definition: dict):
        super()._populate(definition)
        # Parse configuration, allocate state, validate inputs

    def prepare(self, *args, **kwargs) -> bool:
        # Establish connections, warm up caches
        return super().prepare(*args, **kwargs)

    def run(self, *args, **kwargs) -> bool:
        # Perform a single tick (poll remote, push outbound data)
        return super().run(*args, **kwargs)

    def stop(self, *args, **kwargs) -> bool:
        # Stop background workers, close sockets
        return super().stop(*args, **kwargs)
```

Key responsibilities:

- **Configuration parsing** in `_populate` – validate user input and provide sensible defaults.
- **Lifecycle control** – implement `prepare/start/run/stop/detach/attach/release` as needed to manage resources cleanly. See the Modbus and HTTP adapters for reference.
- **Attribute binding** – wire SPX attributes to protocol data structures (topics, registers, BLE state) using helper functions in `spx_sdk.attributes`.
- **Threading and IO** – background threads (`mqtt`, `ble`), event loops (`http_endpoint`), or socket servers (`ascii`) keep traffic flowing.
- **Status reporting** – expose a `status` property (typically an enum) so operators can inspect health via the API/UI.

---

## Designing the configuration schema

Aim for a declarative shape that mirrors the target protocol. Borrow ideas from:

- `mqtt`: `broker`, credentials, QoS, unified `bindings` section with direction.
- `http_endpoint`: route definitions with delay/jitter knobs.
- `ble`: nested `adapter`, `device`, `codecs`, `services`, `bindings`.

Checklist:

1. Define required keys and raise `ValueError` early when they are missing.
2. Surface optional tuning knobs (timeouts, jitter, polling interval) with defaults.
3. Support environment overrides for secrets (see `mqtt`’s `env_username_var` / `env_password_var`).
4. When migrating from older schemas, provide compatibility shims (e.g., MQTT’s legacy `publishers/subscribers` conversion).

Example `_populate` fragment:

```python
def _populate(self, definition: Optional[dict]):
    config = dict(definition or {})

    adapter_cfg = config.get("adapter") or {}
    self.host = adapter_cfg.get("host", "127.0.0.1")
    self.port = int(adapter_cfg.get("port", 9000))
    self.timeout = float(adapter_cfg.get("timeout", 2.0))

    bindings_cfg = config.get("bindings") or []
    if not bindings_cfg:
        raise ValueError("my_transport requires at least one binding")

    self._bindings = [self._build_binding(entry) for entry in bindings_cfg]
    super()._populate(config)
```

---

## Attribute binding patterns

Most adapters maintain a bridge between SPX attribute references and protocol-specific payloads:

- **Resolve references** with `resolve_attribute_reference_hierarchical(self.parent, ref)` to support `$in(...)`, `$out(...)`, or `#attr(...)`.
- **Encapsulate the binding** in small classes (`Binding` in BLE, `SubscriptionBinding` / `PublicationBinding` in MQTT).
- **Track last values** to suppress redundant updates (`_value_changed` logic in BLE).
- **Provide codecs or conversion hooks** where necessary (string encode/decode, register packing).

Sample binding builder:

```python
from dataclasses import dataclass

@dataclass
class Binding:
    topic: str
    attribute: Any
    direction: str  # "publish", "subscribe", "both"

def _build_binding(self, entry: dict) -> Binding:
    topic = entry.get("topic")
    ref = entry.get("attribute")
    if not topic or not ref:
        raise ValueError("Binding requires 'topic' and 'attribute'")
    attr_wrapper = resolve_attribute_reference_hierarchical(self.parent, ref)
    if attr_wrapper is None:
        raise ValueError(f"Cannot resolve attribute reference {ref!r}")
    return Binding(topic=topic, attribute=attr_wrapper, direction=entry.get("direction", "both"))
```

Use these bindings inside your worker loop to push/pull data reliably.

---

## Lifecycle management blueprint

Each protocol aligns with the same lifecycle contract:

1. **prepare()** — one-time setup, allocate sessions, load configs. Do not start threads here.
2. **start()** — launch background workers (threads, asyncio servers). Guard against double start.
3. **run()** — optional per-tick hook for polling-style adapters (BLE, MQTT) when SPX runs in deterministic steps.
4. **stop()** — terminate workers and close connections.
5. **detach()/attach()** — optional; typically used to temporarily pause the adapter while keeping state intact (HTTP, BLE).
6. **release()/destroy()** — final clean-up invoked when the component is removed.

Mirror the defensive coding seen in `http_endpoint` and `modbus_tcp`: always handle repeated calls, and log failures with enough context to debug (host, port, broker address).

---

## Example: WebSocket echo protocol (conceptual)

Below is a minimal skeleton that broadcasts attribute changes over WebSockets and forwards inbound messages to SPX attributes. It demonstrates the concepts above without diving into transport specifics.

```python
# All comments in English only.
import asyncio
import json
import threading
from dataclasses import dataclass
from typing import Any, Optional

import websockets
from spx_sdk.communication.protocol import Protocol
from spx_sdk.registry import register_class
from spx_sdk.attributes.resolve_attribute import resolve_attribute_reference_hierarchical


@dataclass
class WsBinding:
    topic: str
    attribute: Any
    direction: str  # publish / subscribe / both


@register_class(name="websocket_bus")
class WebSocketBus(Protocol):
    def _populate(self, definition: Optional[dict]):
        cfg = dict(definition or {})
        self.host = cfg.get("host", "0.0.0.0")
        self.port = int(cfg.get("port", 8765))
        self.poll_interval = float(cfg.get("poll_interval", 0.1))

        bindings_cfg = cfg.get("bindings", [])
        if not bindings_cfg:
            raise ValueError("websocket_bus requires at least one binding")

        self._bindings: list[WsBinding] = []
        for item in bindings_cfg:
            attr = resolve_attribute_reference_hierarchical(self.parent, item.get("attribute"))
            if attr is None:
                raise ValueError(f"Cannot resolve attribute {item.get('attribute')!r}")
            binding = WsBinding(
                topic=item.get("topic", ""),
                attribute=attr,
                direction=item.get("direction", "both"),
            )
            self._bindings.append(binding)

        self._clients: set[websockets.WebSocketServerProtocol] = set()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        super()._populate(cfg)

    def prepare(self, *args, **kwargs) -> bool:
        if self._loop is None:
            self._loop = asyncio.new_event_loop()
        return super().prepare(*args, **kwargs)

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        def _runner():
            asyncio.set_event_loop(self._loop)
            server_coro = websockets.serve(self._handle_client, self.host, self.port)
            self._loop.run_until_complete(server_coro)
            self.logger.info("WebSocket bus listening on %s:%s", self.host, self.port)
            self._loop.run_forever()

        self._thread = threading.Thread(target=_runner, daemon=True)
        self._thread.start()
        super().start()

    def stop(self) -> bool:
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join(timeout=2.0)
        return super().stop()

    async def _handle_client(self, websocket, path):
        self._clients.add(websocket)
        try:
            async for message in websocket:
                payload = json.loads(message)
                self._apply_inbound(payload)
        finally:
            self._clients.discard(websocket)

    def _apply_inbound(self, payload: dict) -> None:
        topic = payload.get("topic")
        value = payload.get("value")
        for binding in self._bindings:
            if binding.direction in {"subscribe", "both"} and binding.topic == topic:
                if hasattr(binding.attribute, "internal_value"):
                    binding.attribute.internal_value = value
                elif hasattr(binding.attribute, "set"):
                    binding.attribute.set(value)

    def run(self, *args, **kwargs) -> bool:
        self._publish_outbound()
        return super().run(*args, **kwargs)

    def _publish_outbound(self) -> None:
        payloads = []
        for binding in self._bindings:
            if binding.direction in {"publish", "both"}:
                val = getattr(binding.attribute, "external_value", binding.attribute.internal_value)
                payloads.append({"topic": binding.topic, "value": val})
        if payloads and self._clients:
            message = json.dumps(payloads)
            for client in list(self._clients):
                asyncio.run_coroutine_threadsafe(client.send(message), self._loop)
```

This skeleton focuses on structure: configuration parsing, attribute resolution, lifecycle management, and the `run()` method pushing outbound updates. Replace the transport internals with your own library calls.

---

## Integrating the protocol in YAML

Once registered, the protocol becomes available under `communication:` in your model definitions:

```yaml
imports:
  - extensions.protocols.websocket_bus

communication:
  - websocket_bus:
      host: 0.0.0.0
      port: 8765
      bindings:
        - topic: "sensor/temperature"
          attribute: $out(attributes.temperature)
          direction: publish
        - topic: "controller/setpoint"
          attribute: $in(attributes.setpoint)
          direction: subscribe
```

The SPX loader instantiates the protocol component alongside other communication blocks, and the lifecycle control (prepare/start/run/stop) is driven automatically.

---

## Testing and validation

1. **Unit tests** – isolate helper functions (binding builders, codecs) and use dependency injection for networking pieces. The ASCII and MQTT modules include pure-python tests for message parsing.
2. **Integration tests** – use `spx_python.init` plus helper utilities (`wait_for_attribute`, `ensure_instance`) to run end-to-end scenarios. Mirror the approach in `spx-examples/tests/*` to validate bidirectional flows.
3. **Deterministic runs** – when possible, expose deterministic modes (e.g., disable polling jitter) so CI tests are stable.
4. **Fault observability** – log errors with context (host, port, topic, correlation IDs) and expose counters through the protocol component’s state so operators can inspect issues via `/api/v3/system`.

---

## Best practices checklist

- Keep the adapter self-contained: configuration parsing, lifecycle, and bindings should live in one module.
- Guard against partial configuration by raising informative `ValueError`/`RuntimeError` during `_populate` or `prepare`.
- Clean up all resources in `stop()`/`release()` to avoid zombie threads or lingering sockets.
- Consider exposing metrics attributes (counters, status enums) so dashboards can track connectivity.
- Document the YAML schema inline and in the docs (see `spx-core/communications/ble.md` for a comprehensive example).

Following these conventions will ensure your custom protocol behaves like a first-class citizen alongside the built-in adapters. Once the module is importable, users can combine it with other communication blocks, scenarios, and automation tooling without additional integration work.
