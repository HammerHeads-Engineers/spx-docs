---
description: Browse loaded models and inspect their definitions.
icon: code
---

# Models

## Purpose

The Models view helps you verify which models are loaded and what they contain. Use it to review definitions, create or edit models, and confirm you have the right model set before creating instances.

Back to UI Overview: [UI Overview](general-view.md).

## Where to find it

In the UI navigation, select **Models**. The list shows loaded models; editing or creating a model opens the Model View in a new tab.

## What you can do here

### Models list

* Browse loaded models and confirm they match your bundle.
* Search by name or definition content to find a specific model.
* Click a definition preview to open the full definition modal and copy it.
* Create a new model, or load a model from a JSON/YAML file.
* Export selected models to a file or copy them to the clipboard.
* Import/export full system configuration (models/instances/connections).
* Edit or delete models, including bulk delete or bulk edit for selected rows.

The table shows model names and a compact definition preview. Clicking the preview opens a full-definition modal; selecting rows enables bulk actions in the header.

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption><p>Models list with search, counts, and actions</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption><p>Model definition modal with copy action</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p>Models list with selection + bulk actions</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption><p>Import/Export configuration modal (Models page)</p></figcaption></figure>

### Model view (editor)

The Model View opens in a new tab when you create or edit a model. It is a split view: the editor on the left and validation logs on the right.

* Edit JSON or YAML definitions with automatic format conversion.
* Use **Save** to create or update the model (rename by clicking the model name in the header).
* Use **Test model** to create/open a test instance in a new tab.
* Load from file, save to file, copy to clipboard, search, and format the definition.
* Review create/update/test/delete results in the **Validation** panel.

The header shows the editable model name; the toolbar groups model actions (save/test/delete) and file helpers (load/save/copy/search/format).

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption><p>Model view header with editable name</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption><p>Model editor with JSON/YAML tabs + action toolbar</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (7).png" alt=""><figcaption><p>Validation panel with test/save results</p></figcaption></figure>

## Typical workflow

1. Open **Models** and confirm expected models are listed.
2. Click a definition preview to inspect the full model definition.
3. Open **Edit** (new tab) to enter the Model View.
4. Update JSON/YAML, **Test model** to open a test instance, then **Save**.
5. Return to **Models** to confirm the list refreshes and create instances.

## What to verify

* Integrator: required models for your target protocols are loaded.
* QA: model definitions include the expected attributes and scenarios.
* Developer: editor changes persist, and validation logs show successful updates/tests.

## Common issues

* Model missing from the list: verify the pack/profile selection in the installer bundle.
* Save/Test fails: ensure the model name is set and JSON/YAML parses correctly.
* Load model fails: validate JSON/YAML syntax and ensure the model name is unique.
* Edit/Create opens in a new tab: allow pop-ups if your browser blocks them.
* Definition looks stale: refresh the page or restart the stack after updates.
