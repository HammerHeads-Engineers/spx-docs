---
description: Inspect system and instance logs with source and severity filters.
icon: file-lines
---

# Logs

## Purpose

The Logs page provides a centralized log viewer for the whole system and for individual instances. Use it to diagnose runtime issues, verify scenario behavior, and quickly isolate protocol/model errors.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Logs**.

## What you can do here

* Switch the source between **System** and a selected instance.
* Filter logs by severity (`ALL`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
* Set tail size (`1..500`) to control how many latest log entries are fetched.
* Refresh manually or keep live polling active.
* Expand long log entries for full details.

> Image placeholder: Logs page with source selector, level filter, and limit input.

## Typical workflow

1. Open **Logs**.
2. Start with **System** source to spot global errors.
3. Switch source to a specific instance when you need model-level details.
4. Narrow to `WARNING` or `ERROR` to triage incidents quickly.
5. Increase tail limit if the issue spans longer sequences.

## What to verify

* Integrator: expected instance and system messages are visible after startup.
* QA: failing scenarios generate deterministic warning/error entries.
* Developer: no repeated unexpected stack traces after model/config changes.

## Common issues

* No logs displayed: verify server connection in **Settings**.
* Missing expected entries: increase tail limit and refresh.
* Source not visible in selector: refresh Instances list and confirm instance exists.
* Very noisy output: filter by `WARNING`/`ERROR` first, then drill down.

## Related pages

* [Instances](instances.md) for per-instance tab-level troubleshooting.
* [Settings](settings.md) for connection setup.
* [Troubleshooting and Support](../troubleshooting-and-support/README.md) for escalation flow.
