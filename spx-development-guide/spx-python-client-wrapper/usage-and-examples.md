# Usage & Examples

This guide walks through common workflows using `spx_python.client.SpxClient` and the utilities in `spx_python.helpers`. The examples mirror the scenarios exercised in `tests/test_basic_spx_python.py`, `tests/test_helpers.py`, and the system-level tests inside `spx-examples`.

---

## Navigating the system tree

`SpxClient` behaves like a nested mapping. Indexing descends into sub-components, while attributes inside the `attr` section appear as properties.

```python
client = spx_python.init(address=BASE_URL, product_key=PRODUCT_KEY)

# Access the models container
models = client["models"]                 # returns another SpxClient

# Descend to an instance and grab the temperature attribute wrapper
sensor = client["instances"]["sensor"]
temperature_attr = sensor["attributes"]["temperature"]

current = temperature_attr.internal_value  # READ
temperature_attr.internal_value = current + 2.5  # WRITE

# Methods exposed by a component become callables
sensor.reset()
sensor.start()
```

### Using `get`, `keys`, `items`

- `client.get()` fetches the full JSON payload at the current path.
- `client.get("child", default)` behaves like `dict.get`, catching `SpxApiError`.
- `for name in client["instances"]:` iterates over child component names.

```python
instances = client["instances"]
snapshots = instances.get()  # raw JSON structure

if "supply" in instances:
    supply = instances["supply"]
    print("Timer state:", supply.timer.state)

for name in instances.keys():
    print("Instance:", name)
```

### Setting attributes via `put_attr`

`put_attr(relative_path, value)` addresses attributes using slash-separated paths. The last segment is the attribute, the preceding segments form the parent path.

```python
# Equivalent to client["instances"]["sensor"]["attributes"]["temperature"].internal_value = 42
client.put_attr("instances/sensor/attributes/temperature/internal_value", 42.0)
```

`put_item` performs a raw `PUT` with an arbitrary payload when you need to update multiple fields at once.

---

## Transparent mode for dry runs

Transparent mode turns the client into a no-op stub that records nothing and simply returns empty structures. Enabling it is useful when unit-testing higher-level logic without a live SPX server.

```python
from spx_python import init, set_global_transparent, transparent_mode

set_global_transparent(True)   # every future client defaults to transparent

stub = init(product_key="unused")
assert not stub["models"]      # returns another transparent client

# Override inside a block
with transparent_mode(False):
    live = init(product_key=REAL_TOKEN)
```

Inside transparent mode:

- Indexing returns new transparent clients without performing HTTP.
- Attribute reads return the sentinel (which is falsy).
- Writes and method calls are ignored but return `{"result": True}` to keep call chains intact.

See `tests/test_client_unit.py::TestTransparentSentinel` for the complete behaviour matrix.

---

## Managing models and instances

The helpers in `spx_python.helpers` wrap the repetitive steps used across the `spx-examples` integration tests.

```python
from pathlib import Path
from spx_python.helpers import load_model, create_instance, ensure_instance

client = spx_python.init(address=BASE_URL, product_key=PRODUCT_KEY)

# Load or refresh a model from disk
model_path = Path("library/domains/ble/generic/temperature_sensor__ble_gatt.yaml")
changed = load_model(client, "BleTemperatureSensor", model_path)

# Create a new instance, applying overrides on first start
instance = create_instance(
    client,
    model_name="BleTemperatureSensor",
    overrides={"attributes/temperature/internal_value": 23.5},
)

# Ensure an existing instance is running and apply overrides
ensure_instance(
    client,
    instance_key="ble_sensor_test",
    model_key="BleTemperatureSensor",
    overrides={"timer/time": 5.0},
    recreate=changed,
)
```

`create_instance` automatically derives an instance key from the model name (`sensor_sim` → `sensor_sim`, `sensor_sim_2`, …). These helpers power tests such as `tests/test_helpers.py::TestHelperIntegration`.

---

## Waiting for state changes

Polling utilities make assertions in integration tests reliable:

- `wait_for_instance(client, "foo_inst", timeout=5)` — poll until the instance is visible.
- `wait_for_state(instance, {"RUNNING", "running"})` — poll the `.state` property.
- `wait_for_attribute_value(instance, "attributes/output", 1.0)` — poll until a value matches.
- `wait_seconds(duration)` — sleep with short intervals to keep loops responsive.

```python
from spx_python.helpers import wait_for_attribute, wait_for_state

sensor = client["instances"]["sensor"]

wait_for_state(sensor, {"RUNNING"}, timeout=10.0)

def stabilised(value):
    return abs(value - 42.0) < 0.5

wait_for_attribute(sensor, "attributes/temperature", stabilised, timeout=15.0)
```

These helpers are used heavily in the `spx-examples` device tests (for example the BLE vital signs monitor and Modbus SUTs) to confirm that scenarios and attribute overrides propagate as expected.

---

## Bootstrapping whole systems

`bootstrap_model_instance` bundles the recurring flow present in end-to-end tests:

```python
from spx_python.helpers import bootstrap_model_instance

client, instance, changed = bootstrap_model_instance(
    spx_module=spx_python,
    product_key=PRODUCT_KEY,
    base_url=BASE_URL,
    model_path=Path("library/domains/ble/generic/vital_signs_monitor__ble_gatt.yaml"),
    model_key="tests_ble_vsm",
    instance_key="tests_ble_vsm_inst",
    attribute_overrides={"attributes/activityIntensity/internal_value": 0.3},
)

if changed:
    print("Model definition updated on server")
```

The helper returns the `SpxClient`, the instance wrapper, and a flag indicating whether the model changed (allowing you to reset or recreate dependent instances automatically). This mirrors the setup code in tests like `spx-examples/tests/test_ble_vital_signs_monitor_sut.py`.

---

## Calling component methods

When a component exposes methods such as `start`, `stop`, or custom endpoints defined in your YAML, the client surfaces them as callables that perform `POST /method/<name>`.

```python
instance = client["instances"]["sensor"]

instance.stop()
instance.start()

# Pass keyword arguments — sent as {"kwargs": {...}}
instance.timer.set_rate(rate=5.0)
```

If the call returns JSON, `SpxClient` hands it back directly. Non-JSON responses result in `None`. The unit tests cover both cases (`tests/test_client_unit.py::test_call_method_value_error_returns_none`).

---

## Putting it together

The combination of dictionary traversal, transparent mode, and helper routines lets you write expressive test code:

```python
from spx_python.helpers import wait_for_attribute_value

client = spx_python.init(address=BASE_URL, product_key=PRODUCT_KEY)

# Ensure the model + instance exist
load_model(client, "PIDController", Path("models/pid.yaml"))
controller = ensure_instance(client, "pid_controller", "PIDController")

# Drive a cycle
controller.reset()
controller.start()
client.prepare()
client.run()

self.assertTrue(
    wait_for_attribute_value(controller, "attributes/output", expected=0.0, timeout=5.0)
)
```

Everything shown here is battle-tested through `spx-python`’s own test suite and the sample systems shipped with `spx-examples`.
