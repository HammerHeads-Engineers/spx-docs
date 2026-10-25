# Agent Start Here

Read this before selecting a workflow or interpreting a model example as a rule.
The current product contract is the [released version set](../release-notes.md).

## Source order

1. User intent selects the task and whether the result must persist.
2. Workspace `AGENTS.md` provides operating rules and mode resolution.
3. Canonical [model language](../simulation-and-modeling/model-definition-reference.md)
   and [MCP reference](../getting-started/mcp-reference.md) define documented contracts.
4. Public Examples `docs/LLM_SPEC.md` defines contribution conventions; the
   generated offline references identify their canonical Docs commit.
5. Examples illustrate use; an older example does not override a normative rule.

Match behavior to the installed bundle. Newer catalog content does not implicitly
upgrade server, SDK, client or installed MCP modules. Do not infer work mode from
a running server or MCP availability alone.

## Choose the task and stopping point

| Task | Workspace/repository | Completion |
| --- | --- | --- |
| Live model/instance/connection work | managed workspace, `runtime_mcp` | Requested live result; normally valid model, instance RUNNING, reported keys/endpoints. Connections must be RUNNING and propagate. Protocol verification only when requested or needed to diagnose failure |
| Durable model/library contribution | public Examples, `repo_dev` | Relevant model, catalog/pack updates and tests; validator passes; follow repo instructions |
| Product documentation | spx-docs/main | Source-backed prose, working examples, navigation and applicable checks |
| Installation/packaging/signing | private spx-installer | Maintainer workflow, not public Examples compatibility shims |

For runtime tasks prefer host-managed MCP tools. Inspect exact instance keys and
attribute names before writes. Use structured connection endpoints, telemetry as
sources and persistent `k__*` controls as continuous targets. A one-shot `cmd__*`
is not an ordinary continuous input. Do not add repo tests/catalogs merely to
finish a local experiment; persist only when requested.

## Names, layers and clocks

Use the [identifier glossary](../appendices/glossary-of-terms.md#model-identifiers)
to distinguish catalog ID, definition name, model registry key and instance key.
SDK Model is a Python object; spx-python is an HTTP proxy; runtime Model is the
hosted execution object. Their APIs are related but not identical.

`$in`/`$ext` select value wrappers, not read/write permissions. An internal write
clears an external override. A controlled clock does not seed random generators.
Snapshot import rebuilds structure and defaults, not a runtime checkpoint.

## Validation claims

Separate YAML/JSON parsing, catalog validation, SDK execution, runtime/API checks,
protocol exchange and physical-hardware verification. Report exactly which ran.
There is no complete published JSON Schema covering every DSL extension and
adapter. Use the validator plus runtime registration; a schema or parser passing
alone does not prove arbitrary adapter fields are supported.
