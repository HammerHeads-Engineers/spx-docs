# Model

`from spx_sdk.model import Model` imports SDK RC21's `BaseModel` alias. It is
an in-process Python container with a `SimpleTimer` and `SimplePolling`, useful
for testing actions and model logic without an HTTP server.

SPX Server RC76 implements `spx_core` and `spx_server` in Python on top of SDK
components. Its server packaging uses Cython compilation. Compilation does not
mean that the runtime is written in Rust or Go. This release reference makes
no promise of distributed clocks or multi-tenant orchestration.

## Run a local model

Follow the complete, executable [SDK Quickstart](../quick-start-spx-sdk-in-5-minutes.md).
It includes all files, dependencies, equivalent YAML/JSON/dict variants and
expected values. Import custom action modules before loading their definitions.

## SDK versus server runtime

| Concern | Local SDK Model | Server runtime Model |
| --- | --- | --- |
| Execution | Direct Python objects | Hosted component tree controlled through API/MCP/UI |
| Timer | SimpleTimer; local object assignment | Runtime Timer; HTTP proxy property setter |
| Lifecycle | Base SDK behavior | Pause gates, explicit single step, resume transaction |
| Services | Only components imported into the process | Model/instance registries, protocols, logs, scenarios and snapshots |
| Verification | Tests local logic | Tests actual API, provisioning and transport behavior |

A successful local SDK test does not prove a protocol works in the container.
Validate runtime-specific behavior on the released server and protocol behavior
with the relevant SUT. See [protocol capabilities](../../spx-core/communications/capabilities.md)
and [client stepping](../../simulation-and-modeling/using-spx-python.md).
