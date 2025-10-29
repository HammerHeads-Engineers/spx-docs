# Model Module

The SDK ships with a lightweight `Model` implementation designed for authoring simulations locally, unit testing, and generating YAML artifacts. In production, the SPX Server runs its own core (written in Rust/Go depending on version) that reimplements the same concepts with additional optimizations. The goal of the SDK model layer is to give you an ergonomic sandbox that mirrors server behaviour closely enough to validate definitions before handing them off.

## Base classes and helpers

`spx_sdk.model` exports:

- `Model` / `BaseModel`: orchestrates attributes, actions, conditions, and instances in a single Python object.
- `SimpleTimer`: minimal timer component used to advance simulated time.
- `SimplePolling`: helper for periodic execution loops.

The SDK model builds on top of containers and components from the same package (`SpxAttributes`, `SpxActions`, etc.). Anything you configure via YAML maps to concrete SDK objects, so the same definitions load both in Python and on the server.

## Creating a model in Python

```python
import yaml
from spx_sdk.model import Model

with open("system.yaml") as fh:
    definition = yaml.safe_load(fh)

model = Model("Plant", definition)

# Access top-level containers
attrs = model["attributes"]
actions = model["actions"]

# Drive the model manually
model.prepare()
for _ in range(10):
    model["timer"]["time"] += 0.1
    model.run()
```

You can embed a model inside tests without spinning up the SPX Server. This is ideal for validating custom actions, logic blocks, or protocol adapters before shipping them upstream.

## Working with instances

Models can host nested components declared under `instances`:

```yaml
instances:
  sensor: { attributes: { value: { default: 0.0 } } }
  controller:
    attributes:
      set_point: { default: 10.0 }
    actions:
      - function: "#attr(error)"
        call: "#attr(set_point) - #attr(sensor/value)"
        output: "#attr(error)"
```

```json
{
  "instances": {
    "sensor": {
      "attributes": {
        "value": { "default": 0.0 }
      }
    },
    "controller": {
      "attributes": {
        "set_point": { "default": 10.0 }
      },
      "actions": [
        {
          "function": "#attr(error)",
          "call": "#attr(set_point) - #attr(sensor/value)",
          "output": "#attr(error)"
        }
      ]
    }
  }
}
```


In Python:

```python
sensor = model["instances"]["sensor"]
controller = model["instances"]["controller"]
controller["attributes"].internal["set_point"] = 15.0
```

Every instance is just another `SpxComponent`, so containers and utilities described earlier apply recursively.

## Timers and polling

The SDK lets you plug in a timer to control deterministic time steps:

```python
from spx_sdk.model import SimpleTimer

model["timer"] = SimpleTimer(name="timer", definition={"time": 0.0}, parent=model)
model.prepare()
for tick in range(5):
    model["timer"]["time"] = tick * 0.5
    model.run()
```

`SimplePolling` wraps a loop that repeatedly calls `prepare()` and `run()` at a fixed interval. This is handy for quick prototypes but the production server uses a more sophisticated scheduler.

## Differences vs. server core

- **Performance:** The SDK model is pure Python. It trades raw throughput for readability and ease of extension. The server core reimplements the same lifecycle in a compiled language to handle large deployments and concurrency.
- **Runtime features:** Some advanced behaviours (hot-reload, streaming telemetry, distributed timers) exist only in the server core. Use the SDK to validate definitions and logic, then test the final build on the server.
- **API surface:** The SDK exposes Python-specific conveniences (direct object access, wrappers, ability to monkey-patch components). The server focuses on REST/WS interfaces. Keep your SDK code focused on definition authoring and testing; avoid relying on Python internals if you need parity on the server.

## Recommended workflow

1. Use the SDK model to prototype new components, actions, and logic locally.
2. Write unit tests that instantiate `Model` with your YAML and assert behaviour (`tests/test_actions`, `tests/test_logic`, etc., follow this pattern).
3. Once definitions are stable, deploy them to the SPX Server, which loads the same YAML but executes using its high-performance core.
4. Reserve server-only features (distributed timers, multi-tenant orchestration) for integration tests.
