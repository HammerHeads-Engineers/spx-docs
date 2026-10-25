# Modules Container

Modules (`spx_core/system/modules.py`) instantiate reusable registered components.
The RC76 container accepts a list. Each entry starts with an alias → registered
model/class name, followed by optional sibling configuration sections.

```yaml
modules:
  - power_stage: power_stage_model
  - ui_panel: ui_panel_model
    init_parameters:
      $in(k__backlight_enabled): true
```

The referenced models must be registered first. Do not put a nested `type`
object in place of the registered class name: that is a different instance
configuration shape. Repeated aliases are disambiguated with numeric suffixes.
Use `instances` for ordinary runtime device instances and `modules` for
composition supported by your model. Validate the complete assembly, not only
the individual fragments.

See [Templates](templates.md), [Instances](instances.md) and the
[model definition reference](../../simulation-and-modeling/model-definition-reference.md).
