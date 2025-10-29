# Model Loader

`spx_core/system/model.py` defines the `Model` class that the server instantiates for every YAML document. It is responsible for:

- Holding top-level containers (`attributes`, `actions`, `communication`, etc.).
- Spinning up dedicated `Timer`, `Polling`, and `Scenarios` children when those sections appear in YAML.
- Driving the lifecycle (`prepare`, `start`, `run`) for the entire simulation.

## YAML structure

{% tabs %}
{% tab title="YAML" %}
```yaml
model:
  name: plant
  timer:
    step: 0.1
  polling:
    interval: 0.05
  scenarios:
    voltage_drift:
      enabled: true
      duration: 5.0
      actions:
        - noise:
            output: "#attr(voltage)"
            std: 0.01
  attributes: { ... }
  actions: [ ... ]
  communication: { ... }
```
{% endtab %}

{% tab title="JSON" %}
```json
{
  "model": {
    "name": "plant",
    "timer": {
      "step": 0.1
    },
    "polling": {
      "interval": 0.05
    },
    "scenarios": {
      "voltage_drift": {
        "enabled": true,
        "duration": 5.0,
        "actions": [
          {
            "noise": {
              "output": "#attr(voltage)",
              "std": 0.01
            }
          }
        ]
      }
    },
    "attributes": { "...": "..." },
    "actions": [ "..." ],
    "communication": { "...": "..." }
  }
}
```
{% endtab %}
{% endtabs %}

### Key behaviors

- **Automatic extraction**: The loader pulls `timer`, `polling`, and `scenarios` from the model definition before instantiating other containers. This keeps the YAML tidy—no need to declare those sections separately.
- **Unique identifier**: Each model gets a `uid` (UUID string) you can query through the API for observability.
- **Real-time flag**: `model.real_time` controls whether the polling loop runs continuously (`true`) or waits for manual ticks (`false`). You can flip it through the API for deterministic testing.

### Lifecycle expectations

1. `prepare()` is called on every child (attributes, actions, communication, timer, polling, scenarios).
2. `start()` launches timer/polling threads when `real_time` is true.
3. `run()` is driven by either the polling loop or manual API calls (`POST /run`).

### Practical tips

- Always keep `attributes`, `actions`, and `communication` at the top level—nested models inherit the same pattern.
- Use the SDK to validate the structure before deploying; the server loader relies on the same class registry.
- To disable real-time execution in tests, call `PATCH /models/<id>` with `{ "real_time": false }` and then trigger `run()` steps manually.
