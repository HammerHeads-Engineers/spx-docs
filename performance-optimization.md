# Performance Optimization

Use this checklist when simulations are slow, flaky, or resource-heavy.

## Quick checklist

- **Tick rate**: keep `timer.dt` as coarse as your use case allows; avoid over-simulating.
- **Polling frequency**: reduce adapter polling intervals unless your tests require tight loops.
- **Logs**: avoid noisy logs in per-tick code paths; capture only what helps debug scenarios.
- **Snapshots**: prefer restoring snapshots over re-initializing complex models from scratch.
- **Extensions**: keep custom Python logic lean; avoid blocking I/O in `run()` loops.

Related:

- [Timer](spx-core/system/timer.md)
- [Polling](spx-core/system/polling.md)
- [Snapshots (Core)](spx-core/snapshots.md)
