---
description: Inspect running instances, trigger scenarios, and check logs.
icon: soap
---

# Instances

## Purpose

The Instances section covers two views: the Instances list and the Instance View (detail tabs). Use the list to locate and manage running instances, and use the Instance View to inspect state, run scenarios, and troubleshoot behavior.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Instances** to open the list. Use the **Open** action to open the Instance View in a new tab.

## Instances list

The list shows active instances with Name, Model, and Status. It also provides model filtering, creation, and bulk actions.

{% stepper %}
{% step %}
#### Filter the list by model to focus on a specific group.

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption><p>Filter instances by model name</p></figcaption></figure>
{% endstep %}

{% step %}
#### Create a new instance (single or bulk) by choosing a model and name or name prefix.

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption><p>Adding new instance</p></figcaption></figure>
{% endstep %}

{% step %}
#### Select instances and use bulk actions to start, stop, delete, or open multiple rows.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption><p>Bulk operations on selected instances</p></figcaption></figure>


{% endstep %}

{% step %}
#### Use per-row actions (Start, Stop, Delete, Open) and the status indicator to control or inspect a single instance.
{% endstep %}
{% endstepper %}

## Instance View

Open the Instance View in a new tab from the list. The header shows the instance name, model, and current status, and the control bar provides action buttons.

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p>Instance view</p></figcaption></figure>

### Controls and modes

* Use **Continuous** mode for Start/Stop and real-time updates.
* Use **Stepper** mode to Prepare and Run single steps.
* Use **Reset** or **Delete** to clear state or remove the instance.

### Tabs and panels

* **Attributes**: view and edit attribute values, select axes, and inspect the time-series chart (range, refresh rate, clear, export CSV, print).

<figure><img src="../.gitbook/assets/image (14).png" alt=""><figcaption><p>Instance attributes, and time-series chart</p></figcaption></figure>

* **Physics**: review actions, toggle enabled state, and inspect action attributes.

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption><p>Physics tab (actions)</p></figcaption></figure>

* **Scenarios**: start or stop scenarios and confirm state transitions.

<figure><img src="../.gitbook/assets/image (9).png" alt=""><figcaption><p>Defined ready to use scenarios</p></figcaption></figure>

* **Communication**: review protocol bindings, toggle enabled state, and open per-binding logs.

<figure><img src="../.gitbook/assets/image (10).png" alt=""><figcaption><p>Communication with protocols</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (11).png" alt=""><figcaption><p>Communication logs (per attribute/register/binding)</p></figcaption></figure>

* **Polling**: inspect per-instance polling attributes and adjust settable values.

<figure><img src="../.gitbook/assets/image (12).png" alt=""><figcaption><p>Instance polling parameters</p></figcaption></figure>

* **Timer**: inspect per-instance timer attributes and adjust settable values.

<figure><img src="../.gitbook/assets/image (13).png" alt=""><figcaption><p>Instance timer parameters</p></figcaption></figure>

* **Logger**: view instance logs and confirm there are no errors.

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
