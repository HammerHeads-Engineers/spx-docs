---
description: Browse loaded models and inspect their definitions.
icon: code
---

# Models

## Purpose

The Models view helps you verify which models are loaded and what they contain. Use it to review model definitions, create or edit models, and validate that the right models are present before you create instances.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Models**. The list shows loaded models; editing a model opens in a new tab.

## What you can do here

* Browse loaded models and confirm they match your bundle.
* Click a definition preview to open the full definition modal and copy it if needed.
* Create a new model or load a model from a JSON/YAML file.
* Edit or delete models, including bulk delete or bulk edit for selected rows.
* In the editor, switch between JSON and YAML, test the model, and save updates.
* \[Screenshot: Models list with definition preview]
* \[Screenshot: Model definition modal (copyable)]
* \[Screenshot: Model editor with JSON/YAML tabs]
* \[Screenshot: Load model modal]

## Typical workflow

1. Open **Models** and confirm expected models are listed.
2. Click a definition preview to inspect the full model definition.
3. Open **Edit** (new tab), update JSON/YAML, and use **Test model** to preview values.
4. Save the model and return to **Models** to confirm the list refreshes.
5. Create instances from the **Instances** page and verify they start correctly.

## What to verify

* Integrator: required models for your target protocols are loaded.
* QA: model definitions include the expected attributes and scenarios.
* Developer: editor changes persist and test preview data updates.

## Common issues

* Model missing from the list: verify the pack/profile selection in the installer bundle.
* Load model fails: validate JSON/YAML syntax and ensure the model name is unique.
* Edit/Create opens in a new tab: allow pop-ups if your browser blocks them.
* Definition looks stale: refresh the page or restart the stack after updates.
