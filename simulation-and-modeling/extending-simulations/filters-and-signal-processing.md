# Filters & Signal Processing

Filters and derived signals are common in device models:

- smooth noisy measurements (moving average / low-pass),
- compute derived values (RMS, min/max windows, rate-of-change),
- decimate/hold outputs for protocol constraints.

In SPX you typically implement these as **custom actions** (or custom components) so they are testable and deterministic.

## Pattern: “read input attribute → write output attribute”

1. Read an input value (for example `$in(raw_signal)`).
2. Keep internal filter state in the Python class (buffer, integrator, etc.).
3. Write the filtered value to an output (often `$out(filtered_signal)` so presentation effects do not feed back into core logic).

See also: [Extend with a Custom Component](../../getting-started/extend-with-custom-component.md), [Actions](../../spx-development-guide/spx-sdk/actions.md).

## Minimal example: moving average

**Python action** (place under a configured extensions directory, for example `./extensions/moving_average.py`):

```python
from collections import deque

from spx_sdk.actions import Action
from spx_sdk.registry import register_class


@register_class(name="moving_average")
class MovingAverage(Action):
    def _populate(self, definition):
        super()._populate(definition)
        self.window = int(getattr(self, "window", 8))
        self._buf = deque(maxlen=self.window)

    def prepare(self, *args, **kwargs):
        super().prepare(*args, **kwargs)
        self._buf.clear()

    def run(self, *args, **kwargs):
        self.apply_wrappers()
        sample = getattr(self, "source", None)
        if sample is None:
            return False
        self._buf.append(float(sample))
        avg = sum(self._buf) / len(self._buf)
        return self.write_outputs(avg)
```

**YAML wiring** (use the registered class name `moving_average`):

```yaml
attributes:
  raw_signal: 0.0
  filtered_signal: 0.0

actions:
  - moving_average: $out(filtered_signal)
    source: $in(raw_signal)
    window: 8
```
