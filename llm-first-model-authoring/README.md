# LLM-first model authoring

LLM-first authoring in SPX means:

- an LLM accelerates drafting YAML + tests,
- **MiL tests** are the quality gate,
- `spx-examples` is the contract for structure, naming, and validation.

Treat `spx-examples` as a repo-as-spec:

- Spec: `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/LLM_SPEC.md`
- Modeling language: `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md`

What you ship is not “a model”, it’s a **model + tests + catalog entries** that stays stable under deterministic stepping.

## Next steps

- Repo-as-spec: [Repo-as-spec](repo-as-spec.md)
- Model Brief template: [Model Brief template](model-brief-template.md)
- Workflow (Generate → Validate → Iterate): [Workflow: Generate → Validate → Iterate](workflow-generate-validate-iterate.md)
- Prompt recipes: [Prompt recipes](prompt-recipes.md)
- Definition of Done: [Definition of Done (DoD)](definition-of-done.md)

Related docs:

- MiL tests: [`getting-started/use-in-unit-tests-mil.md`](../getting-started/use-in-unit-tests-mil.md)
- Snapshots: [`getting-started/snapshots-guide.md`](../getting-started/snapshots-guide.md)
- Custom extensions: [`getting-started/extend-with-custom-component.md`](../getting-started/extend-with-custom-component.md)
