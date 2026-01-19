---
icon: sidebar
---

# General View

The General view is a fast way to inspect a running SPX Server and validate behavior while you iterate.

> First time running SPX? Follow: [Smart Building Pack: First Run Walkthrough](../getting-started/first-run-smart-building-pack.md).

## UI Overview

The UI is designed for interactive debugging and inspection. Use it to confirm that models and instances are loaded, that state changes as expected, and that scenarios behave as intended.

[Screenshot: UI main navigation / landing screen]

Main areas:

- Instances: list of running instances plus a detail view for attributes, scenarios, and logs.
- Models: list of loaded models with a view/edit panel for model definitions.
- Timer & Polling: configure time stepping and polling behavior.
- Snapshots: create and restore snapshots while testing.
- Settings: UI-level configuration for the running stack.

#### What to keep in mind

* Use the UI for interactive inspection and debugging (instances, charts, scenarios, logs).
* Use MiL tests as the authoritative regression suite. If a value “does not change” in tests, verify your test/client is advancing time deterministically (step time + run loop) before debugging the UI.
