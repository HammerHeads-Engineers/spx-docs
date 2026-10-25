---
description: Foundation classes for every SPX object
icon: block-brick
---

# Components

### 1 . The big picture

```markup
SpxComponent  <-- generic lifecycle, hierarchy, hooks
      ▲
      │
SpxContainer  <-- auto‑loads children from YAML/Python definitions
      ▲
      └───> higher‑level bricks (Attributes, Actions, Conditions, …)
```

* `SpxComponent` is the _protocol_ every runtime object obeys.
* `SpxContainer` adds a smart constructor that expands a YAML/JSON _definition_ into an in‑memory tree of child components.

When you declare a model in YAML/JSON or Python dict, SPX silently manufactures a small forest of `SpxContainers` and `SpxComponents`; knowing the two base classes lets you extend the system with zero boilerplate.

***

### _SpxComponent_ — what you get out‑of‑the‑box

| Capability           | Detail                                                                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lifecycle FSM        | prepare → start → run → pause → stop → reset → destroy, with the current state stored in self.state (`SpxComponentState` enum).                         |
| Hierarchy            | Parent/child pointers, depth‑first traversal helpers (get\_root, get\_hierarchy), dict‑like access (comp\["pump"]).                                     |
| Enable/disable flag  | Flip component.enabled = False and all lifecycle calls become no‑ops without altering the tree.                                                         |
| Hook bus             | Register hooks (`register_hook`) and fire them (`trigger_hooks`) on any event name you invent ("`on_set`", "`after_run`", …).                           |
| Pythonic sugar       | `len(comp)`, 'sensor' in comp, `repr(comp)` for painless debugging.                                                                                     |
| Definition hydration | Pass a dict/YAML block as definition= – every key is copied to an attribute, or raises if the attribute doesn’t exist (great for catching typos early). |

Tip : reuse the embedded logger (self.logger.debug(...))—each component has a namespace like\
`spx_sdk.components.SpxContainer.MyModel`.

### _SpxContainer_ — turbo‑charged constructor

`SpxContainer` inherits everything above and turns a data structure into live children at instantiation.

#### Filtered mode (type=SomeSubclass)

```python
attrs = SpxAttributes(
    name="attributes",
    definition={"temperature": 25.0, "power_on": True},
    parent=model,
    type=SpxAttribute          # <-- filter
)
```

* Only entries that map to `SpxAttribute` (or its subclasses) become children.
* Scalars are promoted to the base class with a unique name.
* Dict or list entries are looked up in the registry to find more specific subclasses.

#### Generic mode (default, no type)

{% tabs %}
{% tab title="YAML" %}
```yaml
children:
  PIDController:
    kp: 1.2
  NoiseAction:
    std: 0.05

```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "children": {
    "PIDController": { "kp": 1.2 },
    "NoiseAction": { "std": 0.05 }
  }
}

```
{% endtab %}
{% endtabs %}


* Each key is treated as a class name registered with `@register_class`.
* Instances are created automatically; nested dicts or single‑key list items are supported.

***

### End‑to‑end example – bring your own Action

```python
# 1) Custom Action ----------------------------------------------------
@register_class(name="spring_mass_damper")
class SpringAction(Action):
    def prepare(self, *a, **kw):
        super().prepare(*a, **kw)
        self.k = self.params.get("k", 10.0)
        self.m = self.params.get("m", 1.0)
        self.c = self.params.get("c", 0.2)

    def run(self, *a, **kw):
        x = self.resolve_param(self.params["input"])
        v = self.resolve_param(self.params["velocity"])
        force = -self.k * x - self.c * v            # F = -­kx * cv
        acc = force / self.m
        return super().run(result=acc)
```

### 2) Definition snippet

{% tabs %}
{% tab title="YAML" %}
```yaml
actions:
  - spring_mass_damper: "#attr(acc)"
    input: "#attr(position)"
    velocity: "#attr(speed)"
    k: 15.0
    m: 0.8
    c: 0.05
```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "actions": [
    {
      "spring_mass_damper": "#attr(acc)",
      "input": "#attr(position)",
      "velocity": "#attr(speed)",
      "k": 15.0,
      "m": 0.8,
      "c": 0.05
    }
  ]
}
```
{% endtab %}
{% endtabs %}


* During model load the `actions` container scans the list, spots `spring_mass_damper`, pulls the matching class from the registry, and instantiates it under the parent.
* The new Action inherits lifecycle and hooks from `SpxComponent`; parameters are auto‑hydrated; outputs are resolved to real `SpxAttribute` objects.

### Authoring guidelines

| Do                                                                      | Avoid                                                       |
| ----------------------------------------------------------------------- | ----------------------------------------------------------- |
| Keep subclasses _thin_—delegate cross‑cutting behaviour to hooks.       | Deep inheritance chains; prefer composition via containers. |
| Use trigger\_hooks("on\_event") early in methods to keep extensibility. | Hard‑coding behaviour in run that can’t be overridden.      |
| Validate definition dicts in \_populate, raise early.                   | Silent failures when a user misspells a field.              |
| Call super().\_populate(definition) last if you mutate definition.      | Mutating then forgetting to pass up—children won’t load.    |

***

### Cheat‑sheet

```python
from spx_sdk.components import SpxComponent

class MyHook(SpxComponent):
    def run(self, attr):          # arbitrary signature
        # do something with attr …
        pass

@register_class()                 # now MyHook is usable in YAML
class MyDevice(SpxContainer):     # inherits auto‑child loading
    def _populate(self, defn):
        super()._populate(defn)   # load attributes/actions first
        self.register_hook("on_prepare", MyHook(parent=self))
```

| Want to…               | Call/Property                                |
| ---------------------- | -------------------------------------------- |
| Get root of tree       | `comp.get_root()`                            |
| Walk children          | `for c in comp.get_children_list(): …`       |
| Access attribute value | `model["attributes"]["temp"].external_value` |
| Toggle feature         | `comp.enabled = False`                       |

***

#### TL;DR

* `SpxComponent` → lifecycle + hierarchy + hooks.
* `SpxContainer` → “turn this YAML blob into living children”.

Master these two, and every other SPX brick—attributes, actions, conditions, full models—will feel like variations on a theme rather than brand‑new APIs.
