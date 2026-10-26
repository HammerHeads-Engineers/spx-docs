---
description: Automate server setup and assertions with Python, then test real protocol behavior.
---
# Automate with Python

Use `spx-python` to control a running SPX Server. Use the SDK path when you want
to run model logic in your own Python process instead.

| Order | Guide | Expected result |
| --- | --- | --- |
| 1 | [First Python program](../simulation-and-modeling/using-spx-python.md) | Three controlled-time samples at 31.25°C, with cleanup. |
| 2 | [Create and control a simulation](../getting-started/build-your-first-simulation.md) | Understand setup, inputs, execution and readback. |
| 3 | [Connect instances with Python](python-connections.md) | Target readbacks of 28°C and 34°C. |
| 4 | [Test a client over Modbus](../getting-started/use-in-unit-tests-mil.md) | The real TCP client reads both expected temperatures. |
| 5 | [Run tests in CI](../getting-started/ci-cd-setup-github-actions.md) | A disposable runtime, assertions and teardown on a runner. |

Read [Model-in-the-Loop concepts](../simulation-and-modeling/model-in-the-loop.md)
and [Testing practices](../testing-and-validation.md) for scope and assertions.
The [UI path](ui.md) shows the equivalent manual operations.

## Read diagrams, run code and check results

Use Python 3.12 and the [documented package versions](../release-notes.md).
Reserve each script's demo names on a disposable server. Keep product keys in
your environment; screenshots never need to contain a real key.

Diagrams explain execution order, data flow and the boundary between a local
SDK model and a model on SPX Server. Their captions and alternative text describe
the same relationships for agents and screen readers. Commands, complete source
and expected results are copyable text; tables explain how outputs follow inputs.

Run the example in your own environment and compare the values and completion
checks. A diagram or expected-output block is not an execution record of your run.
Protocol verification is explicitly identified; a UI/API read does not prove Modbus.
