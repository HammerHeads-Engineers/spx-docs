---
description: Review simulated time and polling behavior in the UI.
icon: timer
---

# Timer & Polling

## Purpose

The Timer and Polling views expose system-level entities that control simulated time and polling behavior. Use them to confirm deterministic stepping in tests and to keep UI updates predictable. For deeper test guidance, see [Use in Unit Tests (MiL)](../getting-started/use-in-unit-tests-mil.md).

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, open **Timer** or **Polling**. These are separate pages.

<figure><img src="../.gitbook/assets/image (17).png" alt=""><figcaption><p>Polling system parameters</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (18).png" alt=""><figcaption><p>Timer system parameters</p></figcaption></figure>

## What you can do here

* Review the Timer entity attributes exposed by the server and adjust values that have setters.
* Review the Polling entity attributes exposed by the server and adjust values that have setters.
* Use the attribute tree to inspect nested values and confirm current settings.

## Typical workflow

1. Open **Timer** and confirm the timer attributes load.
2. Open **Polling** and confirm polling attributes load.
3. Adjust a value (if the attribute is settable) and observe changes in **Instances**.
4. Return to tests and confirm deterministic stepping still matches expectations.

## What to verify

* Integrator: timer attributes respond when the stack is running.
* QA: time is stepped deterministically in MiL tests.
* Developer: polling behavior matches expected update cadence.

## Common issues

* No timer available: the server does not expose timer data for this stack.
* No polling available: polling data is not exposed for this stack.
* Values cannot be edited: the attribute is read-only (no setter).
* UI time differs from tests: confirm both point to the same server.
