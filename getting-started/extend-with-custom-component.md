---
icon: puzzle-piece-simple
---

# Extend with a Custom Component

SPX supports custom components to enable extending simulations with new functionalities and behaviors. This flexibility allows users to model complex and realistic scenarios that go beyond the built-in components, enhancing the fidelity and usefulness of simulations.

In this example, we demonstrate how to simulate a contact fault in a PT100 sensor. Such a fault can manifest as sudden drops to zero or spurious spikes in the sensor output, caused by intermittent contact issues on the sensor terminals. Physically, these faults may arise due to oxidation, vibration, or loose connections, which cause unpredictable interruptions or anomalies in the sensor signal.

The goal of this extension is to emulate this behavior within a simulation to test how the system under test (SUT) handles such anomalies.

## Example YAML – Simulating Contact Fault

```yaml
models:
  pt100_sensor:
    attributes:
      temperature: 0.0
    actions:
      - { ramp: $attr(temperature), stop_value: 150, duration: 5, type: overshoot, overshoot: 5 }
      - { noise: $ext(temperature), std: 0.01, mode: proportional }
      - { contact_fault: $ext(temperature), spike_value: 500.0 } # custom extension with spike distortions
```

The YAML example above shows the configuration of the PT100 sensor model and the sequence of actions applied to it. The custom component `contact_fault` is referenced as an action with parameters specifying the target signal, the probability of fault occurrence, and the spike value to simulate the fault.

The next step is to implement the `contact_fault` custom component in Python. This implementation will define the behavior of the contact fault within the simulation framework, allowing the simulation engine to apply this fault condition during runtime.

## Implementing Contact Fault in Python

The implementation of the `contact_fault` action will use the SPX SDK's `Action` class as a base. It will model the intermittent contact fault by occasionally injecting spikes or drops into the target signal according to the specified probability and spike value.

{% code title="./extensions/contact_fault.py" %}
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
        print("Populating ContactFault from definition:", definition)
        # Allow parent class to override from definition (if provided)
        super()._populate(definition)

    def prepare(self):
        # Reset any internal state and seed RNG if requested
        print("Preparing ContactFault with seed:", self.seed)
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
{% endcode %}

```python
# SPDX-License-Identifier: MIT
# Copyright (c) 2025 Hammerheads Engineers sp. z o.o.
# Author: Aleksander Stanik
import sys
import os
import time
import yaml
import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

current_dir = os.getcwd()
repo_root = os.path.abspath(os.path.join(current_dir, '..'))

if repo_root not in sys.path:
    sys.path.append(repo_root)


import spx_python
spx_python.set_global_transparent(False)
# Initialize HTTP-based SPX client wrapper pointing to local SPX server
product_key = os.environ['SPX_PRODUCT_KEY']
wrapper = spx_python.init(address='http://localhost:8000',
                                product_key=product_key)
```

```python
wrapper.reload_modules()
```

```python
# Create a new model for the PT100 sensor
pt_100_yaml = '''
attributes:
  temperature: 0.0
actions:
  - { saw: $attr(temperature), stop_value: 14, period: 5 }
  - { ramp: $attr(temperature), stop_value: 150, duration: 5, type: overshoot, overshoot: 5 }
  - { noise: $ext(temperature), std: 0.01, mode: proportional }
  - { contact_fault: $ext(temperature), spike_value: 500.0 }
'''

# Parse YAML and build the model
data = yaml.safe_load(pt_100_yaml)
wrapper["models"]["pt_100_1"] = data
wrapper["instances"]["test_pt_100"] = "pt_100_1"

instance = wrapper["instances"]["test_pt_100"]
```

```python
temperatures = []
temperatures_raw = []
times = np.linspace(0, 10, 1000)

instance["polling"].disable()

instance.reset()
instance.prepare()

# Run the instance for each time step
for t in times:
    instance["timer"].time = t
    instance.run()
    temperatures.append(instance["attributes"]["temperature"].external_value)
    temperatures_raw.append(instance["attributes"]["temperature"].internal_value)
    # print (f"Time: {t:.2f}s, Temperature: {temperatures[-1]:.2f}°C, Raw: {temperatures_raw[-1]:.2f}°C")

# Plotting the results
fig = go.Figure()
fig.add_trace(go.Scatter(x=times, y=temperatures, mode='lines', name='Temperature'))
fig.add_trace(go.Scatter(x=times, y=temperatures_raw, mode='lines', name='Temperature Internal'))
fig.update_layout(
    title='Change of Temperature Over Time',
    xaxis_title='Time (s)',
    yaxis_title='Temperature (°C)',
    showlegend=True
)

```
