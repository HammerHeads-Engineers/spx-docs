# SDK Best Practices

This page collects practical conventions for authoring models with the SDK and keeping them maintainable across a growing library.

## Model definition hygiene

- Keep YAML definitions small and composable; prefer templates and reuse over copy/paste forks.
- Name things consistently: **Models**, **Instances**, **Scenarios**, and attribute keys should be predictable and grep-friendly.
- Separate “true state” from “presentation”: write faults/noise to external values (`$out(...)`, `$ext(...)`) when you do not want them to feed back into logic.

## Determinism and testability

- Always drive time explicitly (MiL tests). Do not hide time progression behind sleeps or background threads.
- Add a MiL test for every new behavior. Treat tests as the contract for model correctness.
- Use Snapshots to create stable starting points for longer scenarios.

## Validation and upgrades

- Run schema/definition validation early: [Validation](validation.md).
- Prefer explicit imports and registries for custom classes: [Registry](registry.md), [Imports](imports/README.md).

## Where to look next

- Actions: [Actions](actions.md)
- Attributes: [Attributes](attributes.md)
- Model container: [Model](model.md)
