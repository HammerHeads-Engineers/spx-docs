---
description: Follow complete browser workflows, from one sensor to a connected energy simulation.
---
# Work with the UI

Use this path to operate SPX in the browser. Start with one device, then connect
instances and observe a small energy system. No Python or MCP client is required.

| Order | Guide | You will finish with |
| --- | --- | --- |
| 1 | [Create and control an instance](ui-instance.md) | A running sensor whose telemetry follows your input. |
| 2 | [Connect two instances](connect-instances.md) | A verified source-to-target signal path. |
| 3 | [Build a building-energy simulation](ui-building-energy.md) | Five running instances and seven active connections. |
| 4 | [Observe signals and test behavior](ui-observe.md) | Two charts showing the effect of changing daylight. |
| 5 | [Run a scenario](run-scenarios.md) | A controlled 20 → 80 → 20°C disturbance. |
| 6 | [Save and restore a configuration](ui-save-restore.md) | A restored structure that you explicitly restart and check. |

If you have completed [First device in the UI](../getting-started/README.md),
keep `my_temperature_sensor` running and continue at **2. Connect two instances**.

## Before the exercises

[Install SPX](../getting-started/installation-guide.md) and open
`http://localhost:3000`. In [Settings](../ui-reference/settings.md), confirm
**Ready**, the intended upstream target and **Authorization: Accepted by SPX server**.
SPX Setup manages the connection; to change it, rerun Setup and start the
updated environment, then choose **Retry** in Settings. Screenshot ports belong
to an isolated documentation workspace; use your installation's configured address.

Use a disposable workspace. Exercises 1–2 need one model and two instances;
the energy example needs capacity for five models and five instances. Its import
replaces models, instances and connections. Export any configuration you need first.

Screenshots show the real released UI RC76. They retain the application view,
page title or instance header, and the relevant selection. Open an image to
inspect small labels. On narrower windows some tabs move into **More tabs** (…).
The numbered text, exact runtime names and completion checks are the same on
all screen sizes and are also the instructions for an agent.

## Reading values correctly

`k__temperature_c` is a persistent input; `temperature_c` is telemetry. The UI
may shorten both labels to “temperature”. Yellow key styling and the full-name
hover hint help identify the input. **Set** in these exercises writes Internal;
connections read External telemetry and write Internal inputs.

A running status alone does not prove the exercise worked: perform the value
change and check the documented result. For automation use
[Python](python.md); for tools and runtime rules use [Agents & MCP](../llm-first-model-authoring/agent-start-here.md).
