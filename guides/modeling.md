---
description: Author definitions and extend behavior with complete, executable examples.
---
# Develop models and extensions

Choose a ready-made [catalog model](../usage-scenarios-and-examples/device-catalog.md)
when it already meets your needs. Use this path to create or change behavior.

| Order | Guide | You will verify |
| --- | --- | --- |
| 1 | [Model concepts](../simulation-and-modeling/core-concepts.md) | Definitions, instances, wrappers and execution. |
| 2 | [Create a YAML or JSON model](model-authoring.md) | Equivalent definitions and a running UI test instance. |
| 3 | [Local model with SDK](../spx-development-guide/quick-start-spx-sdk-in-5-minutes.md) | A temperature curve ending at about 97.48°C. |
| 4 | [Write a custom action](../getting-started/extend-with-custom-component.md) | A seeded per-instance contact-fault sequence. |
| 5 | [Custom actions and logic](../simulation-and-modeling/extending-simulations/custom-actions-and-logic.md) | A hysteresis action that retains state between thresholds. |
| 6 | [Load a Python class](../getting-started/code-defined-simulations.md) | A property updated by a mapped lifecycle method. |
| 7 | [Filter a signal](../simulation-and-modeling/extending-simulations/filters-and-signal-processing.md) | A three-sample moving average. |
| 8 | [Test and reload extensions](../simulation-and-modeling/extending-simulations/testing-and-hot-reload.md) | A fresh execution of changed code and recreated runtime instances. |

Use the [model language reference](../simulation-and-modeling/model-definition-reference.md)
for complete syntax. For a contribution to public Examples, also follow its
`AGENTS.md`, modeling playbook, catalog rules and validation workflow; see
[Contribute to Examples](../llm-first-model-authoring/repo-as-spec.md).

The examples below execute locally with the SDK unless a step explicitly says
server. Copying a Python module to your laptop does not install it inside a server
container. See the [Python path](python.md) for remote lifecycle and cleanup.
