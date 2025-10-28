# Timer

The `Timer` component (`spx_core/system/timer.py`) keeps track of simulated time. It supports real-time and manual stepping, making it a key building block for deterministic tests.

## YAML structure

```yaml
timer:
  step: 0.1          # seconds added each run when in manual mode
  initial_time: 0.0
  max_duration: 3600
  auto_reset: false
  resolution: 0.01   # round time to nearest 10 ms
  decimal_places: 3
```

### Configuration fields

| Field | Description |
|-------|-------------|
| `step` / `time_step` | Default increment applied when you call `run()` manually. |
| `initial_time` | Starting value of the timer when the model loads. |
| `max_duration` | Cap on elapsed time; timer stops (or resets) when this is reached. |
| `auto_reset` | If true, timer wraps around after `max_duration`. |
| `resolution` | Quantizes reported time to fixed increments (useful for UI displays). |
| `decimal_places` | Number of decimals to keep when rounding. |

### Runtime API

- `GET /timer` returns the current `time`, `running` state, and configuration.
- `PATCH /timer` with `{"time": 120.0}` sets an absolute value (the timer pauses first to avoid skipping).
- `POST /timer/start` / `stop` control real-time accumulation.

### Manual stepping

When `model.real_time` is `false`, you can advance the simulation deterministically:

```bash
POST /run { "time_step": 0.1 }
```

The timer records the last step value so consecutive `run` calls without parameters reuse the same increment.

### Tips

- Set `auto_reset: true` when simulating periodic machines (e.g., rotating equipment) to avoid ever-growing time values.
- For QA regression tests, disable real-time mode, set a small `step`, and drive the simulation with a fixed number of iterations.
- Use `resolution` to match the precision of downstream systems—rounded timestamps make comparisons easier.
