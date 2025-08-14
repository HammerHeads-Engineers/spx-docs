# Extend with Custom Component

SPX supports custom components to enable extending simulations with new functionalities and behaviors. This flexibility allows users to model complex and realistic scenarios that go beyond the built-in components, enhancing the fidelity and usefulness of simulations.

In this example, we demonstrate how to simulate a contact fault in a PT100 sensor. Such a fault can manifest as sudden drops to zero or spurious spikes in the sensor output, caused by intermittent contact issues on the sensor terminals. Physically, these faults may arise due to oxidation, vibration, or loose connections, which cause unpredictable interruptions or anomalies in the sensor signal.

The goal of this extension is to emulate this behavior within a simulation to test how the system under test (SUT) handles such anomalies.

## Example YAML – Simulating Contact Fault

```yaml
models:
  pt100_sensor:
    type: pt100
    parameters:
      resistance_nominal: 100.0
      temperature_coefficient: 0.00385
    actions:
      - { ramp: { start_temp: 20.0, end_temp: 100.0, duration: 3600 } }
      - { noise: { mean: 0.0, stddev: 0.05 } }
      - { contact_fault: { target: $ext(temperature), probability: 0.01, spike_value: 1000.0 } } # Custom component simulating contact fault
```

The YAML example above shows the configuration of the PT100 sensor model and the sequence of actions applied to it. The custom component `contact_fault` is referenced as an action with parameters specifying the target signal, the probability of fault occurrence, and the spike value to simulate the fault.

The next step is to implement the `contact_fault` custom component in Python. This implementation will define the behavior of the contact fault within the simulation framework, allowing the simulation engine to apply this fault condition during runtime.

## Implementing Contact Fault in Python

The implementation of the `contact_fault` action will use the SPX SDK's `Action` class as a base. It will model the intermittent contact fault by occasionally injecting spikes or drops into the target signal according to the specified probability and spike value.

```python
# Minimal implementation of a custom action that simulates intermittent
# contact faults on a PT100-like sensor. It randomly injects either a
# drop-to-zero or a spike to a configured value. Typical usage maps this
# action to an *external* attribute target so core simulation logic
# remains stable while the presented value exhibits faults.

import random
from spx_sdk.actions import Action
from spx_sdk.registry import register_class


@register_class(name="contact_fault")
class ContactFault(Action):
    """Randomly injects spikes/drops into the target signal.

    Parameters (populated from YAML):
      - probability (float): chance to inject a fault on each run() step. Default: 0.01
      - spike_value (float): value to use for spike events. Default: 1000.0
      - drop_ratio (float): probability of choosing a drop-to-zero vs. spike. Default: 0.5
      - seed (int|None): optional RNG seed for reproducibility. Default: None
    """

    def _populate(self, definition):
        # Sensible defaults for quick onboarding
        self.probability = 0.01
        self.spike_value = 1000.0
        self.drop_ratio = 0.5
        self.seed = None
        # Allow parent class to override from definition (if provided)
        super()._populate(definition)

    def prepare(self):
        # Reset any internal state and seed RNG if requested
        super().prepare()
        random.seed(self.seed)

    def run(self):
        """Possibly corrupt each mapped output according to probability.
        Returns True if at least one fault was injected in this step.
        """
        faulted = False
        for output in self.outputs.values():
            # Decide if a fault happens on this step
            if random.random() < float(self.probability):
                # Choose between drop-to-zero and spike
                if random.random() < float(self.drop_ratio):
                    output.set(0.0)
                else:
                    output.set(float(self.spike_value))
                faulted = True
        return faulted
```
