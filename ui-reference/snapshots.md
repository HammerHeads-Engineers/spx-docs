---
description: Capture and restore system snapshots.
icon: floppy-disks
---

# Snapshots

## Purpose

The Snapshots view lets you capture a known-good system state and restore it later. Use it to reset instances between checks, compare behavior before/after changes, or share a baseline snapshot with your team.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Snapshots**.

## What you can do here

The page has a toolbar (search + actions) and a snapshots table. Use it to capture state, review history, and restore baselines.

### Toolbar actions

* **Search** snapshots by label, notes, or path.
* **New snapshot** to capture current system state.
* **Import/Export** to move configuration (models/instances/connections) between environments.
* **Copy export data** to share configuration via clipboard.

### Snapshots list

The list shows saved snapshots with label, notes, path (or “In memory”), and date. Each row includes actions to restore, download, or delete that snapshot. Use bulk selection to delete multiple snapshots at once.

<figure><img src="../.gitbook/assets/image (23).png" alt=""><figcaption><p>Snapshots list with label/notes/path/date columns</p></figcaption></figure>

### Create a snapshot

Use **New snapshot** to capture the current system state. Labels and notes are optional. You can save to memory, disk, or both (disk file names are generated automatically).

<figure><img src="../.gitbook/assets/image (22).png" alt=""><figcaption><p>New snapshot modal with label/notes + save to memory/disk</p></figcaption></figure>

### Restore, download, or delete a snapshot

* **Restore** loads the selected snapshot and resets system state (confirmation required).
* **Download** saves the snapshot JSON to your machine.
* **Delete** removes the snapshot (confirmation required).

<figure><img src="../.gitbook/assets/image (24).png" alt=""><figcaption><p>Restore snapshot confirmation</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (25).png" alt=""><figcaption><p>Delete snapshot confirmation</p></figcaption></figure>

## Typical workflow

1. Open **Snapshots** and confirm the list loads.
2. Create a snapshot before you run a scenario or test.
3. Make your changes or run the scenario.
4. Restore the snapshot to reset state.
5. Return to **Instances** and confirm values match the baseline.

## What to verify

* Integrator: restoring a snapshot returns values to the expected baseline.
* QA: snapshots make test setup repeatable.
* Developer: snapshot/restore works before and after model changes.

## Common issues

* Snapshot list is empty: confirm the stack is running and snapshots exist.
* Create fails: check server logs and disk space permissions (for disk snapshots).
* Restore fails: check server logs and confirm the snapshot is still available.
* State does not match baseline: verify you restored the intended snapshot.
* Import/export fails: ensure the JSON file is valid and matches the expected schema.
