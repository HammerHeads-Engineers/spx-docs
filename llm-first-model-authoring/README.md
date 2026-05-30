---
icon: brain-circuit
---

# LLM-first model authoring

LLM-first authoring in SPX means:

* an LLM accelerates drafting YAML + tests,
* **MiL tests** are the quality gate,
* `spx-examples` is the contract for structure, naming, and validation.

Treat `spx-examples` as a repo-as-spec:

* Repo root (main): https://github.com/HammerHeads-Engineers/spx-examples/tree/main
* Spec: `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/LLM_SPEC.md`
* Modeling language: `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md`
* Task template: `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/LLM_TASK_TEMPLATE.md`

What you ship is not “a model”, it’s a **model + tests + catalog entries** that stays stable under deterministic stepping.

For runtime-first work after installing SPX, start with the installer-managed
SPX MCP workspace. `SPX MCP Setup` configures the local `spx-mcp` server for
MCP-capable clients, so an agent can inspect the running server, register
catalog models, create instances, update attributes, and validate behavior
before you decide whether the change needs to become durable repo work.

## Next steps

* Runtime-first MCP setup: [Connect an LLM with SPX MCP](../getting-started/connect-llm-with-spx-mcp.md)
* Docs automation rules: [Docs automation guidelines](docs-automation-guidelines.md)
* Repo-as-spec: [Repo-as-spec](repo-as-spec.md)
* Model Brief template: [Model Brief template](model-brief-template.md)
* Workflow (Generate → Validate → Iterate): [Workflow: Generate → Validate → Iterate](workflow-generate-validate-iterate.md)
* Prompt recipes: [Prompt recipes](prompt-recipes.md)
* Definition of Done: [Definition of Done (DoD)](definition-of-done.md)

Related docs:

* MiL tests: [`getting-started/use-in-unit-tests-mil.md`](../getting-started/use-in-unit-tests-mil.md)
* Snapshots: [`getting-started/snapshots-guide.md`](../getting-started/snapshots-guide.md)
* Custom extensions: [`getting-started/extend-with-custom-component.md`](../getting-started/extend-with-custom-component.md)
