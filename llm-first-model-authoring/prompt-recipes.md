# Prompt recipes

These prompts are designed for “web LLM” usage (internet access + GitHub browsing, no local repo access). They use `spx-examples` on GitHub as the canonical spec and convention source.

Before generating any code, instruct the LLM to open and follow these files from the repo:

- LLM contract: `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/LLM_SPEC.md`
- Model DSL: `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md`
- Validation script: `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/tools/validate_models.py`
- Catalog (new models must be registered): `https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/catalog/models.yaml`

Important: a web LLM must not claim it ran commands. It should output:

- file-by-file changes (or a unified diff),
- exact local validation commands to run (`python tools/validate_models.py`, `pytest` / `poetry run pytest`),
- and any assumptions/questions when documentation is incomplete.

## 1) Create a new model (copy the closest template)

```text
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: main)

Goal: add a new model for <DEVICE> exposed over <PROTOCOL>.

Hard requirements:
- Follow these specs (read them first):
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/LLM_SPEC.md
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md
- Place the model under: library/domains/<domain>/<vendor|generic>/<new_model>.yaml
- File name and `name:` must be lower_snake_case and aligned.
- Update library/catalog/models.yaml with a new entry for this model.
- Add/extend tests under tests/ so pytest covers the new model behavior.
- Do not claim you ran anything; output the exact commands I should run locally:
  - python tools/validate_models.py
  - pytest (or poetry run pytest)

Start from this closest template:
- <TEMPLATE_PATH> (relative path in repo, plus GitHub URL)

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
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: main)

Goal: extend an existing model with a new <PROTOCOL> mapping without changing unrelated runtime behavior.

Model:
- YAML: <MODEL_PATH>

What to add:
- New protocol mapping for:
  - <attribute_1> ↔ <protocol register/topic/endpoint>
  - <attribute_2> ↔ ...

Constraints:
- Follow docs/MODEL_LANGUAGE.md for the communication block shape:
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md
- Keep naming/unit conventions for any new attributes.
- Update catalogs only if required (e.g., new protocol/service references).
- Add/extend a MiL test under tests/ that proves the mapping works end-to-end.
- Do not claim you ran anything; output the exact commands I should run locally:
  - python tools/validate_models.py
  - pytest (or poetry run pytest)

Before coding:
- Identify the closest existing model in library/domains that already uses <PROTOCOL> and follow its pattern.
```

## 3) Add faults + MiL tests (scenarios are the contract)

```text
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: main)

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
- Do not claim you ran anything; output the exact commands I should run locally:
  - python tools/validate_models.py
  - pytest -k <new_test_name> (or poetry run pytest -k <new_test_name>)
```

## 4) Generate a model + protocol mapping from device/protocol documentation

Use this when you have a device datasheet, protocol manual, or register map and want the LLM to “recreate the protocol surface” with the minimum simulation behavior required for MiL tests.

```text
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: main)

Before coding, read and follow:
- https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/LLM_SPEC.md
- https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md
- https://github.com/HammerHeads-Engineers/spx-examples/blob/main/tools/validate_models.py
- https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/catalog/models.yaml

Goal: generate a new SPX model that:
1) implements the minimum deterministic simulation behavior needed for MiL testing, and
2) recreates the device/protocol interface with the most important parameters based ONLY on the attached documentation.

Inputs (device/protocol docs):
- <DOC_URL_1> (public URL to PDF/HTML/MD/TXT) — describe what it contains (register map, commands, payloads, timing, etc.)
- <DOC_URL_2>
- (Optional) relevant pages/sections to focus on: <PAGES_OR_SECTIONS>

If the documentation is NOT publicly accessible (login/Confluence), ask me to paste:
- register tables / command lists,
- payload schemas,
- timing/retry/error rules,
- and any example frames/transactions.

Target protocol:
- <PROTOCOL> (must match an existing spx-examples pattern, e.g. modbus/mqtt/scpi/http/ble/knx/bacnet/...)

Hard requirements:
- Do not invent protocol fields/registers/commands that are not in the documentation.
- If the documentation is ambiguous/incomplete, stop and ask concrete questions; list assumptions explicitly.
- Place the model under: library/domains/<domain>/<vendor|generic>/<new_model>.yaml
- File name and `name:` must be lower_snake_case and aligned.
- Update library/catalog/models.yaml with a new entry for this model.
- Add/extend tests under tests/ so pytest covers the new model behavior end-to-end via the protocol.
- Keep determinism: tests drive time; avoid wall-clock sleeps for simulation behavior.
- Do not claim you ran anything; output the exact commands I should run locally:
  - python tools/validate_models.py
  - pytest (or poetry run pytest)

Work plan:
1) Parse the documentation and produce a mapping table:
   - item name (what the SUT cares about),
   - direction (read/write),
   - protocol details (register address / topic / endpoint / command),
   - data type + units + scaling,
   - doc reference (page/section).
2) Find the closest existing model in library/domains that uses <PROTOCOL> and copy its pattern.
3) Implement the new model YAML:
   - attributes (unit suffixes, defaults),
   - minimal actions/dynamics (first-order response / counters / state machine as appropriate),
   - protocol block matching the mapping table.
4) Add scenarios:
   - at least 1 fault scenario derived from the docs (disconnect, overrange, stale data, timeout, etc.),
   - include scenario description.
5) Add a MiL test that:
   - loads the model from disk,
   - creates an Instance,
   - drives deterministic time,
   - exercises the protocol mapping from a SUT client,
   - asserts expected responses and fault behavior.
6) Update catalogs:
   - library/catalog/models.yaml (required)
   - domain/service catalogs only if necessary.
7) Run validation:
   - python tools/validate_models.py
   - pytest -k <new_test_name>

Deliverables:
- Patch with:
  - new model YAML,
  - catalog updates,
  - tests.
- Short PR summary + exact local validation commands.
```
