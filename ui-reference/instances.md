---
description: Inspect running instances, trigger scenarios, and check logs.
---

# Instances

## Purpose

The Instances view is where you inspect running model instances and confirm they behave as expected. Use it to check current state, trigger scenarios, and confirm logs are clean while you iterate.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Instances**. The list shows active instances; select one to open its detail view.

## What you can do here

- Browse running instances and confirm they are active.
- Open an instance detail view to review attributes/state, charts (if available), scenarios, and logs.
- Trigger scenarios and verify that values update as expected.

## Typical workflow

1. Open **Instances**.
2. Select an instance you care about.
3. Review attributes/state to confirm baseline values.
4. Trigger a scenario if you need to force a change.
5. Check the Logs tab for errors or warnings.

## What to verify

- Integrator: the instance is active and values change when the SUT drives them.
- QA: scenario triggers update values while time is stepped deterministically.
- Developer: logs stay clean after loading or updating models.

## Common issues

- Instance missing from the list: verify the installer bundle and bootstrap completed successfully.
- Values do not change: confirm the simulation time is advancing and polling is active.
- Scenario does nothing: confirm the scenario exists in the model definition.
- Logs show errors: check the Logs tab and align timestamps with recent changes.

## Screenshots

- [Screenshot: Instances list]
- [Screenshot: Instance details - Attributes tab]
- [Screenshot: Instance details - Charts tab]
- [Screenshot: Instance details - Scenarios tab]
- [Screenshot: Instance details - Logs tab]
