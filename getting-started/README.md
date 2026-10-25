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

This page helps you get up and running with the SPX simulation stack—the SPX Server (REST API for modeling & simulation) and the SPX-Python client (lightweight Python wrapper for that API). You’ll learn how to install the essentials, bring the server up locally with Docker, connect from Python, and perform the core operations you’ll use in day-to-day development and CI.

By the end, you will be able to:

* Start the SPX Server locally via Docker and verify it’s healthy.
* Connect Codex, Claude Code, or another MCP-capable client to your local SPX runtime through the packaged SPX MCP server.
* Initialize the SPX-Python client and talk to the server.
* Create models and instances, read/write attributes, and run a basic simulation step.
* Reuse the same flow in unit tests and CI pipelines.

## Reference repository: spx-examples

For the latest runnable models, installer profiles, generated bundle tooling,
and MiL tests, use the public
[spx-examples repository](https://github.com/HammerHeads-Engineers/spx-examples).

Product installation and bundle generation are owned by private `spx-installer`.
The public Examples repository does not contain the product installer or Compose bundle.

What’s inside this page:

* **Installation Guide** — sign in, download the platform installer, complete the native installation, use the automatically opened `SPX Setup` on macOS, and verify UI/API on localhost. RC qualification uses [staging Downloads](https://staging.simplephysx.com/downloads), channel **Development**, and a key from [Product Keys](https://staging.simplephysx.com/account/product-keys).
* **Connect an LLM with SPX MCP** — run `SPX MCP Setup`, open the generated SPX MCP workspace, and use MCP tools against the local SPX server.
* **Advanced: Manual Docker Compose** — run the SPX Server API via Compose without the wizard (server-only).
* **Modbus Client / PLC Controller** — use SPX as an active Modbus master that polls and controls downstream Modbus devices.
* **Quick Start Guide** — minimal, copy-paste recipes to connect to the server, do basic CRUD on models/instances, tweak attributes, run prepare()/run(), and wire these steps into your unit tests and CI.

**Who is this for?**

Developers, QA, and CI engineers who want a clear, repeatable path to stand up SPX locally and automate it in tests.

Prerequisites (at a glance):

* Docker & Docker Compose (to run the server)
* Native macOS and Windows installers provide Python 3.12; no separate Python installation is needed for that path
* Portable/Linux MCP requires host Python `>=3.10`; use Python 3.12 for public repository development
* A valid `SPX_PRODUCT_KEY`
* Network access to pull Docker images and install Python dependencies

> Tip: Everything shown here is designed to work the same way locally and in CI, so the commands you practice on your laptop carry straight over to pipelines.

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
