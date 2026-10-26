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

## Execution and screenshots

Use Python 3.12 and the [documented package versions](../release-notes.md).
Reserve each script's demo names on a disposable server. Keep product keys in
your environment; screenshots never need to contain a real key.

The code-guide execution screenshots show reports captured from actual released
SDK/client/runtime runs. They are labeled as execution records, rather than SPX
application screens. Full commands and expected outputs remain copyable in text.
Protocol proof is explicitly identified; a UI/API read does not prove Modbus.
