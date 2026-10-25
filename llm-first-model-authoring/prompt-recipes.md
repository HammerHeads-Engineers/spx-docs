---
description: Ready prompts for live MCP results, persistent model contributions and tests.
---

# Prompt recipes

Choose the task first. `runtime_mcp` means a live result; `repo_dev` means a
persistent repository change. Both can be performed by a local agent. A web-only
assistant should produce a patch/instructions and state which checks remain unrun.

Read [Agent Start Here](agent-start-here.md),
[Examples AGENTS.md](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/AGENTS.md),
[modeling playbook](https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md)
and [canonical model language](../simulation-and-modeling/model-definition-reference.md)
when applicable. Runtime tools are described in the [MCP reference](../getting-started/mcp-reference.md).

## Live runtime task

**Mode:** runtime_mcp. **Requires:** a connected MCP workspace and running server.
**Completion:** requested live behavior; normally the instance is RUNNING.

```text
Use runtime_mcp in this workspace. Goal: <requested live simulation result>.
Read the workspace AGENTS.md and use its host-managed SPX MCP tools.
Inspect health, actual model/instance keys and available tool schemas first.
Reuse the closest catalog model; validate only the touched model if needed.
Register/ensure the model and instance, start it and verify the requested result.
Do not change repository catalogs, packs or tests unless I request persistence.
Do not run protocol smoke tests unless requested or needed to diagnose failure.
Report the model ID, instance key, final state and relevant endpoint details.
State what you actually verified and stop when the requested live result works.
```

<a id="id-2-create-a-new-model-copy-the-closest-template"></a>
## Durable model contribution

**Mode:** repo_dev. **Requires:** a public Examples checkout and the input manual
or behavior specification. **Completion:** a reviewable change and relevant checks.

```text
Use repo_dev in public spx-examples. Goal: <durable model change>.
Read AGENTS.md, docs/LLM_SPEC.md and the generated docs/MODEL_LANGUAGE.md.
Start from <closest model or discovery task>. Inputs/manual: <path or URL>.
Implement only <attributes, behavior and protocol subset>.
Follow naming, units and instance-specific communication parameter conventions.
Update catalog/pack metadata and tests where required by repository instructions.
Run validation and the relevant tests using the actual project environment.
Do not hand-edit generated docs/MODEL_LANGUAGE.md or docs/MCP.md.
If canonical documentation needs changing, propose that in spx-docs first,
then refresh offline exports through the existing synchronization mechanism.
Report changed files, source revisions, actual checks and any remaining limits.
```

<a id="id-1-generate-a-model--protocol-mapping-from-device-protocol-documentation"></a>
## Adapt a device from its manual

**Mode:** runtime_mcp for a local result, repo_dev only when persistence is requested.
Provide the smallest useful register/topic/endpoint subset and cite manual sections.

```text
Goal: simulate <device> for <SUT/use case>. Mode: <runtime_mcp or repo_dev>.
Manual: <path or URL>; closest model: <path or ask the agent to find one>.
Implement the minimum useful telemetry, setpoint, command and status subset.
Preserve the closest model's behavior unless the device needs a specific change.
Do not invent register addresses or protocol fields. Ask about essential gaps.
Parameterize deployment host/port/IDs and follow the selected mode's stopping rule.
Report model/instance identity and executed checks. Persist only if requested.
```

## Connect instances

**Mode:** runtime_mcp. **Completion:** RUNNING connection and observed propagation.

```text
Connect <source behavior> to <target behavior> in the live server.
Inspect actual instance keys and attributes before choosing endpoints.
Use structured MCP connection tools, telemetry as the source and a persistent
control input as the target. Use replace=true and start=true for this wiring.
Ensure the global connection container is running, then change the source or
run the connection and read back the target. Report state and observed values.
Do not persist a model/catalog change unless I ask.
```

<a id="id-4-add-faults--mil-tests-scenarios-are-the-contract"></a>
## Add a fault and regression test

**Mode:** repo_dev for a persistent fault/test; use the live recipe for an experiment.

```text
In public spx-examples, add <fault/scenario> to <model> and test <expected SUT behavior>.
Follow AGENTS.md and the current model language. Specify clock control, inputs,
random seeds and the expected state before, during and after the disturbance.
Reuse existing SUT helpers and update only relevant model/catalog/test files.
Keep docs/LLM_SPEC.md changes local to contribution rules; product syntax changes
belong upstream in spx-docs and generated MODEL_LANGUAGE/MCP exports stay read-only.
Run the relevant validation/tests if tools are available; otherwise provide exact
commands and state that they were not run. Report evidence, not assumed success.
```

<a id="id-3-add-protocol-mapping-to-an-existing-model"></a>
<a id="id-5-generate-a-mil-integration-test-for-an-existing-model"></a>
<a id="id-6-generate-client-software-integration-tests-against-an-spx-model-mil"></a>
<a id="id-7-generate-production-device-tests--report-_test_logs"></a>
## Check an existing protocol mapping

**Mode:** runtime_mcp for live verification, repo_dev for a saved regression test.

```text
Verify <protocol read/write behavior> on <instance or model> using <SUT/client>.
Inspect endpoint, namespace/unit/topic and codecs before the exchange.
Verify actual protocol readback and writes in addition to control-API values.
Report versions, backend, observed values and any hardware not exercised.
For repo_dev, save the smallest regression test and required metadata;
for runtime_mcp, stop after the requested verification without repo hardening.
```

## Prepare a patch without local tools

**Access:** web-only. Choose the same task mode, but do not claim local execution.
Provide a file-by-file patch, source URLs/revisions and exact validation commands.
List checks that remain unrun. Do not transform a local runtime request into a
repository contribution simply because the assistant lacks MCP access.

<a id="id-0-update-documentation-from-source-repos-single-branch-automation"></a>
## Documentation maintenance

Product documentation maintenance is a separate task for spx-docs. Maintainers
use the [automation contract](https://github.com/HammerHeads-Engineers/spx-docs/blob/main/llm-first-model-authoring/docs-automation-guidelines.md)
and [maintenance guide](https://github.com/HammerHeads-Engineers/spx-docs/blob/main/docs/documentation-maintenance.md).
Catalog bot branches are not general model-authoring branches.
