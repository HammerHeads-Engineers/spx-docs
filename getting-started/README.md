---
description: Get up and running with the SPX simulation stack.
icon: flag-checkered
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Getting Started

Choose your workflow in [Start here](../overview/start-here.md). This page
contains the browser/UI first-device walkthrough.

Install with [SPX Setup](installation-guide.md), verify the UI/API, then follow
the steps below. For agents use [MCP onboarding](connect-llm-with-spx-mcp.md);
for code use the [client tutorial](../simulation-and-modeling/using-spx-python.md).
The [version matrix](../overview/system-requirements-and-capability.md) explains
which Python belongs to the installer, MCP, SDK or server container.

Public [spx-examples](https://github.com/HammerHeads-Engineers/spx-examples)
contains models, catalogs, profiles, examples and runtime MCP modules. Bundle
generation and product installation belong to private `spx-installer`.

## First device in the UI

For a basic communication check, select Modbus, MQTT, BACnet, KNX or OPC UA in
local Setup, enable model installation and SPX UI, then start the stack. Protocol
selection installs models but does not automatically create device instances.

1. Open `http://localhost:3000/instances` and choose **New instance**.
2. Select a model from the table below, enter an instance name, and keep its
   default communication meta parameters for a local test.
3. Create and start it. Open its details and verify **RUNNING**,
   **Attributes** and **Communication**.
4. Connect a protocol client using the listed endpoint; read a value, change
   the control input and check the readback in both the client and SPX UI.

| Protocol | Model | Local endpoint and control input |
|---|---|---|
| Modbus TCP | `Process.ThermalController.Modbus` | port 502, unit 1; holding registers 2–3, big-endian Float32 `setpoint` |
| MQTT | `Building.RobotVacuum.Mqtt` | port 1883; publish `1` to `spx/examples/robot_vacuum/command/desired_cleaning`, observe `telemetry/cleaning_active`, then publish `0` |
| BACnet/IP | `Building.HvacFlexitNordic.Bacnet` | UDP 47808, device 2; analogValue 1994 `presentValue` |
| KNXnet/IP | `Building.RoomController.Knx` | UDP 3671 tunnel; temperature at `2/0/1`, setpoint at `2/0/2`, DPT 9.001 |
| OPC UA | `Building.BMSController.OpcUa` | `opc.tcp://localhost:4843/spx/bms-controller`; namespace `urn:spx:examples:opcua:bms-controller`, node `BMS/HVACMode` (`auto`/`heating`) |

The Community limit is five instances. These five examples can run together.
MQTT telemetry is published when values change; without retained messages a
late subscriber may need to send a command before receiving telemetry.

Save a disk snapshot before replacing your stack. **Restore** recreates
configuration and resets runtime measurements; manually start the restored
instances. **Connections** represents links between SPX attributes, rather
than the device's protocol adapters.

## Next steps on simplephysx.com

Explore the main protocol simulator pages for SPX runtime workflows:

* [MQTT Simulator](https://www.simplephysx.com/mqtt-simulator)
* [Modbus TCP Simulator](https://www.simplephysx.com/modbus-simulator)
* [OPC UA Simulator](https://www.simplephysx.com/opc-ua-simulator)
* [BACnet Simulator](https://www.simplephysx.com/bacnet-simulator)
* [KNX Simulator](https://www.simplephysx.com/knx-simulator)
