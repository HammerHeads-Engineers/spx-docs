# Parameters

The `Parameters` container (`spx_core/system/parameters.py`) is the simplest way to push constant values into your model when it starts. Think of it as a batch of assignments that run during `prepare()`.

## YAML structure

{% tabs %}
{% tab title="YAML" %}
```yaml
parameters:
  attributes.voltage.default: 230.0
  attributes.mode.default: "production"
  instances.controller.parameters.gain: 1.2
```

{% endtab %}

{% tab title="JSON" %}
```json
{
  "parameters": {
    "attributes.voltage.default": 230.0,
    "attributes.mode.default": "production",
    "instances.controller.parameters.gain": 1.2
  }
}
```
{% endtab %}
{% endtabs %}

### How it works

- Each key is an attribute reference resolved via `resolve_attribute_reference_hierarchical`.
- The container sets the attribute's internal value by default.
- If the reference points at an external wrapper (`#external(...)`), the external value is updated instead.

### Validation

- The container expects a mapping; any other type raises an error.
- If a reference cannot be resolved, a `KeyError` is raised with the full component path. This usually means the attribute name changed or the instance was not loaded yet.

### Best practices

- Use environment variables for deployment-specific values by combining parameters with templates or SDK tooling: generate YAML where `default` values read from `os.environ` before shipping it to the server.
- Keep parameter entries close to the attributes they configure—long dotted paths are harder to maintain.
- Document critical parameters (e.g., safety limits) so QA knows what to tweak when running experiments.
