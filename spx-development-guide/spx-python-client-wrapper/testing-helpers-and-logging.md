# Testing Helpers & Logging Integration

The `spx_python.helpers` and logging extensions are designed to make test code shorter, more robust, and observable. This guide shows how to:

- Bootstrap models and instances specifically for tests.
- Capture unit-test assertions and test case results into SPX instance attributes.
- Integrate logging with both `unittest` and `pytest`.
- Inspect the resulting log structures for debugging and reporting.

The examples are based on `spx_python.helpers`, `spx_python.unittest_logging`, and tests such as `tests/test_helpers.py`, `tests/test_unittest_logging.py`, and `tests/test_pytest_logging_integration.py` from the `spx-python` repository.

---

## Unittest integration

### Bootstrapping a model + instance

For integration-style tests it is common to create a real model and instance and reuse them across multiple test methods.

```python
import os
import unittest
from pathlib import Path

import spx_python
from spx_python.helpers import (
    bootstrap_model_instance,
    SpxAssertionLoggingMixin,
    spx_ensure_attribute,
)

BASE_URL = os.getenv("SPX_BASE_URL", "http://localhost:8000")
PRODUCT_KEY = os.environ["SPX_PRODUCT_KEY"]


class HeaterTests(SpxAssertionLoggingMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        model_path = Path("models/heater.yaml")

        client, instance, _changed = bootstrap_model_instance(
            spx_module=spx_python,
            product_key=PRODUCT_KEY,
            base_url=BASE_URL,
            model_path=model_path,
            model_key="tests_heater",
            instance_key="tests_heater_inst",
        )

        cls.client = client
        cls.instance = instance

        # Tell the mixin where to log
        cls.spx_log_instance = instance
        cls.spx_log_attr = "test_logs"
        spx_ensure_attribute(instance, cls.spx_log_attr, default=[])
```

This follows the same pattern as `tests/test_helpers.py::TestHelperIntegration`: model and instance are created once, then used by all tests in the class.

### Capturing assertion logs with `SpxAssertionLoggingMixin`

`SpxAssertionLoggingMixin` wraps all standard `unittest.TestCase.assert*` methods. Each assertion call appends a log entry to `spx_log_attr` on `spx_log_instance`:

- `kind`: `"assertion"`
- `label`: the assertion method name (e.g., `"assertEqual"`)
- `status`: `"pass"` or `"fail"`
- `args` / `kwargs`: JSON-safe copies of the assertion arguments
- `message`: the failure message (for failed assertions)
- `ts`: timestamp (seconds since epoch)

Minimal usage:

```python
class HeaterTests(SpxAssertionLoggingMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ... create cls.instance pointing to your SPX instance ...
        cls.spx_log_instance = cls.instance
        cls.spx_log_attr = "test_logs"
        spx_ensure_attribute(cls.instance, cls.spx_log_attr, default=[])

    def test_temperature_in_range(self):
        temperature = self.instance["attributes"]["temperature"].internal_value
        self.assertGreaterEqual(temperature, 15.0)
        self.assertLessEqual(temperature, 30.0)
```

If `spx_log_instance` or `spx_log_attr` is not set, assertions behave normally without logging, as shown in `tests/test_helpers_logging.py::TestSpxAssertionLoggingMixin`.

### Recording test case start/end with `spx_log_test_case`

The decorator `spx_log_test_case` emits a pair of `"testcase"` entries around a test method:

- `event="start"` before the body runs.
- `event="end"`, with `status="pass"` or `status="fail"`, after the body.

```python
from spx_python.helpers import spx_log_test_case


class HeaterTests(SpxAssertionLoggingMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # ... set cls.spx_log_instance and cls.spx_log_attr ...
        spx_ensure_attribute(cls.spx_log_instance, cls.spx_log_attr, default=[])

    @spx_log_test_case()  # defaults to spx_log_attr ("test_logs")
    def test_heater_can_start(self):
        self.instance.start()
        self.assertEqual(self.instance.state, "running")
```

You can override the attribute path per test:

```python
    @spx_log_test_case(attr_path="attributes/custom_trace")
    def test_custom_channel(self):
        ...
```

See `tests/test_unittest_logging.py::test_spx_log_test_case_records_entries` for the expected log shape.

---

## Pytest integration

### Overview of `SpxPytestLoggerPlugin`

`SpxPytestLoggerPlugin` provides two fixtures and an automatic hook:

- `spx_instance`: a class-scoped fixture that creates/returns the SPX instance used for logging and ensures the log attribute exists.
- `spx_log`: a function-scoped fixture that appends custom entries (for example `"note"` records) to the same attribute.
- `pytest_runtest_makereport` hook: automatically logs `"testcase"` entries with status and duration for each test function.

All three write into `ATTR_PATH` (by default `"test_logs"`) on the instance produced by an `instance_factory` callable.

### Wiring the plugin in `conftest.py`

A typical configuration mirrors `tests/test_pytest_logging_integration.py` but can be simplified for your own project.

```python
# conftest.py
import os
import uuid

import pytest
import spx_python
from spx_python.helpers import SpxPytestLoggerPlugin, spx_ensure_attribute

BASE_URL = os.getenv("SPX_BASE_URL", "http://localhost:8000")
PRODUCT_KEY = os.environ["SPX_PRODUCT_KEY"]
ATTR_PATH = "test_logs"


def _build_client():
    return spx_python.init(address=BASE_URL, product_key=PRODUCT_KEY)


def _instance_factory():
    client = _build_client()
    # Use a dedicated instance for logging
    model_key = "pytest_log_model"
    instance_key = "pytest_log_instance"
    models = client["models"]
    instances = client["instances"]

    if model_key not in models:
        models[model_key] = {"attributes": {ATTR_PATH: []}}
    if instance_key not in instances:
        instances[instance_key] = model_key

    instance = instances[instance_key]
    spx_ensure_attribute(instance, ATTR_PATH, default=[])
    return instance


_plugin = SpxPytestLoggerPlugin(_instance_factory, attr_path=ATTR_PATH)
spx_instance = _plugin.instance_fixture()
spx_log = _plugin.log_fixture()


def pytest_configure(config):
    config.pluginmanager.register(_plugin, "spx_pytest_logger")
```

This setup:

- Registers the plugin globally.
- Exposes `spx_instance` and `spx_log` fixtures to all tests.
- Ensures the log attribute exists on the backing SPX instance before tests run.

### Using `spx_log` in tests

The `spx_log` fixture appends arbitrary entries to the configured attribute. Each call produces a payload like:

- `kind`: value of the first argument (e.g., `"note"`, `"step"`, `"measurement"`).
- `message`: optional human-readable message.
- Additional keyword arguments: merged into the payload as metadata.
- `ts`: timestamp.

```python
def test_pytest_log_fixture_can_append(spx_instance, spx_log):
    before = list(spx_instance["attributes"]["test_logs"].internal_value)

    spx_log(
        "note",
        message="pytest fixture logging",
        marker="pytest_fixture",
        scenario="happy_path",
    )

    after = list(spx_instance["attributes"]["test_logs"].internal_value)
    assert len(after) == len(before) + 1
    assert after[-1]["marker"] == "pytest_fixture"
    assert after[-1]["scenario"] == "happy_path"
```

This is the same pattern used in `tests/test_pytest_logging_integration.py::test_pytest_log_fixture_can_append`.

### Automatic `"testcase"` entries from the plugin hook

`SpxPytestLoggerPlugin.pytest_runtest_makereport` runs after each test and appends a `"testcase"` entry when:

- The phase is `"call"` (setup/teardown are ignored).
- A corresponding SPX instance can be found:
  - Prefer `spx_instance` from `item.funcargs` if present.
  - Otherwise fall back to the instance cached for the node ID (created by `spx_log`).
  - As a last resort, use `cls.spx_log_instance` on the test class if defined.

The payload includes:

- `kind`: `"testcase"`
- `event`: `"end"`
- `status`: `"passed"`, `"failed"`, or `"skipped"`
- `nodeid`: pytest node ID (`test_file.py::TestClass::test_method`)
- `duration`: test duration in seconds
- `message`: stringified failure details for failed tests

In `tests/test_pytest_logging_integration.py` the `verify_pytest_logging_entries` fixture asserts that:

- There are entries of `kind == "note"` produced by `spx_log`.
- There are `"testcase"` entries for at least two tests, all with `event == "end"` and `status == "passed"`.

---

## Inspecting and consuming logs

All logging helpers ultimately append JSON-safe payloads to an SPX attribute, typically `attributes/test_logs/internal_value`:

- Unittest mixin: `kind == "assertion"` and `kind == "testcase"` entries.
- Pytest plugin:
  - `kind == "note"` (or any label you choose) for explicit `spx_log(...)` calls.
  - `kind == "testcase"` from the plugin hook.

You can inspect them directly from Python:

```python
logs_attr = instance["attributes"]["test_logs"]
entries = list(logs_attr.internal_value or [])

for entry in entries:
    print(entry["ts"], entry.get("kind"), entry.get("status"), entry.get("message"))
```

Or via the SPX UI by browsing to the instance and inspecting the corresponding attribute value.

Because the payloads are consistent across `unittest` and `pytest`, you can post-process them in dashboards, CI reports, or custom analytics regardless of which test framework produced them.

---

## Concrete end-to-end examples from `spx-examples`

This section shows how the logging helpers fit into real scenarios taken from the `spx-examples` repository. The goal is to make it trivial to lift the patterns into your own test suites.

### BLE Vital Signs Monitor (unittest)

The `ble_vital_signs_monitor` model exposes vital sign telemetry over a BLE-like SUT helper. The integration test `tests/test_ble_vital_signs_monitor_sut.py` prepares the model and instance, then drives scenarios such as `brisk_walk`.

A logging-aware variant of that setup could look like this:

```python
import os
import unittest
from pathlib import Path

import spx_python
from spx_python.helpers import (
    bootstrap_model_instance,
    SpxAssertionLoggingMixin,
    spx_ensure_attribute,
)
from tests.devices.ble_vital_signs_monitor_sut import BleVitalSignsMonitorSUT


class TestBleVitalSignsMonitorLogged(SpxAssertionLoggingMixin, unittest.TestCase):
    MODEL_PATH = Path("library/domains/ble/generic/vital_signs_monitor__ble_gatt.yaml")
    MODEL_KEY = "tests__ble_vital_signs_monitor"
    INSTANCE_KEY = "tests_ble_vital_signs_monitor_inst"

    @classmethod
    def setUpClass(cls):
        product_key = os.environ["SPX_PRODUCT_KEY"]
        base_url = os.environ.get("SPX_BASE_URL", "http://localhost:8000")

        client, instance, _changed = bootstrap_model_instance(
            spx_module=spx_python,
            product_key=product_key,
            base_url=base_url,
            model_path=cls.MODEL_PATH,
            model_key=cls.MODEL_KEY,
            instance_key=cls.INSTANCE_KEY,
        )

        cls.client = client
        cls.instance = instance
        cls.attributes = instance["attributes"]

        # Configure assertion logging
        cls.spx_log_instance = instance
        cls.spx_log_attr = "test_logs"
        spx_ensure_attribute(instance, cls.spx_log_attr, default=[])

        cls.sut = BleVitalSignsMonitorSUT(
            spx_client=client,
            spx_instance=instance,
            spx_instance_key=cls.INSTANCE_KEY,
        )

    def test_brisk_walk_scenario_is_logged(self):
        scenarios = self.instance["scenarios"]
        scenario = scenarios["brisk_walk"]
        scenario.start()

        # Standard assertion — automatically logged by the mixin
        self.assertTrue(
            self.attributes["activityIntensity"].internal_value >= 0.5,
            "Expected activityIntensity to rise during brisk_walk scenario",
        )
```

After this test runs, SPX will contain a `test_logs` attribute on `tests_ble_vital_signs_monitor_inst` with entries for the assertion (and any additional test case decorators you apply).

### Modbus Vacuum Gauge (unittest)

The Modbus vacuum gauge example (`tests/test_modbus_vacuum_gauge_sut_example.py`) uses `bootstrap_model_instance` and `wait_for_condition` to validate pressure dynamics and relay outputs.

To add structured logging around these assertions:

```python
import os
import pathlib
import unittest

import spx_python
from spx_python.helpers import (
    bootstrap_model_instance,
    SpxAssertionLoggingMixin,
    spx_ensure_attribute,
)
from tests.devices.modbus_vacuum_gauge_sut_example import ModbusVacuumGaugeSUTExample


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "library" / "domains" / "vacuum_systems" / "generic" / "vacuum_gauge__modbus.yaml"
MODEL_KEY = "tests__vacuum_gauge"
INSTANCE_KEY = "generic_vacuum_gauge"
BASE_URL = os.environ.get("SPX_BASE_URL", "http://localhost:8000")


class TestModbusVacuumGaugeLogged(SpxAssertionLoggingMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        product_key = os.environ["SPX_PRODUCT_KEY"]
        client, instance, _changed = bootstrap_model_instance(
            spx_module=spx_python,
            product_key=product_key,
            base_url=BASE_URL,
            model_path=MODEL_PATH,
            model_key=MODEL_KEY,
            instance_key=INSTANCE_KEY,
            attribute_overrides=None,
        )

        cls.client = client
        cls.instance = instance
        cls.attrs = instance["attributes"]

        cls.spx_log_instance = instance
        cls.spx_log_attr = "test_logs"
        spx_ensure_attribute(instance, cls.spx_log_attr, default=[])

    def setUp(self):
        self.sut = ModbusVacuumGaugeSUTExample(unit_id=2, timeout=1.0)
        if not self.sut.connect():
            self.skipTest("Modbus server not reachable at 127.0.0.1:502")

    def tearDown(self):
        if hasattr(self, "sut") and self.sut:
            self.sut.close()

    def test_relay_outputs_follow_setpoints_logged(self):
        # This assertion (and any subsequent ones) are logged to test_logs
        self.assertIn("high_pressure", self.attrs)
```

The full original test contains several assertions on pressure trajectories and relay flags; wrapping them in the mixin gives you a complete assertion trace inside SPX.

### Pytest with a concrete model (generic MQTT environment sensor)

The MQTT environment sensor example in `tests/test_mqtt_environment_sensor_sut_example.py` uses `ensure_model` and `ensure_instance` to prepare an instance backed by `library/domains/iot/generic/environment_sensor__mqtt.yaml`.

Below is a sketch of how to integrate the `SpxPytestLoggerPlugin` into a similar scenario:

```python
# conftest.py (excerpt)
import os
from pathlib import Path

import pytest
import spx_python
from spx_python.helpers import SpxPytestLoggerPlugin, spx_ensure_attribute

ATTR_PATH = "test_logs"
MODEL_PATH = Path("library/domains/iot/generic/environment_sensor__mqtt.yaml")
MODEL_KEY = "tests__generic_mqtt_environment_sensor"
INSTANCE_KEY = "tests_generic_mqtt_environment_sensor_inst"
BASE_URL = os.environ.get("SPX_BASE_URL", "http://localhost:8000")


def _instance_factory():
    client = spx_python.init(address=BASE_URL, product_key=os.environ["SPX_PRODUCT_KEY"])
    models = client["models"]
    instances = client["instances"]

    if MODEL_KEY not in models:
        from spx_python.helpers import load_model_definition, ensure_model

        model_def = load_model_definition(MODEL_PATH)
        ensure_model(client, MODEL_KEY, model_def)

    if INSTANCE_KEY not in instances:
        instances[INSTANCE_KEY] = MODEL_KEY

    instance = instances[INSTANCE_KEY]
    spx_ensure_attribute(instance, ATTR_PATH, default=[])
    return instance


_plugin = SpxPytestLoggerPlugin(_instance_factory, attr_path=ATTR_PATH)
spx_instance = _plugin.instance_fixture()
spx_log = _plugin.log_fixture()


def pytest_configure(config):
    config.pluginmanager.register(_plugin, "spx_pytest_logger")
```

In a test file you can now use `spx_log` while exercising the MQTT SUT:

```python
def test_temperature_telemetry_is_logged(spx_instance, spx_log):
    # ... publish MQTT telemetry and wait for SPX attributes to update ...
    spx_log("note", message="mqtt_temperature_update", model="mqtt_env_sensor")
```

Together with the automatic `"testcase"` entries from the plugin hook, this gives you a timeline of MQTT-driven events and test outcomes attached to `tests_generic_mqtt_environment_sensor_inst`.
