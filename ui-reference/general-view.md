---
icon: browser
---

# UI Overview

The UI is a fast way to inspect a running SPX Server and validate behavior while you iterate.

> First run after installing Smart Building Pack? Follow: [Smart Building Pack: First Run Walkthrough](../getting-started/first-run-smart-building-pack.md).

## Main Areas

Use the UI for interactive inspection and debugging. It helps you confirm what is running, verify state changes, and validate scenarios quickly.

<figure><img src="../.gitbook/assets/Zrzut ekranu 2026-01-19 o 10.47.24.png" alt=""><figcaption></figcaption></figure>

* [Instances](instances.md): inspect running instances, scenario triggers, and logs.
* [Models](models.md): review loaded models and their definitions.
* [Connections](connections.md): wire attribute data flow between instances.
* [Timer & Polling](timer-and-polling.md): separate Timer and Polling pages for system attributes.
* [Snapshots](snapshots.md): capture and restore known-good states during testing.
* [Settings](settings.md): review UI-level settings and connectivity details.

#### What to keep in mind

* Use the UI for interactive inspection and debugging (instances, scenarios, logs).
* Use MiL tests as the authoritative regression suite. If a value "does not change" in tests, verify your test/client is advancing time deterministically (step time + run loop) before debugging the UI.
