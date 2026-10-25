# Scenarios

Scenarios (`spx_core/system/scenarios.py`) let you script temporary changes to your simulation: inject noise, disconnect protocols, or override values for a limited time. They are essential for fault-injection tests and QA workflows.

## Configuration example

```yaml
scenarios:
  temperature_spike:
    enabled: false
    duration: 2.0
    overrides:
      $in(temperature_c): 80.0
```

Start `temperature_spike` explicitly on the chosen instance. `enabled: true`
opts into automatic start with its parent; keep it false for opt-in fault
injection. For actions, use the normal `actions` list. A lifecycle method call
belongs inside that list as a `call` action with `path` and optional `stop_path`.

### Configuration fields

| Field | Description |
|-------|-------------|
| `enabled` | Configured automatic-start policy; manual start can activate an opt-in scenario. |
| `duration` | Seconds to stay active. Negative or `null` means run until stopped manually. |
| `period` | When set, the scenario schedules its own run loop independent of the model tick. |
| `jitter` | Random variation added to the period. |
| `run_limit` | Number of times the scenario can activate before disabling itself. |
| `actions` | Child actions to execute while active. |
| `actions[].call.path` | Method invoked by a lifecycle call action. |
| `actions[].call.stop_path` | Optional stop counterpart for that call action. |
| `overrides` | Mapping of attribute/protocol values to apply temporarily. |

You can also nest a `schedule` block; fields inside it mirror top-level keys and are merged for backward compatibility.

### Lifecycle

1. `start()` prepares children, sets timers, and, if `period` is defined, spawns a dedicated scheduler thread.
2. `run()` executes child components each model tick when no custom period is set.
3. `stop()` cancels timers, cleans up overrides, and deactivates the scenario.

### Common patterns

- **Protocol chaos**: Use an `actions` list containing a `call` action with `path` to detach or attach communication adapters.
- **Signal overrides**: `overrides` restores previous values on stop. `set` and `function` actions materialize changes that remain after stop.
- **Scheduled disturbances**: Combine `period` and `jitter` for recurring events (e.g., every 30 ±5 seconds).

### Tips for junior engineers / QA

- Start with small durations (1–2 s) to verify behavior, then scale up.
- Watch the server logs; scenarios emit lifecycle messages and diagnostics for easier troubleshooting.
- Combine scenarios with snapshots: capture the baseline, run scenarios, restore to baseline.
- Document test cases alongside the scenario YAML so teammates know why each disturbance exists.
