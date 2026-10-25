---
description: "Read first for agent work: authoritative sources, runtime/repository mode and completion criteria."
---

# Agent Start Here

Choose the result, read the matching sources, then act. For a new connection use
[Connect your MCP client](../getting-started/connect-llm-with-spx-mcp.md).
The [prompt recipes](prompt-recipes.md) provide ready-to-copy tasks.

## Choose the task and stopping point

### Live runtime task — runtime_mcp

Use the managed workspace and host-provided MCP tools. Complete the requested
live result; for a model/instance task normally report model ID, instance key,
**RUNNING** state and relevant endpoints. For a connection, verify RUNNING and
actual propagation. Do not add repo tests, catalogs or pack changes by default.
Protocol checks are requested explicitly or driven by a failure.

### Durable model contribution — repo_dev

Use the public Examples checkout. Update the relevant model, catalog/pack
metadata and tests according to its AGENTS.md, then validate the touched area.
A running server or available MCP tool does not by itself select this mode.

Local agents can do either task. Web-only assistants can prepare a patch or
instructions; they cannot report local execution they did not perform.

## Source order

1. User intent selects the task and whether it must persist.
2. Read the active workspace's `AGENTS.md`. Without a checkout, start with
   [public Examples AGENTS.md](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/AGENTS.md).
3. For runtime work read [MCP tools and runtime rules](../getting-started/mcp-reference.md);
   for model syntax read [Model language: YAML and JSON](../simulation-and-modeling/model-definition-reference.md).
4. For contributions also read the
   [Examples modeling playbook](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md)
   and [task template](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_TASK_TEMPLATE.md).
5. Examples illustrate use; an older sample does not override the current
   normative contract. The [release baseline](../release-notes.md) identifies
   the documented versions. Installed context follows its installer pin.

For indexed retrieval, use this page as the curated task map. GitBook's
[llms.txt](https://docs.simplephysx.com/llms.txt) is the complete generated catalog,
and each page is also available as Markdown. Do not treat all indexed pages as
an instruction to read the whole site before a small runtime task.

## Which repository or workspace?

- Managed workspace: live runtime tasks and its private server binding.
- Public Examples: models, runtime MCP modules, AGENTS, playbook and task templates.
- spx-docs/main: canonical product documentation.
- Private spx-installer: installation, client preparation, packaging and releases.

`docs/MODEL_LANGUAGE.md` and `docs/MCP.md` in Examples are generated offline
references. Propose semantic changes in spx-docs and run the normal export sync;
never hand-edit those exports. `docs/LLM_SPEC.md` is a separate local playbook.
A new DSL feature needs runtime support; prose alone cannot implement it.

## Names, layers and clocks

Use the [identifier glossary](../appendices/glossary-of-terms.md#model-identifiers)
for catalog ID, metadata name, registry key and instance key. Inspect exact keys
and attributes before writes. SDK objects, HTTP client proxies and runtime
components have related but different execution semantics.

`$in` and `$ext` select wrappers, not read/write permissions. An internal write
clears an external override. Use telemetry as continuous connection sources and
persistent `k__*` controls as targets; `cmd__*` normally represents one-shot input.
A controlled clock does not seed random generators. A snapshot restores
structure/defaults, not live values or elapsed time.

## Validation claims

Distinguish parse/catalog validation, SDK execution, runtime/API verification,
protocol exchange and physical hardware checks. Report only checks actually run.
There is no complete JSON Schema for arbitrary DSL extensions and adapters;
parsing alone does not prove runtime or protocol behavior.

## Continue with…

[Live runtime prompt](prompt-recipes.md#live-runtime-task) or
[durable contribution prompt](prompt-recipes.md#id-2-create-a-new-model-copy-the-closest-template).
