---
description: Create and manage attribute connections between instances.
icon: link
---

# Connections

## Purpose

The Connections view lets you wire data flow between instance attributes without editing model files. Use it to validate signal paths, mirror values, and quickly iterate on wiring during debugging.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Connections**.

## What you can do here

* Browse and search connections by name or endpoint.
* Create, edit, duplicate, or delete connections.
* Toggle connections on/off with the **Enabled** switch.
* Choose **Internal** or **External** value sources (`internal_value` / `external_value`) for each endpoint. Internal values are computed inside the model; External values represent data coming from outside (protocols, UI/tests) and exposed to integrations.
* Import/export full system configuration (models/instances/connections) and copy export data.

### Connections list

The table is grouped into **From** and **To** endpoints. Each connection has:

* **Name** — a human-friendly connection identifier.
* **From** — instance + attribute + value source.
* **To** — instance + attribute + value source.
* **Enabled** — toggle to activate or disable the connection.

Value sources are shown as chips in the list; when you edit a row, they become **Internal/External** toggles. Use **Internal** when you want simulation output, and **External** when the value should represent inbound or integration-facing data.

<figure><img src="../.gitbook/assets/image (19).png" alt=""><figcaption><p>Connections list showing From/To columns + Enabled toggle</p></figcaption></figure>

### Create or edit a connection

Use **Add connection** to create a new row, then select instances and attributes. Use the **Internal/External** toggle in the Value column to choose which attribute value to read/write (`internal_value` vs `external_value`). Internal is the model's computed value; External is the value exposed to or coming from the outside. Save or cancel from the action buttons in the row; existing rows also support **Duplicate** and **Delete**.

<figure><img src="../.gitbook/assets/image (21).png" alt=""><figcaption><p>New connection row in edit mode</p></figcaption></figure>

### Import / Export configuration

Use **Import** or **Export** to move a full system configuration (models, instances, connections) between environments. You can also copy the export payload to the clipboard.

<figure><img src="../.gitbook/assets/image (20).png" alt=""><figcaption><p>Connections page import/export actions</p></figcaption></figure>

## Typical workflow

1. Open **Connections** and search for an existing connection (if needed).
2. Add or edit a connection and select **From** and **To** endpoints.
3. Choose **Internal** or **External** value sources and save.
4. Toggle **Enabled** on and confirm values change in **Instances**.

## What to verify

* Integrator: source and destination instances/attributes exist and update correctly.
* QA: connections are deterministic when stepping time in tests.
* Developer: enabling/disabling connections has immediate effect on values.

## Common issues

* Server connection not established: connect in **Settings** and refresh.
* Attribute list empty: select an instance first; verify the instance exposes attributes.
* Connection does not update values: confirm **Enabled** is on and endpoints are correct.
* Save fails: check for missing name, instance, or attribute.
