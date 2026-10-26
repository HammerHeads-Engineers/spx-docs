---
description: Load a ready-made model, start one instance and verify an input change through the UI.
---
# Create and control an instance

**Goal:** run `my_temperature_sensor` and make its telemetry read **31.25°C**.
**Before you start:** complete [UI setup](ui.md#before-the-exercises), with space
for one model and one instance. Reserve the names below; use a fresh workspace
if either already belongs to another exercise.

## 1. Load the ready-made model

Open **Models** in the sidebar and choose **Load model from file**. Save
[this model file](https://raw.githubusercontent.com/HammerHeads-Engineers/spx-docs/main/examples/guides/temperature_sensor.yaml)
to your computer, then select it in the file picker. It is a model definition,
not a full system configuration.
<figure><img src="../.gitbook/assets/guide-models-start.jpg" alt="Full SPX Models page with sidebar and Load model from file in its toolbar."><figcaption><p>Models is selected in the sidebar. Load model from file imports one definition.</p></figcaption></figure>

In **Load Model**, enter **my_temperature_model** as Model name and click
**Load Model**. The registry name identifies the saved model; the definition's
`name: pt100_demo` is metadata.
<figure><img src="../.gitbook/assets/guide-load-model.jpg" alt="Load Model dialog over the Models page, with temperature_sensor.yaml and Model name my_temperature_model."><figcaption><p>Choose the supplied YAML file and save it as my_temperature_model.</p></figcaption></figure>

**Check:** the Models list contains `my_temperature_model`.
<figure><img src="../.gitbook/assets/guide-model-loaded.jpg" alt="Models page listing the saved my_temperature_model definition."><figcaption><p>The saved model is now available when creating an instance.</p></figcaption></figure>

## 2. Create an instance

Open **Instances**, click **New instance**, select model `my_temperature_model`,
and keep **Single instance** selected. Enter **my_temperature_sensor** as Name
and choose **Create**. No meta parameters are needed for this protocol-free model.
<figure><img src="../.gitbook/assets/guide-create-instance.jpg" alt="New Instance dialog showing my_temperature_model, Single instance and my_temperature_sensor."><figcaption><p>The model is the reusable definition; the instance is the device you will run.</p></figcaption></figure>

**Check:** the row exists. Its initial state is **INITIALIZED**, which means it
has been created but has not started.
<figure><img src="../.gitbook/assets/guide-instance-initialized.jpg" alt="Instances page with my_temperature_sensor in INITIALIZED state and its row controls."><figcaption><p>Use Start instance on this row to begin continuous execution.</p></figcaption></figure>

## 3. Start and open the device

Click the row's **Start instance** button, then **Open instance details**. The
Instance View opens in another tab. Keep **Continuous** mode selected.

**Check:** the header says **RUNNING**. Open **Attributes**; both input
`k__temperature_c` and telemetry `temperature_c` initially read **20°C**.

## 4. Change the input

Use **Set** on the yellow key-input row `k__temperature_c`, enter **31.25**, then
click **Apply value**. The label may omit `k__`; hover over the name to check its
full path. If columns do not fit, drag the panel divider or scroll the table.
<figure><img src="../.gitbook/assets/guide-sensor-set.jpg" alt="Running sensor Instance View with the Set temperature input popover and value 31.25."><figcaption><p>Write the key input. Applying a value does not by itself prove that model execution updated telemetry.</p></figcaption></figure>

**Check:** after the next model cycle and UI refresh, **both rows read 31.25**.
The curves overlap because this model copies the input to telemetry without noise.
<figure><img src="../.gitbook/assets/guide-sensor-readback.jpg" alt="Full my_temperature_sensor Instance View showing RUNNING, both temperature rows at 31.25 and a chart step."><figcaption><p>The matching telemetry reading confirms that the simulation processed the input.</p></figcaption></figure>

## Finish or continue

For [Connect two instances](connect-instances.md), keep this sensor running.
Otherwise choose **Stop instance**. Delete only this exercise's instance and then
its model if you want to remove them; leave unrelated resources intact.

If the value does not follow, confirm RUNNING, the input's full name and the
successful edit. See [Instances reference](../ui-reference/instances.md).
To author the YAML yourself, use [Create a YAML or JSON model](model-authoring.md).
