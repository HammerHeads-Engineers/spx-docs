# Glossary of Terms

- **SPX Server**: the runtime that hosts Models and runs Instances, exposing the REST API (default `http://localhost:8000`).
- **SPX SDK**: Python package for authoring/validating model definitions and implementing custom classes (actions/components).
- **SPX UI**: browser frontend for inspecting and operating a running SPX Server.
- **spx-python**: Python client wrapper for controlling SPX Server (dict-like interface over Models/Instances and helpers for tests).

- **Model**: a definition (usually YAML) describing attributes, actions, communication adapters, timers, and scenarios.
- **Instance**: a running copy of a Model with live state you can read/write.
- **Attribute**: a named value in a model/instance. Many models distinguish **internal** (true state) vs **external** (presented value with noise/faults).
- **Action**: a step that runs each simulation tick and mutates attributes (built-in or custom).
- **Scenario**: a repeatable script of events (fault injection, parameter steps, sequencing) executed against an Instance.
- **MiL test**: “Model-in-the-Loop” test where SPX is the deterministic plant/device and your Software Under Test is the real client.
- **Snapshot**: captured simulation state that can be restored to get a known starting point for tests/debugging.
- **Protocol adapter**: a communication block (Modbus/MQTT/HTTP/ASCII/BLE, etc.) that exposes the simulation over a real interface.
