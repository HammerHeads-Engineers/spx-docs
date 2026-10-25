---
description: Start and stop an existing scenario and inspect its expected effect.
---

# Run an existing scenario

**Prerequisites:** a running instance whose model defines a scenario. The small
[first UI sensor](../getting-started/README.md) does not include scenarios; choose
a model with a documented scenario from the [catalog](../usage-scenarios-and-examples/device-catalog.md).

**Result:** you observe that scenario's documented effect and confirm what is
restored or retained after stopping it. Do not assume all models define faults.

1. Open the instance details and its **Scenarios** tab.
2. Read the scenario description and note the attributes or adapter behavior it affects.
3. Record the baseline, start the chosen scenario and inspect its state and effect.
4. Stop it, or wait for its documented duration, then inspect the resulting values.

An override can restore the previous value on stop; an ordinary action may leave
its write in place. For manual-clock tests advance the clock using the
[verified client loop](../simulation-and-modeling/using-spx-python.md), not wall-clock waits.

Do not use a snapshot as a checkpoint for scenario progress. Snapshot restore
rebuilds configuration; runtime inputs and warmup must be applied explicitly.
See the [scenario reference](../spx-core/system/scenarios.md) for configuration
and [prompt recipes](../llm-first-model-authoring/prompt-recipes.md) for agent tasks.
