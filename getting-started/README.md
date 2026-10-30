---
description: Create one temperature sensor in the browser and verify a 31.25 degree readback.
---

# First device in the UI

## Before you start {#first-device-in-the-ui}

**Prerequisites:** [SPX installed](installation-guide.md), UI open at
`http://localhost:3000`. In [Settings](../ui-reference/settings.md), confirm
**Ready**, the intended upstream target and **Authorization: Accepted by SPX server**.
SPX Setup manages this connection. To change it, rerun Setup and start the
updated environment, then use **Retry** in Settings.

**Result:** instance `my_temperature_sensor` is **RUNNING**; setting its input to
**31.25°C** produces a telemetry reading of **31.25°C**. No MCP, Python or external
protocol client is needed. This is a simulation exercise, not a hardware check.

**Start with [Create and control an instance](../guides/ui-instance.md).**
That is the main walkthrough: load the supplied model file, create the sensor,
start it and verify the temperature. Then keep it running and continue directly
with [Connect two instances](../guides/connect-instances.md).

If you prefer to paste YAML instead of downloading a file, use the alternative
below to prepare the same model, then join the main walkthrough at step 2.

## Create the model {#create-the-model}

This is an alternative to step 1 of the main walkthrough. Use it before creating
the sensor; if you already completed the walkthrough, continue to connections.

1. Open **Models → New model**. In the new Model View, choose **Edit model name**,
   enter `my_temperature_model` and save the name. Use a fresh exercise environment
   if that name already belongs to another model.
2. Select YAML in the editor and paste the complete definition below.
3. Choose **Create model** and check the Validation panel for **OK**.

<!-- model:pt100:start -->
```yaml
name: pt100_demo
description: Minimal deterministic temperature sensor
attributes:
  k__temperature_c:
    type: float
    default: 20.0
    unit: degC
  temperature_c:
    type: float
    default: 20.0
    unit: degC
actions:
  - function: $in(temperature_c)
    name: update_temperature
    call: $in(k__temperature_c)
```
<!-- model:pt100:end -->

The definition's `name` is metadata; the registry name you saved is the model
selected when creating an instance. See [model identifiers](../appendices/glossary-of-terms.md#model-identifiers)
if these names differ in your project.

## Create and start an instance

Continue at **step 2: Create an instance** in
[Create and control an instance](../guides/ui-instance.md). Your model is already
saved, so skip its file-loading step. Follow steps 2–3 to create and start
`my_temperature_sensor`.

## Change an input and verify the result

In step 4 of that walkthrough, set `k__temperature_c` to **31.25** and verify
that `temperature_c` follows to **31.25**. A successful edit alone does not
prove that the model processed the input; check the telemetry readback.

## Finish and continue

Keep `my_temperature_sensor` running for
[Connect two instances](../guides/connect-instances.md); both ways of preparing
the model lead to that exercise. If you are finishing here, stop the sensor.
To remove the exercise, delete its instance and then `my_temperature_model`.
The [UI guide path](../guides/ui.md) lists the later exercises.
