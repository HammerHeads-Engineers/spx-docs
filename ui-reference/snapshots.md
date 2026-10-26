---
description: Use browser controls to save and restore configuration, then start restored instances.
icon: floppy-disks
---

# Snapshots in the UI

## Purpose

The Snapshots view lets you save model/instance/connection configuration and restore that structure later. Use it to reset instances between checks, compare behavior before/after changes, or share a baseline snapshot with your team.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Snapshots**.

## What you can do here

The page has a toolbar (search + actions) and a snapshots table. Use it to capture configuration, review history, and restore baselines.

### Toolbar actions

* **Search** snapshots by label, notes, or path.
* **New snapshot** to capture current configuration.
* **Import/Export** to move configuration (models/instances/connections) between environments.
* During config import, choose whether to include `run.instances` startup data.
* **Copy export data** to share configuration via clipboard.

### Snapshots list

The list shows saved snapshots with label, notes, path (or “In memory”), and date. Each row includes actions to restore, download, or delete that snapshot. Use bulk selection to delete multiple snapshots at once.

<figure><img src="../.gitbook/assets/image (23).png" alt="Snapshots list with label/notes/path/date columns"><figcaption><p>Snapshots list with label/notes/path/date columns</figcaption></figure>

### Create a snapshot

Use **New snapshot** to capture the current configuration. Labels and notes are optional. You can save to memory, disk, or both (disk file names are generated automatically).

<figure><img src="../.gitbook/assets/image (22).png" alt="New snapshot modal with label/notes + save to memory/disk"><figcaption><p>New snapshot modal with label/notes + save to memory/disk</figcaption></figure>

### Restore, download, or delete a snapshot

* **Restore** loads the selected snapshot and resets system state (confirmation required).
* **Download** saves the snapshot JSON to your machine.
* **Delete** removes the snapshot (confirmation required).

In the import dialog review the included configuration sections and instance-start option. After restore reacquire instances, reapply runtime inputs and explicitly start required instances/connections.

<figure><img src="../.gitbook/assets/image (24).png" alt="Restore snapshot confirmation"><figcaption><p>Restore snapshot confirmation</figcaption></figure>

<figure><img src="../.gitbook/assets/image (25).png" alt="Delete snapshot confirmation"><figcaption><p>Delete snapshot confirmation</figcaption></figure>

## Typical workflow

1. Open **Snapshots** and confirm the list loads.
2. Create a snapshot before you run a scenario or test.
3. Make your changes or run the scenario.
4. Restore the snapshot to rebuild structure, then reapply test inputs and start instances.
5. Return to **Instances** and confirm values match the baseline.

## What to verify

* Integrator: restoring a snapshot rebuilds defaults; explicitly set runtime fixture values afterwards.
* QA: snapshots make test setup repeatable.
* Developer: snapshot/restore works before and after model changes.

## Common issues

* Snapshot list is empty: confirm the stack is running and snapshots exist.
* Create fails: check server logs and disk space permissions (for disk snapshots).
* Restore fails: check server logs and confirm the snapshot is still available.
* Runtime values differ after restore: snapshot import resets defaults; reapply test inputs and warmup.
* Import/export fails: ensure the JSON file is valid and matches the expected schema.

These instructions describe UI RC76. Screenshots illustrate the controls; use the text and expected runtime state when the visual layout differs.

For a complete task with before/after checks, follow [Save and restore a configuration](../guides/ui-save-restore.md).
