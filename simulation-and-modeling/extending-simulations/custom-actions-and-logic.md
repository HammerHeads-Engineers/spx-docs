# Custom Actions & Logic

The built-in action catalog covers most control and signal-processing scenarios, but advanced projects often need tailor-made behaviours: bespoke trajectories, hardware-specific RPC calls, or complex validation before applying state changes. This guide shows how to author a reusable `Action` extension, borrow conventions from `spx-core/actions`, and integrate it into your models.

---

## Action anatomy recap

An action is a Python class derived from `spx_sdk.actions.Action` and registered with the SDK registry:

- `_populate(definition)` — read configuration from YAML/JSON.
- `prepare()` — allocate resources and reset state; called before the simulation step.
- `run()` — invoked every tick. Must return `super().run(result=value)` when it produces an output.
- `stop()` — optional clean-up hook.

Action instances live inside the model tree; they can navigate to related components via `self.get_root()`, `self.parent`, and attribute wrappers resolved through the registry helpers.

> Inspect existing implementations under `spx-server/spx_core/actions` (e.g., `call.py`, `ramps.py`, `suspend.py`) to see production-grade patterns.

---

## Example: `hysteresis_clamp` action

Consider a scenario where you want to limit an attribute within a band and only propagate changes when the input leaves the band. This avoids chattering when noisy measurements hover around a threshold. The action reads an input attribute, applies hysteresis, and writes the result to an output attribute.

### Implementation (`extensions/actions/hysteresis.py`)

```python
# All comments in English only.
from __future__ import annotations

from typing import Any, Optional

from spx_sdk.actions import Action
from spx_sdk.registry import register_class
from spx_sdk.attributes.resolve_attribute import resolve_attribute_reference_hierarchical


def _coerce_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


@register_class(name="hysteresis_clamp")
class HysteresisClamp(Action):
    """Clamp an input attribute using upper/lower thresholds with hysteresis.

    YAML definition:
      hysteresis_clamp:
        input: "#attr(sensor.temperature)"
        output: "#attr(controller.input)"
        low: 18.0
        high: 22.0
        hysteresis: 0.3
    """

    def _populate(self, definition: Optional[dict]) -> None:
        if not isinstance(definition, dict):
            raise ValueError("hysteresis_clamp definition must be a mapping")

        self._input_ref = definition.get("input")
        self._output_ref = definition.get("output")
        if not self._input_ref or not self._output_ref:
            raise ValueError("hysteresis_clamp requires 'input' and 'output' references")

        self.low = _coerce_float(definition.get("low"), 0.0)
        self.high = _coerce_float(definition.get("high"), 1.0)
        if self.low > self.high:
            raise ValueError("low threshold must be <= high threshold")

        self.hysteresis = max(0.0, _coerce_float(definition.get("hysteresis"), 0.0))
        self._last_output: Optional[float] = None
        super()._populate(definition)

    def prepare(self, *args, **kwargs) -> bool:
        self._input_attr = resolve_attribute_reference_hierarchical(self.parent, self._input_ref)
        self._output_attr = resolve_attribute_reference_hierarchical(self.parent, self._output_ref)
        if self._input_attr is None or self._output_attr is None:
            raise ValueError("Unable to resolve input/output attributes for hysteresis_clamp")
        self._last_output = None
        return super().prepare(*args, **kwargs)

    def run(self, *args, **kwargs) -> bool:
        value = self._read_input()
        output = self._apply_hysteresis(value)
        self._write_output(output)
        return super().run(result=output)

    # Internal helpers -------------------------------------------------
    def _read_input(self) -> float:
        if hasattr(self._input_attr, "external_value"):
            return float(self._input_attr.external_value)
        if hasattr(self._input_attr, "internal_value"):
            return float(self._input_attr.internal_value)
        return float(self._input_attr.get())

    def _write_output(self, value: float) -> None:
        if hasattr(self._output_attr, "internal_value"):
            self._output_attr.internal_value = value
        elif hasattr(self._output_attr, "set"):
            self._output_attr.set(value)
        else:
            raise AttributeError("Output attribute does not support writing")

    def _apply_hysteresis(self, value: float) -> float:
        # First run: clamp directly
        if self._last_output is None:
            clamped = min(self.high, max(self.low, value))
            self._last_output = clamped
            return clamped

        lower_band = self.low - self.hysteresis
        upper_band = self.high + self.hysteresis

        if value < lower_band:
            self._last_output = self.low
        elif value > upper_band:
            self._last_output = self.high
        # Otherwise keep previous output
        return self._last_output
```

Key patterns adopted from existing actions:

- Validation in `_populate` to fail fast when configuration is missing.
- Attribute resolution using `resolve_attribute_reference_hierarchical` so `$in(...)`, `$out(...)`, or `#attr(...)` work interchangeably.
- Writing through `internal_value` first, falling back to attribute wrappers for multi-layer components.
- Returning `super().run(result=output)` so the action can feed its result into other components if wired via `function`.

---

## Registering and wiring the action

Ensure the Python module is importable by the SPX server (drop it into `extensions/actions` or similar and load it via `imports:` or environment hooks).

### YAML snippet

```yaml
imports:
  - extensions.actions.hysteresis

actions:
  - hysteresis_clamp:
      input: $ext(sensor.temperature)
      output: $ext(controller.input)
      low: 18.0
      high: 22.0
      hysteresis: 0.3
```

- The action instance runs every simulation tick.
- When temperature stays within `[18.0, 22.0]`, it preserves the previous output.
- When the reading leaves the hysteresis band, it snaps to the nearest boundary (`low` or `high`).

This wiring mirrors how built-in actions (`pid`, `ramp`, `call`) are declared in the library models under `spx-examples/library`.

---

## Testing the extension

Leverage `spx-python.helpers` to load the action in integration tests:

```python
# All comments in English only.
from pathlib import Path
from spx_python.helpers import bootstrap_model_instance, wait_for_attribute_value

client, instance, _ = bootstrap_model_instance(
    spx_module=spx_python,
    product_key=os.environ["SPX_PRODUCT_KEY"],
    base_url="http://localhost:8000",
    model_path=Path("models/hysteresis_demo.yaml"),
    model_key="hysteresis_demo",
    instance_key="hysteresis_demo_inst",
)

sensor = instance["attributes"]["temperature"]
controller_input = instance["communication"]["pid"]["input"]

sensor.internal_value = 25.0
client.prepare()
client.run()

assert controller_input.internal_value == 22.0

sensor.internal_value = 21.8  # inside hysteresis band → stays at 22.0
client.run()
assert controller_input.internal_value == 22.0

sensor.internal_value = 17.5  # below lower band → snaps to 18.0
client.run()
assert wait_for_attribute_value(instance, "communication/pid/input", 18.0)
```

Unit tests can patch attribute wrappers directly, similar to the approach used in `spx_python/tests/test_client_unit.py`, ensuring the logic copes with `internal_value` and wrapper-based access.

---

## Packaging tips

- Place custom actions inside `extensions/actions` and list them under `imports:` in your model to keep definitions declarative.
- Follow the logging conventions used in `spx-core/actions`: leverage `self.logger` for trace-level information, but avoid noisy logs in tight `run()` loops.
- Document configuration fields alongside the class docstring; the YAML snippet above doubles as inline reference.
- Consider exposing parameters as attributes (e.g., `attributes.hysteresis`) if you want to tune them at runtime via the API.

By adhering to these conventions, custom actions integrate seamlessly with the SPX lifecycle, tooling, and diagnostics — just like the built-in library.***
