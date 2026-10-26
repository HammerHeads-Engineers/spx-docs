# Extend with a Custom Component

This tutorial implements a repeatable contact-fault action in SDK RC21. First
verify it locally, then import the same module into a disposable server RC76.
Use Python 3.12 and the dependencies from the [SDK Quickstart](../spx-development-guide/quick-start-spx-sdk-in-5-minutes.md).

The experiment uses two files: `contact_fault.py` defines the action and
`run_fault.py` prepares a local model, runs 20 cycles and destroys it.

## Save the extension

Save the following as `contact_fault.py`. Each prepared action owns a separate
`random.Random(seed)`. Preparing another instance does not reset its stream.

<!-- tutorial:contact_fault.py:start -->
```python
"""Seeded custom action: import this module before loading its model."""
import random
from spx_sdk.actions import Action
from spx_sdk.registry import register_class


@register_class(name='docs_contact_fault')
class ContactFault(Action):
    def prepare(self, *args, **kwargs):
        result = super().prepare(*args, **kwargs)
        self.rng = random.Random(self.seed)
        return result

    def run(self):
        super().run()
        value = self.value
        if self.rng.random() < self.probability:
            value = 0.0 if self.rng.random() < self.drop_ratio else self.spike_value
        return self.write_outputs(value)


def definition(seed=42):
    return {
        'attributes': {'temperature_c': {'type': 'float', 'default': 20.0, 'unit': 'degC'}},
        'actions': [{'docs_contact_fault': '$ext(temperature_c)',
                     'value': '$in(temperature_c)', 'seed': seed,
                     'probability': 0.5, 'drop_ratio': 0.5, 'spike_value': 500.0}],
    }
```
<!-- tutorial:contact_fault.py:end -->

## Run a local smoke test

Save the following as `run_fault.py` beside `contact_fault.py` and run
`python run_fault.py`. It prints 20 values containing normal readings, drops and
spikes; running it again with seed 42 yields the same sequence.

<!-- tutorial:run_fault.py:start -->
```python
"""Run beside contact_fault.py: python run_fault.py."""
from spx_sdk.model import Model
from contact_fault import definition


def simulate():
    model = Model(name='fault_sensor', definition=definition(seed=42))
    try:
        model.prepare()
        values = []
        for tick in range(20):
            model['timer']['time'] = tick / 10
            model.run()
            values.append(model['attributes']['temperature_c'].external_value)
        return values
    finally:
        model.destroy()


if __name__ == '__main__':
    print(simulate())
```
<!-- tutorial:run_fault.py:end -->

Expected output with seed **42**, in cycle order:

```text
[20.0, 0.0, 500.0, 20.0, 20.0, 0.0, 0.0, 20.0, 0.0, 20.0, 20.0, 500.0, 20.0, 500.0, 20.0, 0.0, 20.0, 0.0, 500.0, 20.0]
```

| Reading | Meaning in this example |
| --- | --- |
| 20.0°C | Normal input presented unchanged. |
| 0.0°C | Simulated contact drop. |
| 500.0°C | Simulated spike. |

Compare the full ordered sequence, not just the presence of these three values.
Use the same seed, parameters and a freshly prepared model.

The internal value remains 20°C; this action writes the external wrapper. It
reapplies a fault after each action execution. A later internal write clears the
external override, so action ordering matters.

## Load into a server

Place `contact_fault.py` in the extension directory mounted into your disposable
server. Its container path must match the configured module search path;
a file in the client working directory is not automatically available inside Docker.
Reload modules through the configured server/client interface, verify that
`docs_contact_fault` is registered, then register `definition(seed=42)` as a
model. Use the [client tutorial](../simulation-and-modeling/using-spx-python.md)
for `real_time=False`, lifecycle, stepping and cleanup.

Module loading executes Python code. Only load extensions you intend to run.
This local test proves action behavior; it does not prove mounted paths, server
reload or protocol access. Test those on your deployment and remove the demo
instance/model afterwards. Clock control does not make a network SUT deterministic.
