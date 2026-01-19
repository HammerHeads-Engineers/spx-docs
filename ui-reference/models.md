---
description: Browse loaded models and inspect their definitions.
---

# Models

## Purpose

The Models view helps you verify which models are loaded and what they contain. Use it to review model definitions, confirm scenarios are available, and validate that the right models are present before you create instances.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Models**. The list shows loaded models; select one to open its detail view.

## What you can do here

- Browse loaded models and confirm they match your bundle.
- Open a model detail view to review its definition (YAML/JSON) and scenarios.
- If the UI exposes it, create an instance from a model and then verify it in **Instances**.

## Typical workflow

1. Open **Models**.
2. Select a model you expect to be present.
3. Review the definition for attributes, actions, and scenarios.
4. Create an instance if the UI offers the action, or use the installer bundle.
5. Open **Instances** and confirm the instance is active.

## What to verify

- Integrator: required models for your target protocols are loaded.
- QA: model definitions include the expected attributes and scenarios.
- Developer: updates to model files show up after a reload or restart.

## Common issues

- Model missing from the list: verify the pack/profile selection in the installer bundle.
- Definition looks stale: restart the stack and confirm the model file was updated.
- Instance creation fails: check Logs for validation or schema errors.
- Scenario not present: confirm the scenario is defined in the model.

## Screenshots

[Screenshot: Models list]
[Screenshot: Model detail view]
[Screenshot: Model definition panel (YAML/JSON)]
