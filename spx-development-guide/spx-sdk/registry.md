---
icon: cabinet-filing
---

# Registry

The registry keeps track of every component, container, protocol, and helper class that the SDK can instantiate from YAML. It is the glue between declarative definitions and Python code: when a model file says `actions: - function: ...`, the registry finds the `FunctionAction` class, constructs it, and wires it into the component tree.

Two global dictionaries live in `spx_sdk.registry`:

- `class_registry`: maps names to class metadata (`{"class": SpxComponentSubclass, "base_class": "SpxComponent"}`).
- `instance_registry`: optional map of named instances (useful for factories or tooling).

## Registering classes

Use `@register_class(...)` to make a class available by name. If you omit the name, the class's `__name__` is used; you can register the same class under multiple aliases for convenience.

```python
from spx_sdk.registry import register_class
from spx_sdk.components import SpxComponent


@register_class()
class Heater(SpxComponent):
    ...

# Extra alias for YAML
@register_class(name="heater_device")
class HeaterAlias(Heater):
    pass
```

The decorator is idempotent; calling it again simply overwrites the entry. Tests in `tests/test_registry/test_register_class.py` verify default names, custom names, and decorator behavior.

## Creating instances dynamically

`create_instance(name, **kwargs)` looks up the class in `class_registry`, merges optional templates, and constructs the object. If the name is not registered it tries to import a Python class by module path (`pkg.module.Class`). All failures surface as `SpxFault` with HTTP-style status codes so you can bubble them through APIs.

```python
from spx_sdk.registry import create_instance

attr = create_instance(
    "SpxAttribute",
    name="temperature",
    parent=attributes_container,
    definition={"type": "float", "default": 22.0},
)
```

When you package custom components, simply ensure their modules run `@register_class` at import time. Then local tools (`spx-sdk` CLI, tests) can instantiate them by name.

### YAML-driven instantiation

The registry can load batches of instances from YAML:

```yaml
heater_instance:
  class: heater_device
  parameters:
    name: heater_instance
    parent: !python/object:spx_sdk.components.SpxComponent { name: "root" }
```

```json
{
  "heater_instance": {
    "class": "heater_device",
    "parameters": {
      "name": "heater_instance",
      "parent": "!python/object:spx_sdk.components.SpxComponent { name: \"root\" }"
    }
  }
}
```

Use `load_instances_from_yaml(path)` or `load_instances_from_yaml_data(yaml_string)`. Each entry must include a registered `class` plus any constructor parameters. The helper stores the created objects in `instance_registry` so you can fetch them with `get_instance("heater_instance")`.

## Discovering classes

The registry provides several lookup utilities:

- `get_class("SpxAttribute")`: return the class object or raise `SpxFault` if missing.
- `get_classes_by_base("SpxComponent")`: return a mapping of names to classes that inherit from the given base anywhere in the MRO (see `tests/test_registry/test_registry_functions.py`).
- `get_class_names_by_base("SpxContainer")`: return only the names (cheap when you generate menus or documentation).

These queries power features such as auto-discovering all registered actions for documentation generation or UI pickers.

## Loading modules automatically

When you point the SDK at a library directory, use:

- `load_modules_from_directory(path, skip_pattern="*test*")`: load top-level modules.
- `load_modules_recursively(path)`: walk the tree and import each `.py` file, skipping test files by default.

Both helpers add directories to `sys.path`, import modules, and trigger any `@register_class` calls inside. Errors convert to `SpxFault` with context about the failing file (`tests/test_registry/test_registry_functions.py::test_load_modules_from_directory` covers happy paths).

To satisfy dependencies declared beside your modules, call `install_requirements_from_dir(path)`. It searches for files matching `requirements*.txt` and runs `pip install`. Use this sparingly in automation; prefer preinstalling dependencies for reproducible builds.

## Working with templates

Registry entries can include a `template` dict. When you call `create_instance`, the template is shallow-merged with the caller's `definition`. This is handy for reusable component blueprints:

```python
from spx_sdk.registry import class_registry, register_class
from spx_sdk.components import SpxComponent


@register_class(name="DefaultSensor")
class Sensor(SpxComponent):
    ...

class_registry["DefaultSensor"]["template"] = {
    "attributes": {"value": {"type": "float", "default": 0.0}},
}
```

Now `create_instance("DefaultSensor", definition={"attributes": {"value": {"default": 25.0}}})` inherits the template but lets callers override individual fields.

## Managing instances

If you create objects manually and want to expose them by name:

```python
from spx_sdk.registry import instance_registry

instance_registry["heater"] = heater_component
```

Later you can retrieve or filter them:

- `get_instance("heater")`
- `get_all_instances()`
- `filter_instances_by_base_class(SpxComponent)` or `filter_instances_by_base_class_name("Protocol")`

These helpers underpin the validation engine and CLI tools that need to inspect the running component tree.

## Clearing and resetting

In tests you often start with a clean registry:

```python
from spx_sdk.registry import clear_registry

clear_registry()
```

This wipes both class and instance registries. Most unit tests in `tests/test_registry` call it in `setUp()` to avoid leakage between cases.

## Error handling via `SpxFault`

Every registry failure funnels through `SpxFault.from_exc(...)`, attaching an `event`, `action`, severity, and optional HTTP status. When you build APIs on top of the SDK, catch `SpxFault` and serialize `fault.to_event().to_dict()` to clients for consistent diagnostics.

## Best practices

- Register classes at import time; avoid lazy registration inside functions, otherwise YAML loaders might fail in surprising ways.
- Keep registry names stable-documentation, CI scripts, and user models reference them directly.
- Use `dynamic_import("package.module.Class")` sparingly. It is powerful for plug-in architectures but harder to validate than explicit registration.
- Prefer `load_modules_recursively` only during initialization (startup scripts, CLI). Re-importing modules at runtime can lead to duplicate registrations; call `clear_registry()` first if you need a full reload.
- Treat the registry as read-only after model construction; direct mutation of `class_registry` is supported but should be reserved for advanced tooling.
