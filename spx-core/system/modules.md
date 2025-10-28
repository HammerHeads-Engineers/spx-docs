# Modules Container

Modules (`spx_core/system/modules.py`) let you include reusable subsystems that were registered as templates. They are similar to instances, but they focus on higher-level building blocks—entire machines, test rigs, or collections of actions/conditions.

## YAML structure

```yaml
modules:
  - power_stage: library/power_stage
  - ui_panel:
      library/ui_panel
      actions:
        - override:
            target: "#attr(backlight)"
            value: 1
```

### Configuration options

| Pattern | Meaning |
|---------|---------|
| `- alias: template_name` | Creates a child using the registered template. |
| `actions`, `conditions`, etc. | Optional sections merged into the module after instantiation. |

### How it works

- The container looks up each template in the class registry (`class_registry[template_name]["template"]`).
- It materializes the module under the provided alias (`power_stage`, `ui_panel`, ...).
- Additional sections (actions, conditions, communication) in the mapping are attached to the new module so you can specialize it without editing the base template.

### Use cases

- **Shared hardware**: Build a `library/scpi_multimeter.yaml` template, then include it wherever a project needs that instrument.
- **Customer-specific variants**: Override only what changes (setpoints, labels, protocols) while keeping the base module unchanged.

### Tips

- Keep templates small and composable; use modules to assemble them into full systems.
- Name modules by role (`power_stage`, `ui_panel`) rather than device type to make diagnostics easier to read.
- Validate templates with the SDK before publishing them to the core—both use the same validation pipeline.
