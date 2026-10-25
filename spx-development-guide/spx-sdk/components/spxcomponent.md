---
icon: block-brick
---

# SpxComponent

### Overview

An `SpxComponent` represents a node in a tree of components. Each node can:

* Hold configuration data (`definition`)
* Track a parent and any number of named children
*   Propagate lifecycle calls (e.g. `prepare()`, `run()`,

    `destroy()`) through its subtree
* Behave like a Python dict for child lookup

Because of its generic design, you can subclass `SpxComponent` to define

specific simulation models—e.g. electrical devices or control‐system

blocks—that plug into MiL workflows.

***

### Core Attributes

| Attribute    | Type                       | Description                                                        |
| ------------ | -------------------------- | ------------------------------------------------------------------ |
| `name`       | str                        | Unique identifier for this component instance.                     |
| `parent`     | Optional\[`SpxComponent`]  | Reference to the parent component; None if this is the root.       |
| `children`   | Dict\[str, `SpxComponent`] | Mapping of child names to child component instances.               |
| `definition` | Any                        | Configuration data used to populate and initialize this component. |
| `state`      | `SpxComponentState`        | Current lifecycle state (e.g. INITIALIZED, RUNNING, DESTROYED).    |
| `logger`     | logging.Logger             | Preconfigured logger under name spx\_sdk.SpxComponent.\<name>.     |

***

### Child Management

```python
component.add_child(child: SpxComponent)      # Add or replace a named child
component.remove_child(child: SpxComponent)   # Remove a child and clear its parent
component.get_children() -> Dict[str, SpxComponent]
component.get_children_list() -> List[SpxComponent]
```

* Validation
  * Adding a child to itself raises ValueError.
  * Adding non-`SpxComponent` raises ValueError.

***

### Dictionary-Like Interface

`SpxComponent` implements **`getitem`**, **`setitem`**, **`contains`**, and **`len`**, letting you treat it like a dict of its children:

```python
child = component['child_name']      # KeyError if not present
component['new_name'] = child_obj    # ValueError if not SpxComponent
'in_child' in component              # True or False
n = len(component)                   # Number of children
maybe = component.get('child', None) # Safe lookup with default
```

This makes dynamic tree construction and traversal concise and Pythonic.

***

### Lifecycle Methods

Each lifecycle call:

1. Logs the action
2. Updates self.state
3. Propagates the call to all children

| prepare() | Sets state → PREPARING; children → prepare(); → PREPARED         |
| --------- | ---------------------------------------------------------------- |
| run()     | → RUNNING; children → run(); → STOPPED                           |
| start()   | Alias for run().                                                 |
| pause()   | → PAUSING; children → pause(); → PAUSED                          |
| stop()    | → STOPPING; children → stop(); → STOPPED                         |
| reset()   | → STOPPING; children → reset(); → STOPPED                        |
| destroy() | → DESTROYING; children → destroy(); clears children; → DESTROYED |

***

### Extending for Simulation Models

To create a custom component—e.g. a device block in an MiL setup—subclass

`SpxComponent` (or `Item` if you’re using the SPX container pattern):

```python
from spx_sdk.components import SpxComponent, SpxComponentState

class VoltageSource(SpxComponent):
    def _populate(self, definition: dict):
        # Parse parameters: e.g. amplitude, frequency
        super()._populate(definition)
        self.voltage = float(definition.get("voltage", 1.0))
        self.frequency = float(definition.get("frequency", 60.0))

    def prepare(self, *args, **kwargs) -> bool:
        self.logger.debug(f"Configuring {self.name}: {self.voltage}V @ {self.frequency}Hz")
        return super().prepare(*args, **kwargs)

    def run(self, *args, **kwargs) -> bool:
        # Inject into MiL signal bus here...
        self.logger.debug(f"Emitting voltage {self.voltage}V")
        return super().run(*args, **kwargs)
```

*   `_populate`: Override to extract domain-specific properties from

    definition. Always call `super()` first.
*   Lifecycle hooks: Add logging or custom behavior before/after

    calling `super().prepare()` / `super().run()`, etc.

***

### Usage Examples

#### Simple Hierarchy

```python
root = SpxComponent(name="root")
child_a = SpxComponent(name="sensor", parent=root)
child_b = SpxComponent(name="controller", parent=root)

print(f"Children of root: {list(root.children.keys())}")  # ["sensor","controller"]
print("sensor" in root)                                   # True
print(len(root))                                          # 2
```

#### Integrating in MiL System

```python
# Build a network of simulated devices
config = {
    "voltage_source": {"voltage": 5.0, "frequency": 50.0},
    "load":           {"resistance": 100.0}
}
power_net = SpxComponent(name="PowerNetwork", definition=config)
# power_net now has two children: VoltageSource and LoadDevice (if registered)
power_net.prepare()
power_net.run()
```

***

### Best Practices

* Unique Names: Use descriptive, unique name values to avoid collisions.
* Docstrings: Document any overrides of \_populate or lifecycle methods.
* Composition: If your model contains distinct sub-elements, nest them as children.
* Logging: Leverage self.logger.debug for traceability in MiL runs.
* Dictionary Interface: Prefer component.get("child") or 'child' in component over manual children\[...] access.
