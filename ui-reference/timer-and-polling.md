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

## What you can do here

### Polling view

The Polling page shows the polling entity as an attribute tree. Use it to inspect current polling values and adjust settable fields.

<figure><img src="../.gitbook/assets/image (17).png" alt=""><figcaption><p>Polling system parameters</p></figcaption></figure>

* Inspect top-level and nested polling attributes.
* Update settable values and confirm changes in **Instances** or logs.

### Timer view

The Timer page shows the timer entity as an attribute tree. Use it to inspect current timer values and adjust settable fields when needed.

<figure><img src="../.gitbook/assets/image (18).png" alt=""><figcaption><p>Timer system parameters</p></figcaption></figure>

* Inspect timer attributes and nested values.
* Update settable values and confirm behavior in **Instances** or tests.

## Typical workflow

1. Open **Polling** and confirm the attribute tree loads.
2. Expand nodes and note current values.
3. Open **Timer** and confirm the attribute tree loads.
4. Adjust a settable value and observe changes in **Instances**.

## What to verify

* Integrator: timer attributes respond when the stack is running.
* QA: time is stepped deterministically in MiL tests.
* Developer: polling behavior matches expected update cadence.

## Common issues

* No timer available: the server does not expose timer data for this stack.
* No polling available: polling data is not exposed for this stack.
* Values cannot be edited: the attribute is read-only (no setter).
* UI time differs from tests: confirm both point to the same server.
