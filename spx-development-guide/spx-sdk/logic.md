icon: list-tree
---

# Logic

The logic module wires declarative conditions into simulations. It lets you describe `if/else` style control flow that watches attribute values and triggers actions or entire subtrees without writing Python code.

## Building blocks

- `Conditions`: container that holds a list of condition blocks. Each block evaluates a boolean expression and, when true, runs its child actions or nested containers.
- `Condition`: individual condition node registered under multiple aliases (`if`, `when`, `case`, `condition`, etc.).
- `Else`: fall-through container executed when previous conditions in the same group fail.
- `IfChain`: specialised container that evaluates conditions sequentially and stops after the first branch that succeeds.

All types are registered in the SDK registry, so you can reference them directly in YAML, JSON, or via the Python APIs.

## Declaring conditions in YAML

```yaml
conditions:
  - if: "#attr(temperature) > 80"
    actions:
      - set: "#attr(fan_state)"
        value: "HIGH"
  - elif: "#attr(temperature) > 60"
    actions:
      - set: "#attr(fan_state)"
        value: "MEDIUM"
  - else:
      actions:
        - set: "#attr(fan_state)"
          value: "LOW"
```

- Each entry in the list becomes a `Condition` (or `Else`) component.
- The first key (`if`, `elif`, `when`, etc.) carries the expression to evaluate.
- Additional keys hold child components to execute (`actions`, nested `conditions`, custom classes).

The same structure in JSON:

```json
{
  "conditions": [
    {
      "if": "#attr(temperature) > 80",
      "actions": [
        { "set": "#attr(fan_state)", "value": "HIGH" }
      ]
    },
    {
      "elif": "#attr(temperature) > 60",
      "actions": [
        { "set": "#attr(fan_state)", "value": "MEDIUM" }
      ]
    },
    {
      "else": {
        "actions": [
          { "set": "#attr(fan_state)", "value": "LOW" }
        ]
      }
    }
  ]
}
```

### Expression syntax

`Condition.evaluate()` resolves attribute references using `substitute_attribute_references_hierarchical`, then feeds the resulting string into Python's `eval`. That means you can combine arithmetic, comparisons, boolean operators, and helper functions available in scope. Keep expressions side-effect free and rely on attribute references (`#attr(name)`, `#external(name)`, `#internal(name)`) to access simulation state.

The validator normalises lowercase `true`/`false` to Python `True`/`False`, so both forms work. If the expression throws (syntax error, missing name), evaluation returns `False` and logs an error.

## Sequencing with `IfChain`

Use `if_chain` when you want an ordered list of branches where only the first matching condition should run.

```yaml
if_chain:
  - if: "#attr(mode) == 'startup'"
    actions:
      - function: "#attr(power_draw)"
        call: "min(#attr(power_draw) + 5, 100)"
  - if: "#attr(mode) == 'steady'"
    actions:
      - function: "#attr(power_draw)"
        call: "max(#attr(power_draw) - 2, 0)"
  - else:
      actions:
        - set: "#attr(power_draw)"
          value: 0
```

`IfChain.prepare()` and `IfChain.run()` walk children in order. As soon as one branch returns `True`, remaining branches are skipped (`tests/test_logic/test_conditions_condition.py::TestConditions`).

JSON form:

```json
{
  "if_chain": [
    {
      "if": "#attr(mode) == 'startup'",
      "actions": [
        { "function": "#attr(power_draw)", "call": "min(#attr(power_draw) + 5, 100)" }
      ]
    },
    {
      "if": "#attr(mode) == 'steady'",
      "actions": [
        { "function": "#attr(power_draw)", "call": "max(#attr(power_draw) - 2, 0)" }
      ]
    },
    {
      "else": {
        "actions": [
          { "set": "#attr(power_draw)", "value": 0 }
        ]
      }
    }
  ]
}
```

## Nesting logic and actions

Condition blocks are standard containers, so you can mix and match:

- Place `actions` arrays inside a condition to execute action components.
- Embed another `conditions` list for nested checks (see `tests/test_logic/test_conditions_condition.py::test_nested_complex_definition`).
- Inject custom components registered in the SDK registry (alarms, state machines, telemetry exporters).

Example with nested conditions:

```yaml
conditions:
  - if: "#attr(pressure) > 30"
    ActionA:
      foo: 1
    conditions:
      - when: "#attr(temperature) > 90"
        ActionB: { bar: 2 }
      - else:
          ActionA: { baz: 3 }
  - else:
      actions:
        - set: "#attr(alert)"
          value: 0
```

## Validation guarantees

Schemas declared via `@definition_schema` ensure definitions fail fast (`tests/test_logic/test_conditions_validation.py`):

- `conditions` entries must be objects with at least one property; the first key must map to a string.
- `if_chain` enforces array structure (`minProperties=1` per item). Non-string condition values raise validation errors.
- `Condition` expects a string (the expression). `Else` expects an object, giving you a place to insert child components.

Combine this with the validation engine to catch mistakes before runtime:

```python
from spx_sdk.validation.engine import validate_document

doc = yaml.safe_load(open("system.yaml"))
res = validate_document(doc, registry=my_registry)
if not res.ok:
    print(res.errors_summary())
```

## Best practices

- Keep expressions short and readable; extract complex maths into actions or helper attributes.
- Use `#attr(instance.attribute)` dotted paths to reference attributes across the hierarchy.
- Prefer `if_chain` to unstructured lists when only one branch should run per tick.
- Leverage diagnostics guards (for custom logic components) to capture evaluation errors.
