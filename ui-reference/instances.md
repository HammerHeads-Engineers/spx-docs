---
description: Inspect running instances, trigger scenarios, and check logs.
---

# Instances

## Purpose

The Instances view is where you manage running model instances and drill into their detail tabs. Use it to check state, start or stop simulations, and confirm behavior while you iterate.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Instances**. The list shows active instances; use the **Open** action to open the detail view in a new tab.

## What you can do here

- Filter the list by model, review the Name/Model/Status columns, and open instance details in a new tab.
- Create new instances from a model (single or bulk) with a name or name prefix.
- Start, stop, or delete instances from the list, or run bulk actions on selected rows.
- In the detail view, switch between Continuous and Stepper modes and run Start/Stop or Prepare/Run, plus Reset/Delete.
- Inspect tabs for Attributes (edit values and choose chart axes), Physics (actions), Scenarios, Communication, Polling/Timer, and Logger.
- Use the chart panel to adjust the time range and refresh rate, clear data, export CSV, or print.

- [Screenshot: Instances list with model filter and bulk actions]
- [Screenshot: Instance detail header and controls]
- [Screenshot: Instance detail - Attributes tab and chart panel]
- [Screenshot: Instance detail - Scenarios tab]
- [Screenshot: Instance detail - Logger tab]

## Typical workflow

1. Open **Instances** and filter by model if needed.
2. Create or select an instance and check its status indicator.
3. Open the detail view, review Attributes, and select axes to plot in the chart.
4. Run a scenario (or toggle an action in Physics) and confirm values change.
5. Check the Logger tab for errors or warnings.

## What to verify

- Integrator: the status indicator reflects the expected state and values change when the SUT drives them.
- QA: scenario start/stop commands update values while time is stepped deterministically.
- Developer: Start/Stop or Prepare/Run commands take effect and Logger stays clean.

## Common issues

- Server connection not established: connect in **Settings** and refresh the list.
- No instances for selected model: clear the model filter or re-run the installer bootstrap.
- Instance detail shows "not found": the instance was deleted or renamed; refresh the list.
- Commands disabled: check the instance state and selected mode (Continuous vs Stepper).
- Logger shows errors: align timestamps with recent changes and check model logs.
