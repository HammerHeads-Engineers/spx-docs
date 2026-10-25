---
description: Connect an agent, choose runtime or repository work, and use a matching prompt.
---

# Agents & MCP

## Connect your agent

[Connect your MCP client](../getting-started/connect-llm-with-spx-mcp.md) to the
installed environment, then read [Agent Start Here](agent-start-here.md).

## Choose the result

- **Live result — runtime_mcp:** operate the running server. Use the
  [runtime prompt](prompt-recipes.md#live-runtime-task). Stop at the requested
  live result; promote it to a repository only when asked.
- **Durable contribution — repo_dev:** change public Examples. Use the
  [repository prompt](prompt-recipes.md#id-2-create-a-new-model-copy-the-closest-template),
  [model brief](model-brief-template.md) and
  [completion criteria](definition-of-done.md).

A local agent may do either task. A web-only assistant can prepare instructions
or a patch, but cannot report local execution it did not perform. Tool access is
separate from the purpose of the work.

## Source ownership

This portal defines product behavior. Public Examples owns model/contribution
rules and runtime MCP modules. Private spx-installer owns setup, client
provisioning and releases. Generated offline references are updated from Docs,
not edited by hand. See the [source order](agent-start-here.md#source-order).

## Continue with…

[Prompt recipes](prompt-recipes.md) for a ready task, or
[MCP reference](../getting-started/mcp-reference.md) for individual tools.
