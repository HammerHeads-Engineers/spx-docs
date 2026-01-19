---
icon: sidebar
---

# UI Overview

The UI is a fast way to inspect a running SPX Server and validate behavior while you iterate.

> First run after installing Smart Building Pack? Follow: [Smart Building Pack: First Run Walkthrough](../getting-started/first-run-smart-building-pack.md).

## Main Areas

Use the UI for interactive inspection and debugging. It helps you confirm what is running, verify state changes, and validate scenarios quickly.

- [Screenshot: UI landing screen / main navigation]

- [Instances](instances.md): inspect running instances, scenario triggers, and logs.
- [Models](models.md): review loaded models and their definitions.
- [Timer & Polling](timer-and-polling.md): check simulated time and polling behavior.
- [Snapshots](snapshots.md): capture and restore known-good states during testing.
- [Settings](settings.md): review UI-level settings and connectivity details.

#### What to keep in mind

* Use the UI for interactive inspection and debugging (instances, scenarios, logs).
* Use MiL tests as the authoritative regression suite. If a value "does not change" in tests, verify your test/client is advancing time deterministically (step time + run loop) before debugging the UI.
