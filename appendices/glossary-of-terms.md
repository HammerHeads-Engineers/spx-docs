# Glossary of Terms

- **SPX Server**: the runtime that hosts Models and runs Instances, exposing the REST API (default `http://localhost:8000`).
- **SPX SDK**: Python package for authoring/validating model definitions and implementing custom classes (actions/components).
- **SPX UI**: browser frontend for inspecting and operating a running SPX Server.
- **spx-python**: Python client wrapper for controlling SPX Server (dict-like interface over Models/Instances and helpers for tests).
- **spx-examples**: the canonical models + MiL tests repository; a practical contract for conventions and validation.
- **Registry**: the SDK’s class registry used to map names in YAML to Python classes at runtime.
- **Extension**: custom Python code (typically under `./extensions`) mounted into the server and registered via the registry.

- **Model**: a definition (usually YAML) describing attributes, actions, communication adapters, timers, and scenarios.
- **Instance**: a running copy of a Model with live state you can read/write.
- **Attribute**: a named value in a model/instance. Many models distinguish **internal** (true state) vs **external** (presented value with noise/faults).
- **Internal value**: the “true” simulation state used by model logic and dynamics.
- **External value**: the value exposed to the outside world (protocol adapters/UI); often includes noise, faults, or scaling.
- **Action**: a step that runs each simulation tick and mutates attributes (built-in or custom).
- **Condition**: an `if` rule that triggers actions when a predicate becomes true.
- **Hook**: a lifecycle or attribute-event callback that runs a component when something changes (prepare/run/start/on_set, etc.).
- **Scenario**: a repeatable script of events (fault injection, parameter steps, sequencing) executed against an Instance.
- **Fault**: a scenario (or scenario step) that intentionally degrades behavior (timeouts, overrange, disconnect, noise, stuck values).
- **MiL test**: “Model-in-the-Loop” test where SPX is the deterministic plant/device and your Software Under Test is the real client.
- **Snapshot**: saved configuration/structure, not a checkpoint of runtime attribute values, timer progress, threads or external sessions.
- **Protocol adapter**: a communication block (Modbus/MQTT/HTTP/ASCII/BLE, etc.) that exposes the simulation over a real interface.
- **Communication binding**: a mapping between an Attribute and a protocol-level representation (register, topic, endpoint, GATT characteristic).
- **Domain**: a top-level category for models (as in `library/domains/<domain>/...`).
- **Service**: an external dependency required by a model/profile (MQTT broker, BLE adapter, etc.); typically declared in catalogs.
- **Catalog**: curated YAML lists that describe available models/domains/services and metadata for installers/profiles.
- **Installer**: SPX Setup from the private spx-installer product that builds a runnable bundle from selected packs or profiles.
- **Bundle**: the generated installer output (includes `bundle.json`, compose files, scripts, models, and assets).
- **spx-start / spx-stop**: generated scripts that start and stop an installer bundle and run bootstrap steps.
- **Assets**: supporting files copied into a bundle (configs for MQTT/KNX/Home Assistant, etc.).
- **Profile**: a selection of models/services used for running a scenario set or CI pack (in spx-examples: `profiles/<pack>/*.yaml`).
- **Pack**: a curated bundle of domains/models/profiles/tests intended to be used together (in spx-examples: `library/catalog/industries.yaml`).
- **Timer**: a time base component used for deterministic stepping (`time_step`/`step`, current time; see the Timer reference).
- **Polling**: a background runner used by some components/adapters; should not replace MiL-driven deterministic stepping for model behavior.
- **Determinism**: the property that simulation results depend only on inputs and the simulated time progression (not wall-clock timing).

## Model identifiers

These identifiers are related but not interchangeable. Example from the pinned
public MQTT environment sensor, registered as `env_demo` and instantiated as
`room_sensor`:

| Identifier | Example | Meaning |
| --- | --- | --- |
| File | `library/domains/environment/sensor/generic/environment_sensor__mqtt.yaml` | Storage path; not a server lookup key |
| Definition `name` | `environment_sensor__mqtt` | Metadata inside the definition |
| Catalog ID (`model_id` in discovery tools) | `Env.EnvSensor.Mqtt` | Identifier in `library/catalog/models.yaml` (field `id`) |
| Registry model key | `env_demo` | Key assigned under `client["models"]` |
| Instance key | `room_sensor` | Key assigned under `client["instances"]` using `env_demo` |
| Attribute path | `room_sensor.temperature_c` | Instance plus an actual attribute; inspect the loaded model for its names |

Registering a definition does not require its registry key to equal its filename,
metadata name or catalog ID. Query the actual catalog or server tree before
wiring instances. An OpenAPI schema is a description of an HTTP payload, not a
simulation device.
