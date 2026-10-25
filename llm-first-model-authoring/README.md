# LLM-first model authoring

Start with [Agent Start Here](agent-start-here.md). Choose the mode before asking
an agent to change a model or control the running server.

- **Live work:** use the installed MCP workspace and `runtime_mcp`. Stop at the
  requested runtime result; repository changes are optional promotion work.
- **Durable contribution:** use public Examples and `repo_dev`. Read its
  `AGENTS.md`, `docs/LLM_SPEC.md` and generated `docs/MODEL_LANGUAGE.md`; update
  models, catalogs, packs and tests as required by that repository.
- **Documentation:** edit spx-docs/main and follow the
  [docs automation guidelines](docs-automation-guidelines.md).

Public [spx-examples](https://github.com/HammerHeads-Engineers/spx-examples)
contains authoring context and runtime MCP modules. Installation, client
provisioning and releases belong to private spx-installer. Product documentation
is canonical here; offline copies in Examples identify the source commit.

For durable work use the [Model Brief](model-brief-template.md),
[generate/validate workflow](workflow-generate-validate-iterate.md),
[prompt recipes](prompt-recipes.md) and [definition of done](definition-of-done.md).
For live setup use [MCP onboarding](../getting-started/connect-llm-with-spx-mcp.md).
