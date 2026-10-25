---
icon: up-to-dotted-line
---

# Imports

In SPX SDK docs, “imports” covers the mechanisms used to bring Python code into a running SPX configuration.

Use imports when YAML alone is not enough:

- loading custom Python classes from local `.py` files (quick prototyping, tests),
- binding Python object properties/methods to SPX attributes,
- or wiring lifecycle methods (`start`/`run`/`stop`) into a model definition.

## Two common patterns

1) **Registry-based components (recommended for libraries)**

Package your extension code as a Python module and register classes via the SDK registry. This is the most maintainable path for reusable actions/components.

See: [Registry](../registry.md).

2) **File-based imports with `python_file` / `import`**

Use the `python_file` component (alias: `import`) to load classes from repo-local files and bind them into the runtime.

See: [PythonFile](pythonfile.md).

## Minimal example (YAML)

```yaml
python_file:
  extensions/my_block.py:
    class: MyBlock
    attributes:
      temperature_c:
        property: temperature_c
    methods:
      run:
        method: tick
        args: [1]
```

Notes:

- Prefer repo-relative paths checked into your project for reproducible builds.
- The path must exist inside the SPX Server process (in Docker, mount the folder into the container).
- `args`/`kwargs` in `methods` can reference runtime values via attribute refs like `$attr(value)`.
