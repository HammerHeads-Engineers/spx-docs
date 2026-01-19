---
description: Inspect running instances, trigger scenarios, and check logs.
icon: soap
---

# Instances

## Purpose

The Instances view is where you manage running model instances and drill into their detail tabs. Use it to check state, start or stop simulations, and confirm behavior while you iterate.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Instances**. The list shows active instances; use the **Open** action to open the detail view in a new tab.

## What you can do here

* Filter the list by model, review the Name/Model/Status columns, and open instance details in a new tab.

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption><p>Filter instances by model name</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption><p>Bulk operations on selected instances</p></figcaption></figure>

* Create new instances from a model (single or bulk) with a name or name prefix.

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption><p>Adding new instance</p></figcaption></figure>

* Start, stop, or delete instances from the list, or run bulk actions on selected rows.
* In the detail view, switch between Continuous and Stepper modes and run Start/Stop or Prepare/Run, plus Reset/Delete.

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p>Instance view</p></figcaption></figure>

*   Inspect tabs for Attributes (edit values and choose chart axes), Physics (actions), Scenarios, Communication, Polling/Timer, and Logger.<br>

    <figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption><p>Models physics</p></figcaption></figure>
*   Use the chart panel to adjust the time range and refresh rate, clear data, export CSV, or print.

    <figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption><p>Defined ready to use scenarios</p></figcaption></figure>

    <figure><img src="../.gitbook/assets/image (10).png" alt=""><figcaption><p>Communication with protocols</p></figcaption></figure>
*

    <figure><img src="../.gitbook/assets/image (11).png" alt=""><figcaption><p>Communication logs (per attribute/register/binding)</p></figcaption></figure>
*   \[Screenshot: Instance detail header and controls]

    <figure><img src="../.gitbook/assets/image (12).png" alt=""><figcaption><p>Instance polling parameters</p></figcaption></figure>
*   \[Screenshot: Instance detail - Attributes tab and chart panel]

    <figure><img src="../.gitbook/assets/image (13).png" alt=""><figcaption><p>Instance timer parameters</p></figcaption></figure>
* \[Screenshot: Instance detail - Scenarios tab]
*   \[Screenshot: Instance detail - Logger tab]\
    <br>

    <figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption><p>Instance attributes, and time-series chart</p></figcaption></figure>

    <figure><img src="../.gitbook/assets/image (15).png" alt=""><figcaption><p>Instance logs</p></figcaption></figure>

## Typical workflow

1. Open **Instances** and filter by model if needed.
2. Create or select an instance and check its status indicator.
3. Open the detail view, review Attributes, and select axes to plot in the chart.
4. Run a scenario (or toggle an action in Physics) and confirm values change.
5. Check the Logger tab for errors or warnings.

## What to verify

* Integrator: the status indicator reflects the expected state and values change when the SUT drives them.
* QA: scenario start/stop commands update values while time is stepped deterministically.
* Developer: Start/Stop or Prepare/Run commands take effect and Logger stays clean.

## Common issues

* Server connection not established: connect in **Settings** and refresh the list.
* No instances for selected model: clear the model filter or re-run the installer bootstrap.
* Instance detail shows "not found": the instance was deleted or renamed; refresh the list.
* Commands disabled: check the instance state and selected mode (Continuous vs Stepper).
* Logger shows errors: align timestamps with recent changes and check model logs.
