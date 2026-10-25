---
description: Wire a telemetry output to another instance and verify propagation.
---

# Connect two instances

**Prerequisites:** complete [First device in the UI](../getting-started/README.md),
then create a second instance of the same model named `second_temperature_sensor`
and start it. Keep your original instance running.

**Result:** changing the first sensor's input changes the second sensor's telemetry.
This connects runtime instances; it does not require editing model files.

1. Open **Connections** and choose **Add connection**.
2. Select **From**: `my_temperature_sensor`, attribute `temperature_c`, External.
3. Select **To**: `second_temperature_sensor`, attribute `k__temperature_c`, Internal.
4. Save the connection as `temperature_link` and enable it.
5. Set the first instance's internal `k__temperature_c` input to **28.0**.
6. Confirm the second instance's input and `temperature_c` telemetry both become **28.0**.

If values do not move, inspect the connection/container state and start them if
initialized. Do not confuse **Enabled** with a running propagation container.
For agent-driven work use the structured connection tools and lifecycle checks
in the [MCP reference](../getting-started/mcp-reference.md).

Disable/delete only `temperature_link` when finished. Stop the second demo
instance if you no longer need it. See the [Connections UI reference](../ui-reference/connections.md)
and [runtime reference](../spx-core/system/connections.md) for all fields.

## Continue with…

[Run a scenario](run-scenarios.md) for a temporary disturbance, or
[First Python program](../simulation-and-modeling/using-spx-python.md) for automated assertions.
