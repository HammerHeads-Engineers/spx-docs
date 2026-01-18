# Actions Module

Actions transform attribute values and push results back into the simulation. Each action is a component that reads inputs (for example `$in(...)`, `$attr(...)`, `$ext(...)`), performs logic, and writes to one or more outputs. Use the `actions` container inside a model to declare the steps that run every simulation tick.

## Defining actions in YAML

The `actions` container expects a list of mappings. The first key in each mapping selects the action class (for example `set`, `function`, or a custom name). The value of that key points to the target attribute(s). Additional keys configure parameters.

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - function: $in(apparent_power)
    call: $in(voltage) * $in(current)
    params:
      alarm_threshold: 100.0

  - set:
      - $in(status)
      - $in(alarm_active)
    value: "RUNNING"

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    {
      "function": "$in(apparent_power)",
      "call": "$in(voltage) * $in(current)",
      "params": {
        "alarm_threshold": 100.0
      }
    },
    {
      "set": [
        "$in(status)",
        "$in(alarm_active)"
      ],
      "value": "RUNNING"
    }
  ]
}

```
{% endtab %}
{% endtabs %}

During loading the SDK turns this into action components named `function` and `set`. If you reuse the same action name multiple times, the container suffices by appending counters (`set_1`, `set_2`).

Attribute references use the `<prefix>(<path>)` form. In actions, prefer `$in(...)` (internal value) and `$out(...)` (external value), plus `$attr(...)`/`$ext(...)` for non-attribute component paths. The SDK also understands the same prefixes with `#` or `@` markers, but `spx-examples` uses `$...` consistently.

## The actions container

Class: `spx_sdk.actions.actions.Actions`

- Registered as `actions` / `Actions` so you can embed it anywhere a container is allowed.
- Validates the list structure via `@definition_schema`, catching typos like integers in place of mappings (`tests/test_actions/test_actions_validation.py`).
- Automatically instantiates subclasses of `Action` registered in the component registry; if no specific class is registered for a name the base `Action` type is used.
- Creates unique child names per action (`dup`, `dup_1`, ...) and preserves the original mapping as `action.definition`.

Class: `spx_sdk.actions.set_action.SetAction`

Use `set` to assign a literal value to one or more attributes. The schema enforces the presence of `set` and `value`.

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - set: $in(transfer_in_progress)
    value: 1

  - set:
      - $in(status)
      - $in(display_message)
    value: "Calibrating"

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    { "set": "$in(transfer_in_progress)", "value": 1 },
    {
      "set": [
        "$in(status)",
        "$in(display_message)"
      ],
      "value": "Calibrating"
    }
  ]
}

```
{% endtab %}
{% endtabs %}

Behaviour highlights:

- `SetAction.run()` writes the literal to every resolved output wrapper; if any `set()` call fails, diagnostics raise a `SpxFault` with `action="actions.set.output"` (`tests/test_actions/test_set_action.py`).
- Definitions can move the literal into a `params` block (`value` is lifted automatically).

## Built-in `function` action

Class: `spx_sdk.actions.function_action.FunctionAction`

`function` evaluates an expression and writes the result to the configured outputs. The `call` string is executed with Python's `eval`, so stick to safe expressions and control inputs through the registry.

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - function: $in(apparent_power)
    call: $in(voltage) * $in(current)

  - function:
      - $in(active_power)
      - $in(standby_power)
    call: max($in(power_draw) - idle_offset, 0)
    params:
      idle_offset: 15.0

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    {
      "function": "$in(apparent_power)",
      "call": "$in(voltage) * $in(current)"
    },
    {
      "function": [
        "$in(active_power)",
        "$in(standby_power)"
      ],
      "call": "max($in(power_draw) - idle_offset, 0)",
      "params": { "idle_offset": 15.0 }
    }
  ]
}

```
{% endtab %}
{% endtabs %}

Features covered by `tests/test_actions/test_function_action.py`:

- Supports multiple outputs (same result written to each).
- `params` entries become resolvable attributes on the action, so you can reference them directly in `call`.
- Attribute references inside `call` are resolved at runtime, after `prepare()` gathers wrappers.

### Function `call`: imports, params, prepare_call

The `function` action in `spx-examples` relies on a few extra fields to keep expressions readable and deterministic:

- `params`: define constants, attribute references, or derived values. You can define them under `params:` or inline as top-level keys — both end up available as variables in `call`.
- `imports`: expose modules/symbols inside the expression context (string, list, or mapping of `alias: "pkg.symbol"`; no `import ...` statements in YAML).
- `prepare_call`: optional expression executed once during `prepare()` (commonly used to seed RNG or initialise cached helpers).

#### Example: imports + prepare_call (deterministic RNG)

```yaml
actions:
  - function: $out(noise_sample)
    imports: [random]
    prepare_call: random.seed(0)
    params:
      lo: 1
      hi: 10
    call: random.randint(lo, hi)
```

#### Example: imports mapping (alias + symbol import)

```yaml
actions:
  - function: $in(absolute_error)
    imports:
      fabs: "math.fabs"
    call: fabs($in(setpoint) - $in(measured))
```

#### Example: derived params + nested-chain references

Parameters can reference other params and runtime values. `call` can also be a multi-line YAML block (`|`) as long as it forms a valid Python expression.

```yaml
actions:
  - function: $in(delta_pct)
    params:
      cycle_time_s: 0.5
      dt: "$(~.timer.default_step) or $(~.polling.interval) or 0.25"
      delta_pct_value: "(cycle_time_s / max(1.0, dt)) * 100.0"
    call: delta_pct_value
```

For the canonical DSL contract used by `spx-examples`, see:

- https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md

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

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - ramp: $in(progress)
    start_value: 0
    stop_value: 100
    step: 5

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    {
      "ramp": "$in(progress)",
      "start_value": 0,
      "stop_value": 100,
      "step": 5
    }
  ]
}

```
{% endtab %}
{% endtabs %}


## Validation workflow

- The actions container schema (`Actions`) ensures each entry is an object and the first key targets a recognised attribute reference pattern (`tests/test_actions/test_actions_validation.py`).
- `SetAction` and `FunctionAction` add their own schemas (`tests/test_actions/test_set_action_validation.py`, `tests/test_actions/test_function_action_validation.py`), so missing required keys produce `ValidationError` instances before runtime.
- Custom actions can attach `@definition_schema` and `@definition_validator` to enforce additional constraints, just like any other component.

## Best practices

- Prototype new behaviour with `set` and `function` before creating custom actions; this keeps early experiments easy to debug.
- Name actions after intent (`sync_apparent_power`) so diagnostics and logs read like a story.
- Keep expressions short. If they grow complex, calculate intermediate values in attributes and reference them from actions.
- Add unit tests that load your YAML with `Model(...)` and call `run()` to confirm each action writes the expected values.
- When collaborating with QA, document parameters (for example in comments or adjacent tables) so teammates know which knobs are safe to tweak.
