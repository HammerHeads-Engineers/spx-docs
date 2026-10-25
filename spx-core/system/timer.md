# Timer

The `Timer` component (`spx_core/system/timer.py`) keeps track of simulated time. It supports real-time and manual stepping, making it a key building block for deterministic tests.

## Configuration Example

{% tabs %}
{% tab title="YAML" %}
```yaml
timer:
  step: 0.1          # seconds added each run when in manual mode
  initial_time: 0.0
  max_duration: 3600
  auto_reset: false
  resolution: 0.01   # round time to nearest 10 ms
  decimal_places: 3
```

{% endtab %}

{% tab title="JSON" %}
```json
{
  "timer": {
    "step": 0.1,
    "initial_time": 0.0,
    "max_duration": 3600,
    "auto_reset": false,
    "resolution": 0.01,
    "decimal_places": 3
  }
}

```
{% endtab %}
{% endtabs %}

### Configuration fields

| Field | Description |
|-------|-------------|
| `step` / `time_step` | Default increment applied when you call `run()` manually. |
| `initial_time` | Starting value of the timer when the model loads. |
| `max_duration` | Cap on elapsed time; timer stops (or resets) when this is reached. |
| `auto_reset` | If true, timer wraps around after `max_duration`. |
| `resolution` | Quantizes reported time to fixed increments (useful for UI displays). |
| `decimal_places` | Number of decimals to keep when rounding. |

### Runtime API and manual stepping

Timers are nodes in API v3, not standalone `/timer` routes. For an instance
`demo`, inspect `/api/v3/system/instances/demo/timer`. Component properties use
`/attr/<name>`; methods use `/method/<name>`. Pass request bodies as described
in the [API v3 reference](../../api-v3-reference/README.md).

For deterministic client-driven work, disable real-time operation before starting
the instance. `instance.run(time_step=0.1)` advances its stopped timer by one
step. You can also set `instance["timer"].time` explicitly; assigning time stops
the clock first. A run without an explicit step uses the timer's configured or
last step value. Pause preserves execution state and transports; an explicit
Run while paused performs one admitted cycle and keeps the model paused.

### Tips

- Set `auto_reset: true` when simulating periodic machines (e.g., rotating equipment) to avoid ever-growing time values.
- For QA regression tests, disable real-time mode, set a small `step`, and drive the simulation with a fixed number of iterations.
- Use `resolution` to match the precision of downstream systems—rounded timestamps make comparisons easier.
