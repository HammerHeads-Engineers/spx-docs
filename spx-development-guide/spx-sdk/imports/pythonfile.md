---
icon: python
---

# PythonFile

The `PythonFile` component loads Python classes from local `.py` files and binds them into the SPX runtime. It is registered under `python_file` (alias: `import`) and is useful for MiL workflows where you want to ship a small amount of custom logic alongside a model without packaging a full Python module.

### Overview

At load time, `PythonFile`:

- Dynamically imports a module via `load_module_from_path(<file_path>)`.
- Instantiates the configured `class`:
  - if the class subclasses `SpxComponent`, it is instantiated with `(root, definition, *init_args, **init_kwargs)`,
  - otherwise it is instantiated as a plain class with `(*init_args, **init_kwargs)`.
- Stores created objects in `class_instances` (keyed by class name).
- Optionally binds lifecycle methods (`start`/`run`/`pause`/`stop`) to arbitrary methods via the `methods:` mapping.
- Links SPX Attributes to Python properties/methods via the `attributes:` mapping.

***

### Configuration Structure

A PythonFile definition is a dict of the form:

{% tabs %}
{% tab title="YAML" %}
```yaml
python_file:
  "extensions/mod1.py":
    class: FakeItemClass
    attributes:
      voltage:
        property: voltage
    methods:
      start: start
      run:
        method: tick
        args: [3]
  "extensions/mod2.py":
    class: ControlBlock
    init:
      args: [42]
      kwargs:
        gain: 1.5
    attributes:
      output:
        getter: read_output
        setter: write_output

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "python_file": {
    "extensions/mod1.py": {
      "class": "FakeItemClass",
      "attributes": {
        "voltage": {
          "property": "voltage"
        }
      },
      "methods": {
        "start": "start",
        "run": { "method": "tick", "args": [3], "kwargs": {} }
      }
    },
    "extensions/mod2.py": {
      "class": "ControlBlock",
      "init": {
        "args": [42],
        "kwargs": {
          "gain": 1.5
        }
      },
      "attributes": {
        "output": {
          "getter": "read_output",
          "setter": "write_output"
        }
      }
    }
  }
}

```
{% endtab %}
{% endtabs %}

* Key: module file path (absolute or relative filesystem path).
* class: name of the class inside that module to instantiate.
* init (optional): constructor parameters:
  * `args`: list of positional args
  * `kwargs`: dict of keyword args
* methods (optional): lifecycle bindings:
  * supported keys: `start`, `run`, `pause`, `stop`
  * each entry can be a string (method name) or an object with `method`, `args`, `kwargs`
  * `args`/`kwargs` may contain attribute references such as `$attr(value)` (resolved at call time)
* attributes: mapping of SPX-model attribute names to linking instructions:
  * property: name of a Python `@property` to bind
  * getter/setter: names of methods to bind as attribute accessors

***

### Core Attributes

When your SPX model engine instantiates a PythonFile, the following attributes are available:

| Attribute         | Type               | Description                                           |
| ----------------- | ------------------ | ----------------------------------------------------- |
| `class_instances` | Dict\[str, object] | Maps each class name to its instantiated object.      |
| `definition`      | dict               | The original configuration dict passed to `_populate`. |
| `parent`          | object             | Parent component in the SPX tree.                     |
| `name`            | str                | Unique name of this PythonFile instance.              |

***

### Usage Example

```python
# In your SPX model definition YAML / dict:
"python_file": {
  "extensions/voltage_source.py": {
    "class": "VoltageSource",
    "init": {
      "args": [230, 50],         # voltage=230V, frequency=50Hz
      "kwargs": {"phase": 0.0}
    },
    "attributes": {
      "voltage": {"property": "voltage"},
      "frequency": {"property": "frequency"}
    }
  }
}

# In SPX application:
pf = PythonFile(name="external_models", definition=your_config)
pf.prepare()   # binds SPX attributes and prepares method bindings
pf.run()       # calls bound run() methods (or falls back to instance.run())
```

***

### Best Practices

* Paths: prefer repo-relative file paths checked into your project. In Docker, make sure the same paths exist inside the container (mount your repo or extensions folder).
* init section: use it only if your class requires constructor parameters.
* Attribute names: ensure your model’s `attributes` container defines keys matching the `attributes:` bindings.
* Logging & Debugging: check server logs for import/initialisation failures (`docker compose logs --tail=200 --no-color spx-server`).
* If you need reusable libraries (not file-path imports), prefer registry-based components: `spx-development-guide/spx-sdk/registry.md`.
