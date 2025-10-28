# Polling

`Polling` (`spx_core/system/polling.py`) drives the simulation loop in real time. It runs in a background thread, repeatedly calling `model.run()` and sleeping between iterations.

## YAML structure

```yaml
polling:
  interval: 0.05   # seconds between iterations
  jitter: 0.01     # random +/- jitter
  max_iterations: 0  # 0 or inf = run forever
```

### Configuration fields

| Field | Description |
|-------|-------------|
| `interval` | Base sleep duration between iterations (seconds). |
| `jitter` | Random value added/subtracted from `interval` to emulate real hardware jitter. |
| `max_iterations` | Stop automatically after N iterations; use for short-lived scenarios. |

### Behavior

- When `start()` is called, polling launches a thread that cycles until stopped or the iteration limit is reached.
- It disables nested polling components to avoid double-scheduling when models contain submodels.
- `stop()` joins the thread gracefully.

### Manual control vs. polling

- **Real-time mode**: leave polling enabled; the simulation runs continuously.
- **Deterministic mode**: disable polling (set `model.real_time` to `false`) and drive `run()` manually via API or SDK tests.

### Tips

- For multi-tenant deployments, keep `interval` relatively high (e.g., 50–100 ms) unless you truly need tight loops; this avoids starving other simulations.
- QA engineers can set `max_iterations` in a scenario to run a fixed number of ticks, gather metrics, and stop automatically.
- Always monitor logs—if actions throw exceptions, the polling loop writes stack traces to help you pinpoint faulty components.
