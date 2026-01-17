# Templates

Templates (`spx_core/system/templates.py`) let you package reusable model fragments and register them in the class registry. Other models can then reference the template by name via the `modules` or `instances` containers.

## Configuration Example

{% tabs %}
{% tab title="YAML" %}
```yaml
templates:
  multimeter:
    attributes:
      voltage: { default: 0.0 }
      current: { default: 0.0 }
    communication:
      ascii:
        port: 0
        mappings:
          "MEAS:VOLT?": "#out(voltage)"
```

{% endtab %}

{% tab title="JSON" %}
```json
{
  "templates": {
    "multimeter": {
      "attributes": {
        "voltage": { "default": 0.0 },
        "current": { "default": 0.0 }
      },
      "communication": {
        "ascii": {
          "port": 0,
          "mappings": {
            "MEAS:VOLT?": "#out(voltage)"
          }
        }
      }
    }
  }
}

```
{% endtab %}
{% endtabs %}

### What happens under the hood

- Each entry is validated against the `Model` schema using the same validation engine as the SDK.
- The template is stored in `class_registry` as `{ "class": Model, "template": <definition> }`.
- When a module references `multimeter`, the runtime clones the template definition and instantiates it as a normal model.

### Best practices

- Keep templates focused: one device or subsystem per template.
- Use parameters inside templates sparingly; prefer leaving knobs for the consuming model to set via `parameters`.
- Version templates (e.g., `multimeter_v2`) when breaking changes occur so older models remain compatible.
- Store template YAML alongside unit tests in `spx-examples/library/domains/...` and sync them into the server repo during releases.
