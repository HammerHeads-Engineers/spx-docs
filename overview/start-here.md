# Start here (by role)

Choose one path. Each path points to its next step; use the remaining chapters
as reference rather than completing every introduction.

| Your goal | Start | Expected first result |
| --- | --- | --- |
| Operate SPX in the browser | [Install](../getting-started/installation-guide.md), then [UI first device](../getting-started/README.md#first-device-in-the-ui) | One instance is RUNNING and shows readable attributes |
| Work with an agent through MCP | [MCP setup](../getting-started/connect-llm-with-spx-mcp.md), then [Agent Start Here](../llm-first-model-authoring/agent-start-here.md) | Agent reports health, model ID, instance key and final state |
| Write tests or extensions | [Python client](../simulation-and-modeling/using-spx-python.md) for server control, or [SDK Quickstart](../spx-development-guide/quick-start-spx-sdk-in-5-minutes.md) for local logic | Program prints its documented values and cleans up |

For protocols, continue to [capabilities and prerequisites](../spx-core/communications/capabilities.md)
and then the selected adapter. Check actual read/write behavior with your SUT.

## Which repository or workspace?

- **Managed MCP workspace:** installed by SPX Tools; `runtime_mcp` for live work.
  Runtime experiments are local unless explicitly promoted to a repository.
- **Public spx-examples checkout:** models, catalogs, packs, examples, tests,
  runtime MCP modules and agent instructions; `repo_dev` for durable contributions.
- **Private spx-installer:** product setup, Python/client provisioning, bundle
  generation, signing and publication. Users obtain it through Downloads.
- **spx-docs:** canonical product behavior and instructions. Public Examples
  contains generated offline references linked to a specific Docs commit.

The latest public library can be newer than the context bundled by your
installer. Use [Release Notes](../release-notes.md) and the
[version matrix](system-requirements-and-capability.md) to identify your combination.
Snapshot restore recreates configuration, not live values or warmup state.
