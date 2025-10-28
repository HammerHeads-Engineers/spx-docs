# Actions Module

Actions transform attribute values and push results back into the simulation. Each action is a component that reads inputs (`#attr(...)`, `#in(...)`, `#ext(...)`), performs logic, and writes to one or more outputs. Use the `actions` container inside a model to declare the steps that run every simulation tick.

## Defining actions in YAML

The `actions` container expects a list of mappings. The first key in each mapping selects the action class (for example `set`, `function`, or a custom name). The value of that key points to the target attribute(s). Additional keys configure parameters.

```yaml
actions:
  - function: "#attr(apparent_power)"
    call: "(#attr(voltage) * #attr(current))"
    params:
      alarm_threshold: 100.0

  - set:
      - "#attr(status)"
      - "#attr(alarm_active)"
    value: "RUNNING"
```

During loading the SDK turns this into action components named `function` and `set`. If you reuse the same action name multiple times, the container suffices by appending counters (`set_1`, `set_2`).

Attribute references accept prefixes `#attr`, `#internal`, `#external`, `#in`, `#out`, or `#ext` (aliases for the same wrappers). The hash `#` marker is optional; `$` or `@` also work, but `#` keeps YAML tidy.

## The actions container

Class: `spx_sdk.actions.actions.Actions`

- Registered as `actions` / `Actions` so you can embed it anywhere a container is allowed.
- Validates the list structure via `@definition_schema`, catching typos like integers in place of mappings (`tests/test_actions/test_actions_validation.py`).
- Automatically instantiates subclasses of `Action` registered in the component registry; if no specific class is registered for a name the base `Action` type is used.
- Creates unique child names per action (`dup`, `dup_1`, ...) and preserves the original mapping as `action.definition`.

### JSON equivalent

```json
{
  "actions": [
    {
      "function": "#attr(apparent_power)",
      "call": "(#attr(voltage) * #attr(current))",
      "params": {
        "alarm_threshold": 100.0
      }
    },
    {
      "set": [
        "#attr(status)",
        "#attr(alarm_active)"
      ],
      "value": "RUNNING"
    }
  ]
}
```

## Built-in `set` action

Class: `spx_sdk.actions.set_action.SetAction`

Use `set` to assign a literal value to one or more attributes. The schema enforces the presence of `set` and `value`.

```yaml
actions:
  - set: "#attr(transfer_in_progress)"
    value: 1

  - set:
      - "#attr(status)"
      - "#attr(display_message)"
    value: "Calibrating"
```

```json
{
  "actions": [
    { "set": "#attr(transfer_in_progress)", "value": 1 },
    {
      "set": [
        "#attr(status)",
        "#attr(display_message)"
      ],
      "value": "Calibrating"
    }
  ]
}
```

Behaviour highlights:

- `SetAction.run()` writes the literal to every resolved output wrapper; if any `set()` call fails, diagnostics raise a `SpxFault` with `action="actions.set.output"` (`tests/test_actions/test_set_action.py`).
- Definitions can move the literal into a `params` block (`value` is lifted automatically).

## Built-in `function` action

Class: `spx_sdk.actions.function_action.FunctionAction`

`function` evaluates an expression and writes the result to the configured outputs. The `call` string is executed with Python's `eval`, so stick to safe expressions and control inputs through the registry.

```yaml
actions:
  - function: "#attr(apparent_power)"
    call: "#attr(voltage) * #attr(current)"

  - function:
      - "#attr(active_power)"
      - "#attr(standby_power)"
    call: "max(#attr(power_draw) - idle_offset, 0)"
    params:
      idle_offset: 15.0
```

```json
{
  "actions": [
    {
      "function": "#attr(apparent_power)",
      "call": "#attr(voltage) * #attr(current)"
    },
    {
      "function": [
        "#attr(active_power)",
        "#attr(standby_power)"
      ],
      "call": "max(#attr(power_draw) - idle_offset, 0)",
      "params": { "idle_offset": 15.0 }
    }
  ]
}
```

Features covered by `tests/test_actions/test_function_action.py`:

- Supports multiple outputs (same result written to each).
- `params` entries become resolvable attributes on the action, so you can reference them directly in `call`.
- Attribute references inside `call` are resolved at runtime, after `prepare()` gathers wrappers.

## Base action class

Class: `spx_sdk.actions.action.Action`

- Parses the raw mapping into `function`, `output`, and parameter fields.
- Resolves outputs lazily during `_populate` and exposes them via `self.outputs`.
- `prepare()` gathers wrappers for parameters that contain attribute references; `run()` calls `apply_wrappers()` then `write_outputs(result)`.
- Custom actions can inherit from `Action` and override `_populate`, `run`, or helper methods. Remember to register the class (`@register_class(name="ramp")`) so the container uses it.

### Creating a custom action

```python
from spx_sdk.actions.action import Action
from spx_sdk.registry import register_class


@register_class(name="ramp")
class RampAction(Action):
    def run(self, *_, **__):
        self.apply_wrappers()
        start = getattr(self, "start_value", 0)
        stop = getattr(self, "stop_value", start)
        step = getattr(self, "step", 1)
        current = getattr(self, "current", start)
        current = current + step if current < stop else stop
        setattr(self, "current", current)
        return self.write_outputs(current)
```

With the registration in place you can declare:

```yaml
actions:
  - ramp: "#attr(progress)"
    start_value: 0
    stop_value: 100
    step: 5
```

## Validation workflow

- The actions container schema (`Actions`) ensures each entry is an object and the first key targets a recognised attribute reference pattern (`tests/test_actions/test_actions_validation.py`).
- `SetAction` and `FunctionAction` add their own schemas (`tests/test_actions/test_set_action_validation.py`, `tests/test_actions/test_function_action_validation.py`), so missing required keys produce `ValidationError` instances before runtime.
- Custom actions can attach `@definition_schema` and `@definition_validator` to enforce additional constraints, just like any other component.
