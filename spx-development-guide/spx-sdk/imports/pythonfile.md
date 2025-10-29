---
icon: python
---

# PythonFile

The `PythonFile` component is an SPX “container” for dynamically importing and instantiating Python classes at runtime. It extends Item and lets you define a set of module paths, classes, and (optionally) constructor parameters in a configuration dictionary. This is particularly useful in Model-in-the-Loop (MiL) workflows for loading custom model blocks or device simulators from external scripts.

### Overview

When you register a PythonFile (via `@register_class(name="python_file")`), SPX will treat it as a special Item whose children are not other SPX components, but instances of classes loaded from external .py files.

* Dynamic loading: Uses `load_module_from_path()` to import a module given its filesystem path.
* Conditional instantiation:
  * If the target class subclasses Item, it is passed the SPX root and the original definition.
  * Otherwise it is instantiated directly (with optional extra `args`/`kwargs`).
* Class registry: Each instance is stored in the class\_instances dictionary by class name.

\


This makes it easy to package device-oriented Python scripts alongside your SPX model definitions and load them on-the-fly.

***

### Configuration Structure

A PythonFile definition is a dict of the form:

```yaml
python_file:
  "/path/to/mod1.py":
    class: FakeItemClass
    attributes:
      voltage:
        property: "voltage"
  "/path/to/mod2.py":
    class: ControlBlock
    init:
      args: [42]
      kwargs:
        gain: 1.5
    attributes:
      output:
        getter: "read_output"
        setter: "write_output"
```

```json
{
  "python_file": {
    "/path/to/mod1.py": {
      "class": "FakeItemClass",
      "attributes": {
        "voltage": {
          "property": "voltage"
        }
      }
    },
    "/path/to/mod2.py": {
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

* Key: module file path (absolute or relative).
* class: name of the class inside that module to instantiate.
* init (optional): extra constructor parameters for plain (non-Item) classes:
  * `args`: list of positional args
  * `kwargs`: dict of keyword args
* attributes: mapping of SPX-model attribute names to linking instructions:
  * property: name of a Python `@property` to bind
  * getter/setter: names of methods to bind as attribute accessors

***

### Core Attributes

When your SPX model engine instantiates a PythonFile, the following attributes are available:

| Attribute         | Type                  | Descripition                                          |
| ----------------- | --------------------- | ----------------------------------------------------- |
| `class_instances` | Dict\[str, object]    | Maps each class name to its instantiated object.      |
| `definition`      | dict                  | The original configuration dict passed to \_populate. |
| `children`        | _Inherited from Item_ | (May be empty) SPX children, not used here.           |
| `parent`          | _Inherited from Item_ | Parent Item/SpxComponent in the SPX tree.             |
| `name`            | _Inherited from Item_ | Unique name of this PythonFile instance.              |

***

### Usage Example

```python
# In your SPX model definition YAML / dict:
"python_file": {
  "/sim/models/voltage_source.py": {
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
pf.prepare()   # binds SPX attributes to the Python object
pf.run()       # no-op here; your classes participate elsewhere
```

***

### Best Practices

* Absolute paths: Use full filesystem paths for module\_path to avoid import ambiguity.
* init section: Only needed for plain classes whose `__init__` takes extra parameters.
* Attribute names: Ensure your SPX model’s attributes container defines keys matching attributes in definition.
* Logging & Debugging: Use your Python classes’ constructors or methods to log instantiation details.
* MiL Integration: Subclass Item for components that need to propagate SPX lifecycle events (`prepare`, `run`, etc.), and bind SPX attributes for real-time data exchange.
