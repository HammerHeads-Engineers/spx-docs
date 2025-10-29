---
icon: square-x
---

# Attributes

Attributes are the state variables of a simulation model. Each attribute exposes two synchronized views of its value:

- `internal_value`: the authoritative value used inside the simulation (physics, control logic, actions).
- `external_value`: the value visible to the outside world (protocol adapters, test harnesses, UI). When you set `external_value`, hooks fire and you can override the internal state temporarily.

Every attribute lives inside an `attributes` container (`SpxAttributes`). This container creates one `SpxAttribute` child per entry and gives you convenient mapping interfaces for read/write access.

## Declaring attributes

```yaml
attributes:
  temperature:
    type: float
    default: 25.0
    unit: "C"
  heater_on:
    type: bool
    default: false
  device_label: "SPX-001"        # scalar shortcut -> type inferred as string
```

JSON version:

```json
{
  "attributes": {
    "temperature": { "type": "float", "default": 25.0, "unit": "C" },
    "heater_on": { "type": "bool", "default": false },
    "device_label": "SPX-001"
  }
}
```

- `type` must be one of the supported entries in `type_mapping` (`float`, `bool`, `int`, `str`).
- `default` seeds `internal_value`. If omitted the SDK falls back to the type default.
- A scalar value is shorthand for `{type: inferred, default: value}`.
- Any extra keys (for example `unit`, custom metadata) stay on the attribute object and can be consumed later.

## Accessing values at runtime

The `SpxAttributes` container exposes two mapping-like helpers:

```python
attributes = model["attributes"]          # SpxAttributes

# Internal values drive simulation logic
current_temp = attributes.internal["temperature"]
attributes.internal["heater_on"] = True

# External values represent what the outside sees
attributes.external["temperature"] = 42.0
outgoing_label = attributes.external["device_label"]
```

These helpers delegate to each child's `internal_value` or `external_value`. Setting `external_value` triggers hooks (`on_set`, `on_external_set`). Changing `internal_value` resets the cached external override so the internal value becomes visible again.

You can work with wrappers directly:

```python
attr = attributes.get("temperature")
internal_wrapper = attr.internal      # InternalAttributeWrapper
external_wrapper = attr.external      # ExternalAttributeWrapper

internal_wrapper.set(30.0)
external_wrapper.set(28.5)
```

Wrappers are useful when you pass attribute handles into actions, hooks, or other components.

## Linking to component properties

Attributes can mirror properties or methods on a domain object (for example a hardware emulator). Use the link helpers to keep the simulation in sync with your backing implementation.

```python
power_supply = PowerSupply()
attributes = SpxAttributes(name="attributes", definition={
    "voltage": {"type": "float", "default": 12.0},
    "power_on": {"type": "bool", "default": False},
})

voltage_attr = attributes.get("voltage")
power_attr = attributes.get("power_on")

# Keep internal_value in sync with power_supply.voltage property
voltage_attr.link_to_internal_property(power_supply, "voltage")
# Expose external_value via a setter/getter pair
voltage_attr.link_to_external_func(power_supply, "get_voltage_setpoint", "set_voltage_setpoint")

# Mirror a boolean property
power_attr.link_to_internal_property(power_supply, "power_on")
```

- `link_to_internal_property(instance, property_name)` and `link_to_internal_func(instance, getter, setter)` synchronize internal values and reset external overrides.
- `link_to_external_property` and `link_to_external_func` perform the same job for the external side.
- `unlink_internal_property()` and `unlink_external_property()` break the link.

Internally the SDK wraps the target property or method in a `LinkedProperty`. Tests in `tests/test_attributes/test_spx_attribute.py` cover these flows.

## Searching and resolving attributes

When you need to look up attributes dynamically there are several helpers in `spx_sdk.attributes.resolve_attribute`:

- `is_attribute_reference(ref)`: detect `#attr(...)`, `$external(...)`, dotted paths (`instance.attr`) and return the cleaned path plus whether it is internal or external.
- `resolve_attribute_reference(instance, ref)`: resolve a reference relative to `instance` and return an internal or external wrapper.
- `resolve_attribute_reference_hierarchical(instance, ref)`: walk up the component tree until the attribute is found.
- `substitute_attribute_references_hierarchical(instance, text)`: replace all references in a string with literal values. Used by actions and conditions before calling `eval`.
- `extract_attribute_wrappers_hierarchical(instance, text)` and `substitute_with_wrappers(text, wrappers)`: collect wrappers for later substitution, handy when building custom evaluators.
- `resolve_nested_chain_reference(instance, "$( .root.subsystem.attributes.voltage.internal_value )")`: follow dotted paths starting from the system root and return a `StaticAttributeWrapper`.

Example:

```python
from spx_sdk.attributes import substitute_attribute_references_hierarchical

expr = "#attr(voltage) > 10 and #external(power_on)"
resolved = substitute_attribute_references_hierarchical(component, expr)
# resolved might become "12.0 > 10 and True"
```

## Using attribute references in definitions

Attribute references appear throughout the SDK. The prefix indicates which wrapper to use:

- `#attr(name)` or `#internal(name)`: read/write the internal value.
- `#external(name)` or `#ext(name)`: read/write the external value (what protocols see).
- `$in(...)` / `$out(...)`: historical aliases used by protocol and action builders.
- `$(.path.to.attribute)`: nested chain from the root; returns a static wrapper (see `resolve_nested_chain_reference`).

Actions, conditions, and custom components rely on these patterns. The diagnostics in `tests/test_actions/test_actions.py` and `tests/test_attributes/test_resolve_attributes.py` illustrate the end to end behaviour.

## Hooks on value changes

Each attribute can trigger hooks on specific events:

- `on_set`: fires for any change (`internal_value` or `external_value`).
- `on_internal_set`: fires only when `internal_value` changes.
- `on_external_set`: fires only when `external_value` changes.

Declare hooks just like in other components:

```yaml
attributes:
  voltage:
    type: float
    default: 12.0
    hooks:
      on_set:
        - refresh_model
        - log_change_hook
```

```json
{
  "attributes": {
    "voltage": {
      "type": "float",
      "default": 12.0,
      "hooks": {
        "on_set": [
          "refresh_model",
          "log_change_hook"
        ]
      }
    }
  }
}
```


The `Hooks` container (see the hooks chapter) registers and executes these hook components automatically.

## Best practices

- Treat `internal_value` as the simulation truth. Use `external_value` for overrides, protocol requests, and UI input. Remember that setting `internal_value` clears the external override.
- Prefer the `attributes.internal` and `attributes.external` views for quick reads and writes; drop down to wrappers only when you need persistent handles.
- Use helper functions (`is_attribute_reference`, `resolve_attribute_reference_hierarchical`) in your custom components rather than parsing references manually.
- When linking to real objects, ensure getters and setters are cheap and side-effect free; they will be called during every prepare/run cycle.
- Keep attribute expressions simple. For heavier computations consider using actions or custom components that consume attribute wrappers.
