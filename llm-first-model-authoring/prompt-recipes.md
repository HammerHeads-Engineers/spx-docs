# Prompt recipes

These prompts are designed for Codex/LLM-assisted work in `spx-examples`-style repos. They assume the LLM can read the repo and must follow `docs/LLM_SPEC.md` + `docs/MODEL_LANGUAGE.md`.

## 1) Create a new model (copy the closest template)

```text
You are working in the spx-examples repository.

Goal: add a new model for <DEVICE> exposed over <PROTOCOL>.

Hard requirements:
- Follow docs/LLM_SPEC.md and docs/MODEL_LANGUAGE.md.
- Place the model under: library/domains/<domain>/<vendor|generic>/<new_model>.yaml
- File name and `name:` must be lower_snake_case and aligned.
- Update library/catalog/models.yaml with a new entry for this model.
- Add/extend tests under tests/ so pytest covers the new model behavior.
- Run: python tools/validate_models.py and pytest (or explain why not).

Start from this closest template:
- <TEMPLATE_PATH>

Implement:
- New model path: <NEW_MODEL_PATH>
- Attributes (with units in names):
  - <attr_1>: <type>, default <value>, notes <...>
  - <attr_2>: ...
- Communication mapping:
  - protocol block: <protocol-specific mapping rules>
- Scenarios:
  - <scenario_name>: description, duration, overrides/actions

Deliverables:
- Patch with the new YAML model, catalog entry, and tests.
- Short PR summary + how to validate locally.
```

## 2) Add protocol mapping to an existing model

```text
You are working in the spx-examples repository.

Goal: extend an existing model with a new <PROTOCOL> mapping without changing unrelated runtime behavior.

Model:
- YAML: <MODEL_PATH>

What to add:
- New protocol mapping for:
  - <attribute_1> ↔ <protocol register/topic/endpoint>
  - <attribute_2> ↔ ...

Constraints:
- Follow docs/MODEL_LANGUAGE.md for the communication block shape.
- Keep naming/unit conventions for any new attributes.
- Update catalogs only if required (e.g., new protocol/service references).
- Add/extend a MiL test under tests/ that proves the mapping works end-to-end.
- Run: python tools/validate_models.py and pytest.

Before coding:
- Identify the closest existing model in library/domains that already uses <PROTOCOL> and follow its pattern.
```

## 3) Add faults + MiL tests (scenarios are the contract)

```text
You are working in the spx-examples repository.

Goal: add fault coverage to <MODEL_PATH> by introducing scenarios + tests that act as the quality gate.

Add:
- 2–3 scenarios under `scenarios:` that represent realistic faults:
  - <fault_1>: description, duration/schedule, overrides/actions
  - <fault_2>: ...
- A MiL test that:
  - loads the model and creates an instance,
  - starts/stops the scenarios,
  - drives deterministic time,
  - asserts the expected SUT-visible behavior.

Constraints:
- Do not introduce wall-clock coupling for simulation behavior.
- Prefer overrides/actions patterns already used in similar models.
- Update docs/LLM_SPEC.md or docs/MODEL_LANGUAGE.md only if you introduce new constructs (avoid if possible).

Validation:
- python tools/validate_models.py
- pytest -k <new_test_name>
```
