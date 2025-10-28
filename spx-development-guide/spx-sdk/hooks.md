# Hooks Module

Hooks let you attach extra behavior (refreshing models, firing custom logic, raising alerts) whenever a component emits lifecycle events such as `on_set`, `on_run`, or `on_error`. The SDK treats hooks as child components: you describe them declaratively, and the `Hooks` container registers each hook class on the parent component.

## What is registered

- `Hooks`: a `SpxContainer` subclass that reads the `hooks:` section of a definition.
- `RefreshHook`: a built-in hook (`refresh_model`) that calls `prepare()` and `run()` on the root component, useful for recalculating derived values after an attribute change.

Both are exposed via `spx_sdk.hooks`. The container itself is decorated with `@definition_schema`, so invalid shapes are rejected early.

## Defining hooks in YAML

Each entry under `hooks` maps an event name to one or more hook classes. You can supply either a bare class name or a single-key object that includes per-hook configuration.

```yaml
attributes:
  temperature:
    default: 20.0
    hooks:
      on_set:
        - refresh_model        # reuse built-in hook
        - notifier_hook        # another custom hook, no config
      on_threshold:
        alert_hook:
          level: critical
          email: ops@example.com
```

When the SDK loads this definition, it creates hook instances under the attribute's `Hooks` container:

- `refresh_model` -> instance of `RefreshHook`
- `notifier_hook` -> instance of a user-registered class
- `alert_hook` -> instance configured with the provided payload

Hooks are stored on the parent component and triggered via `trigger_hooks(event_name, *args, **kwargs)`; tests under `tests/test_hooks/test_hooks.py` confirm each entry runs when the parent triggers the event.

## Authoring custom hooks

Create a subclass of `SpxComponent`, register it, and implement `run()`:

```python
from spx_sdk.components import SpxComponent
from spx_sdk.registry import register_class


@register_class(name="notifier_hook")
class NotifierHook(SpxComponent):
    def run(self, attribute, value, **kwargs):
        subject = f"[SPX] {attribute.name} changed"
        self.client["notifications"].send(subject=subject, payload={"value": value})
        return True
```

Use keyword arguments to accept contextual information when the parent triggers your hook (for example, the attribute object, old/new values, or custom metadata).

## Runtime integration

During `_populate`, the `Hooks` container normalises every event entry into a list, instantiates the specified classes using `create_instance`, and registers them on the parent via `parent.register_hook(event_name, hook_instance)`. Duplicate classes gain suffixes (`dummy_hook`, `dummy_hook_1`) to stay unique, as shown in `tests/test_hooks/test_hooks.py::test_duplicate_entries_named_uniquely`.

At runtime, call `component.trigger_hooks("on_update", attribute=self, value=new_value)`. Each hook's `run()` executes in order; returning `True` signals success, while raising `SpxFault` (or any exception) propagates according to your diagnostics setup.

## Validating definitions

The JSON Schema attached to `Hooks` catches malformed definitions before instantiation:

- event values must be a string, list of strings, or a single-key object `{HookClass: {...}}`,
- lists cannot contain booleans or other primitives,
- dict entries must only declare one hook class (see `tests/test_hooks/test_hooks_validation.py`).

This means user-supplied YAML that misconfigures hooks produces a structured validation error instead of a runtime crash.

## Built-in `refresh_model` hook

The included `RefreshHook` calls `prepare()` and `run()` on the root component. Use it when an attribute change should immediately recompute dependent state:

```yaml
attributes:
  weight:
    default: 0.0
    hooks:
      on_set: refresh_model
```

When `weight` changes, the hook re-prepares and re-runs the system, mirroring the behaviour covered in `tests/test_hooks/test_hooks_attributes.py`.
