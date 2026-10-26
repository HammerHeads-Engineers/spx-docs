---
description: Implement and verify a three-sample moving-average action in a local SDK model.
---
# Filter a signal

**Goal:** inputs **0, 3, 6, 9** produce **0, 1.5, 3, 6** using a three-sample
moving average. **Before you start:** the [SDK environment](../../spx-development-guide/quick-start-spx-sdk-in-5-minutes.md).
This runs locally and needs no server or product key.

## 1. Save the action and model

Save as **moving_average.py**. Import registers the action before the model is
constructed. Prepare clears the per-instance buffer; Run resolves the current
source before adding it. During warmup average only the samples received so far.
Each prepared action owns its own buffer. The table below makes warmup and
the first discarded sample explicit.

<!-- tutorial:moving_average.py:start -->
```python
"""Local SDK filter: python moving_average.py. Register before loading the model."""
from collections import deque
from spx_sdk.actions import Action
from spx_sdk.registry import register_class
from spx_sdk.model import Model


@register_class(name='docs_moving_average')
class MovingAverage(Action):
    def prepare(self, *args, **kwargs):
        result = super().prepare(*args, **kwargs)
        self.samples = deque(maxlen=int(self.window))
        return result

    def run(self):
        super().run()
        self.samples.append(float(self.source))
        return self.write_outputs(sum(self.samples) / len(self.samples))


def simulate():
    model = Model(name='filtered_sensor', definition={
        'attributes': {'k__raw_signal': 0.0, 'filtered_signal': 0.0},
        'actions': [{'docs_moving_average': '$out(filtered_signal)',
                     'source': '$in(k__raw_signal)', 'window': 3}],
    })
    try:
        model.prepare()
        result = []
        for tick, value in enumerate((0.0, 3.0, 6.0, 9.0)):
            model['timer']['time'] = tick / 10
            model['attributes']['k__raw_signal'].internal_value = value
            model.run()
            result.append(model['attributes']['filtered_signal'].external_value)
        assert result == [0.0, 1.5, 3.0, 6.0], result
        return result
    finally:
        model.destroy()


if __name__ == '__main__':
    print(simulate())
```
<!-- tutorial:moving_average.py:end -->

## 2. Run and check the values

```bash
python moving_average.py
```

```text
[0.0, 1.5, 3.0, 6.0]
```

| Input | Samples currently in the buffer | Expected output |
| --- | --- | --- |
| 0 | `[0]` | 0.0 |
| 3 | `[0, 3]` | 1.5 |
| 6 | `[0, 3, 6]` | 3.0 |
| 9 | `[3, 6, 9]` | 6.0 |

On the fourth cycle the oldest sample, 0, has left the three-sample buffer.

**Completion:** the embedded assertion passes and the model is destroyed.
An External output is a presentation result; another Internal write to the same
attribute would clear an External override. Keep action ordering explicit.

For server installation and fresh instances use
[Test and reload extensions](testing-and-hot-reload.md). See
[Actions reference](../../spx-development-guide/spx-sdk/actions.md) for the lifecycle.
