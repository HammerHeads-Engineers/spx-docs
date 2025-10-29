# Scenarios

Scenarios (`spx_core/system/scenarios.py`) let you script temporary changes to your simulation: inject noise, disconnect protocols, or override values for a limited time. They are essential for fault-injection tests and QA workflows.

## YAML structure

{% tabs %}
{% tab title="YAML" %}
```yaml
scenarios:
  voltage_spike:
    enabled: true
    duration: 2.0
    actions:
      - override:
          target: "#attr(voltage)"
          value: 400.0
    run_limit: 1
  ascii_disconnect:
    enabled: true
    schedule:
      period: 30.0
      jitter: 5.0
    call:
      path: communication.ascii.detach
      stop_path: communication.ascii.attach
```

{% endtab %}

{% tab title="JSON" %}
```json
{
  "scenarios": {
    "voltage_spike": {
      "enabled": true,
      "duration": 2.0,
      "actions": [
        {
          "override": {
            "target": "#attr(voltage)",
            "value": 400.0
          }
        }
      ],
      "run_limit": 1
    },
    "ascii_disconnect": {
      "enabled": true,
      "schedule": {
        "period": 30.0,
        "jitter": 5.0
      },
      "call": {
        "path": "communication.ascii.detach",
        "stop_path": "communication.ascii.attach"
      }
    }
  }
}
```
{% endtab %}
{% endtabs %}

### Configuration fields

| Field | Description |
|-------|-------------|
| `enabled` | Scenario must be enabled to run. |
| `duration` | Seconds to stay active. Negative or `null` means run until stopped manually. |
| `period` | When set, the scenario schedules its own run loop independent of the model tick. |
| `jitter` | Random variation added to the period. |
| `run_limit` | Number of times the scenario can activate before disabling itself. |
| `actions` | Child actions to execute while active. |
| `call.path` | Method to call when the scenario starts. |
| `call.stop_path` | Method to call when the scenario stops (optional). |
| `overrides` | Mapping of attribute/protocol values to apply temporarily. |

You can also nest a `schedule` block; fields inside it mirror top-level keys and are merged for backward compatibility.

### Lifecycle

1. `start()` prepares children, sets timers, and, if `period` is defined, spawns a dedicated scheduler thread.
2. `run()` executes child components each model tick when no custom period is set.
3. `stop()` cancels timers, cleans up overrides, and deactivates the scenario.

### Common patterns

- **Protocol chaos**: Use `call.path` to detach or attach communication adapters.
- **Signal overrides**: Apply transient `override` actions to attributes and let them revert automatically when the scenario stops.
- **Scheduled disturbances**: Combine `period` and `jitter` for recurring events (e.g., every 30 ±5 seconds).

### Tips for junior engineers / QA

- Start with small durations (1–2 s) to verify behavior, then scale up.
- Watch the server logs; scenarios emit lifecycle messages and diagnostics for easier troubleshooting.
- Combine scenarios with snapshots: capture the baseline, run scenarios, restore to baseline.
- Document test cases alongside the scenario YAML so teammates know why each disturbance exists.
