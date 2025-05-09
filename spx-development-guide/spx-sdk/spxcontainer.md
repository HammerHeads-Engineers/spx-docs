---
icon: warehouse-full
---

# SpxContainer

`SpxContainer` is a powerful helper in the SPX-SDK for bulk-instantiating and organizing child items (anything derived from `SpxItem`) from a single YAML/JSON-style “definition” object. It supports two main modes:

1.  **Generic mode** (no `type= filter`):

    Instantiates any registered class it sees in your definition.
2.  **Filtered mode** (`type=SomeBaseClass`):

    Instantiates only subclasses of SomeBaseClass, with sensible fall-back to the base type itself.

### Concepts

*   Registered classes

    All instantiable types must be registered via `@register_class` (or `register_class()`), so that `SpxContainer` knows how to look them up by name.
*   Definition

    A container’s definition can be:

    * A dict: top-level keys map to class-names; values become that child’s .definition.
    * A list: each entry is either
      * a single-key dict {ClassName: config}, or
      * a “raw” scalar (string, number, nested dict with multiple keys) wrapped into a plain `SpxItem`.
*   Generic vs. Filtered

    * Generic: every key (or list-dict) must correspond to a registered class, otherwise ValueError.
    * Filtered: you supply type=FooBase; container will only instantiate subclasses of FooBase, for everything else it will fall back to FooBase itself (if registered), or else error.



### Constructor & API

```python
from spx_sdk.components import SpxComponent, SpxContainer, SpxItem

cont = SpxContainer(
    name: str,             # a label for this container node
    definition: Any,       # dict-or-list-based structure
    parent: SpxComponent,  # optional parent in your component tree
    type: Optional[type]   # optionally filter to only instantiate subclasses of this base
)
```

### Generic Mode Examples

```python
from spx_sdk.registry import register_class, clear_registry
from spx_sdk.components import SpxComponent, SpxContainer, SpxItem

clear_registry()

@register_class()
class A(SpxItem):
    pass

@register_class()
class B(A):
    pass

@register_class()
class CItem(SpxItem):
    pass

# 1) dictionary → one child per key
cont = SpxContainer(
    name="generic",
    definition={
        "A": {"foo": 1},
        "C": "hello"
    },
    parent=root_component
)

# cont.children → [ instance of A(definition={"foo":1}), 
#                   instance of CItem(definition="hello") ]
```

```python
from spx_sdk.registry import register_class, clear_registry
from spx_sdk.components import SpxComponent, SpxContainer, SpxItem

clear_registry()

@register_class()
class A(SpxItem):
    pass

@register_class()
class B(A):
    pass

@register_class()
class CItem(SpxItem):
    pass

# 2) mixed list → dicts with one key instantiate A/B; scalars become raw SpxItem
cont = SpxContainer(
    name="mixed",
    definition=[
      {"A": {"x": 5}},
      {"B": {"y": 7}},
      "just a string",
      {"D": {}},          # unknown single-key dict → ValueError
      {"X":1,"Y":2}       # multi-key dict → wrapped as SpxItem(definition={…})
    ],
    parent=root_component
)
```

```python
from spx_sdk.registry import register_class, clear_registry
from spx_sdk.components import SpxComponent, SpxContainer, SpxItem

clear_registry()

@register_class()
class A(SpxItem):
    pass

@register_class()
class B(A):
    pass

@register_class()
class CItem(SpxItem):
    pass

# 3) single scalar definition → one raw SpxItem child
cont = SpxContainer(
    name="scalar_only",
    definition=123,
    parent=root_component
)
# cont.children → [ SpxItem(definition=123) ]
```

### Filtered Mode Examples

<pre class="language-python"><code class="lang-python">from spx_sdk.registry import register_class, clear_registry
from spx_sdk.components import SpxComponent, SpxContainer, SpxItem

clear_registry()

@register_class()
class A(SpxItem):
    pass

<strong># 1) dict-based filtered
</strong>cont_1 = SpxContainer(
    name="flt1",
    definition={
      "A": {"x":1}, 
      "Unknown": {"foo": "bar"}
    },
    parent=root_component,
    type=SpxItem
)
# children: 
#  - A(definition={"x":1})           # A is a subclass of SpxItem
#  - SpxItem(definition={"foo":"bar"})  # fallback to base type
</code></pre>

```python
# 2) list-based filtered
cont_2 = SpxContainer(
  name="flt2",
  definition=[ "foo", {"x":9}, 42 ],
  parent=root_component,
  type=SpxItem
)
# by “first subclass” approach every node becomes a SpxItem
# fallback → [ SpxItem("foo"), SpxItem({"x":9}), SpxItem(42) ]
```

```python
# 3) scalar filtered → always base type
cont_3 = SpxContainer(
    name="scalar_flt",
    definition="hello",
    parent=root_component,
    type=SpxItem
)
# → [ SpxItem(definition="hello") ]
```

### Edge Cases & Fallbacks

1. Unknown key in generic dict → ValueError
2. Multi-key dict in list → wrapped in `SpxItem`never raises)
3. Filtered mode but base class not registered → ValueError immediately
4. Filtered list: the first matching subclass is used; if none matches, fallback once to the base itself

### Tips & Best Practices

* Always register your custom `SpxItem` subclasses with a unique @register\_class(name="…").
* Use filtered mode to pull out a certain category of items (e.g. only `Action` classes under a “logic” block).
* Keep nested logic in your child definitions – `SpxContainer` never recurses beyond the top level of definition.
