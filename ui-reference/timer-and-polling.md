---
description: Review simulated time and polling behavior in the UI.
---

# Timer and Polling

## Purpose

The Timer and Polling view is where you check how simulated time advances and how often the UI refreshes data. Use it to confirm deterministic stepping in tests and to keep UI updates predictable. For deeper test guidance, see [Use in Unit Tests (MiL)](../getting-started/use-in-unit-tests-mil.md).

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Timer & Polling**.

- [Screenshot: Timer and Polling main view]

## What you can do here

- View current simulated time and run state.
- Adjust time stepping controls if the UI exposes them.
- Review polling settings that control UI update frequency.

- [Screenshot: Timer controls]
- [Screenshot: Polling settings]

## Typical workflow

1. Open **Timer & Polling**.
2. Confirm time advances while your script or test runs.
3. Adjust step size or polling interval if needed.
4. Return to **Instances** and confirm values refresh as expected.

## What to verify

- Integrator: simulated time advances while the stack is running.
- QA: time is stepped deterministically in MiL tests.
- Developer: polling frequency matches expected update cadence.

## Common issues

- Time does not advance: confirm your test/client is updating the timer.
- Values look stale: verify polling interval and refresh the view.
- Non-deterministic updates: ensure deterministic stepping in tests.
- UI time differs from tests: confirm both point to the same server.
