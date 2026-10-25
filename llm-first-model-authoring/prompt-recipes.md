---
icon: terminal
---

# Prompt recipes

These prompts are split into two modes:

* **Local-agent mode** (has local git/worktree access): recipe `0` for docs automation.
* **Web-LLM mode** (internet + GitHub browsing, no local repo access): recipes `1+`.

In both modes, treat `spx-examples` on GitHub as the canonical spec and convention source.

Before generating any code, instruct the LLM to open and follow these files from the repo:

* LLM contract: `https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md`
* Model DSL: `https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/MODEL_LANGUAGE.md`
* Task template: `https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_TASK_TEMPLATE.md`
* Validation script: `https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/tools/validate_models.py`
* Catalog (new models must be registered): `https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/catalog/models.yaml`

Important: a web LLM must not claim it ran commands. It should output:

* file-by-file changes (or a unified diff),
* exact local validation commands to run (`python tools/validate_models.py`, `pytest` / `poetry run pytest`),
* and any assumptions/questions when documentation is incomplete.

## 0) Update documentation from source repos (single-branch automation)

Use this when you are updating `spx-docs` based on `spx-examples` changes.

```
You are preparing a docs automation patch for:
- Docs repo: spx-docs
- Source repo: spx-examples

Branch policy (mandatory):
1) Work only on: codex/docs-sync-latest-commits-v1-0-0
2) Rebase on: origin/version-1.0.0 before editing
3) Keep PR target: version-1.0.0

Start with:
- git fetch origin
- git checkout codex/docs-sync-latest-commits-v1-0-0
- git rebase origin/version-1.0.0
- git status --porcelain (must be empty before starting)

Source checkout:
- Prefer local source path: ../spx-examples
- If missing, clone:
  - git clone --depth 1 --branch develop https://github.com/HammerHeads-Engineers/spx-examples.git .tmp/spx-examples
- Use the chosen path consistently in all commands below.

Then pin and report source snapshot:
- git -C <SPX_EXAMPLES_PATH> rev-parse origin/develop

Task:
- Update docs pages impacted by source changes.
- Keep change boundary strict: no unrelated edits outside impacted docs + required navigation/generated files.
- If generated pages are affected, regenerate them from script (no manual table edits):
  - python scripts/generate_device_catalog.py --spx-examples <SPX_EXAMPLES_PATH> --source-ref origin/develop --source-branch develop

Validation:
- python scripts/generate_device_catalog.py --spx-examples <SPX_EXAMPLES_PATH> --source-ref origin/develop --source-branch develop --check
- any additional page-specific checks (links/examples/paths)
- git diff --name-only (verify only intended files changed)

Output format:
1) Files changed.
2) Source snapshot commit SHA(s).
3) Evidence matrix:
   - docs page
   - source file/url
   - source commit
   - rationale
4) Open assumptions/questions.
5) Conflict/rebase status (state clearly whether conflicts were resolved in this run).

Constraints:
- Do not mark models as officially supported by manufacturers unless explicitly confirmed.
- Do not include secrets/tokens in docs examples.
- If source information is missing or conflicting, stop and ask concrete blocking questions.
```

## 1) Generate a model + protocol mapping from device/protocol documentation

Use this when you have a device datasheet, protocol manual, or register map and want the LLM to “recreate the protocol surface” with the minimum simulation behavior required for MiL tests.

```
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: develop)

Before coding, read and follow:
- https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md
- https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/MODEL_LANGUAGE.md
- https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/tools/validate_models.py
- https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/catalog/models.yaml

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

## 2) Create a new model (copy the closest template)

```
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: develop)

Goal: add a new model for <DEVICE> exposed over <PROTOCOL>.

Hard requirements:
- Follow these specs (read them first):
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/MODEL_LANGUAGE.md
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

## 3) Add protocol mapping to an existing model

```
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: develop)

Goal: extend an existing model with a new <PROTOCOL> mapping without changing unrelated runtime behavior.

Model:
- YAML: <MODEL_PATH>

What to add:
- New protocol mapping for:
  - <attribute_1> ↔ <protocol register/topic/endpoint>
  - <attribute_2> ↔ ...

Constraints:
- Follow docs/MODEL_LANGUAGE.md for the communication block shape:
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/MODEL_LANGUAGE.md
- Keep naming/unit conventions for any new attributes.
- Update catalogs only if required (e.g., new protocol/service references).
- Add/extend a MiL test under tests/ that proves the mapping works end-to-end.
- Do not claim you ran anything; output the exact commands I should run locally:
  - python tools/validate_models.py
  - pytest (or poetry run pytest)

Before coding:
- Identify the closest existing model in library/domains that already uses <PROTOCOL> and follow its pattern.
```

## 4) Add faults + MiL tests (scenarios are the contract)

```
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: develop)

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

## 5) Generate a MiL integration test for an existing model

Use this when the model YAML already exists and you want a deterministic, protocol-driven test that validates the SUT-facing behavior.

```
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: develop)

Goal: add a deterministic MiL integration test for an existing model.

Model:
- YAML: <MODEL_PATH> (relative path)
- GitHub URL: <MODEL_URL>

Hard requirements:
- Read and follow:
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/MODEL_LANGUAGE.md
- Do not change the model YAML unless the test exposes a real defect.
- Prefer existing SUT helpers under https://github.com/HammerHeads-Engineers/spx-examples/tree/develop/tests/devices
- Add the test under `tests/shared/integration/` or the relevant `tests/packs/<pack>/integration/` folder.
- Use deterministic stepping (drive time from the test; avoid wall-clock sleeps for simulation behavior).
- If the protocol requires ports/services, mention the required docker-compose port mapping.
- Do not claim you ran anything; output the exact commands I should run locally:
  - python tools/validate_models.py
  - pytest -k <new_test_name> (or poetry run pytest -k <new_test_name>)

Before coding:
- Find a similar test in the repo that uses the same protocol and copy its structure.
- List which attributes/scenarios you will assert and why they matter to the SUT.

Deliverables:
- Patch with the new test file (and any minimal support code if needed).
- Short PR summary + exact local validation commands.
```

## 6) Generate client-software integration tests against an SPX model (MiL)

Use this when you need to modify or create client code (SUT) and verify it end-to-end against an SPX model via MiL tests.

```
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: develop)

Goal: add or update a client (SUT) and a deterministic MiL integration test that validates the client behavior against an SPX model.

Inputs:
- Model YAML: <MODEL_PATH> (relative path) + GitHub URL
- Client code:
  - Existing SUT wrapper in spx-examples (if any): <SUT_PATH>
  - Or external client repo/path: <CLIENT_REPO_URL> + <PATHS>
  - If external code is not public, ask me to paste the relevant files.

Hard requirements:
- Read and follow:
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/MODEL_LANGUAGE.md
- Reuse or extend existing SUT helpers when possible:
  - https://github.com/HammerHeads-Engineers/spx-examples/tree/develop/tests/devices
- Add the MiL test under `tests/shared/integration/` or `tests/packs/<pack>/integration/`.
- Keep tests deterministic: drive time from the test (no wall-clock sleeps for simulation behavior).
- If protocol ports/services are required, note the needed docker-compose port mappings.
- Do not claim you ran anything; output the exact commands I should run locally:
  - python tools/validate_models.py
  - pytest -k <new_test_name> (or poetry run pytest -k <new_test_name>)

Before coding:
- Identify a similar existing test for the protocol and copy its structure.
- List what the client should send/receive and which attributes/scenarios verify correctness.

Deliverables:
- Patch with the updated/new SUT code (if required) and the MiL test.
- Short PR summary + exact local validation commands.
```

## 7) Generate production-device tests + report (_test\_logs)

Use this when you need automated regression tests for a production client/device driver, plus a test report derived from `attributes/_test_logs`.

```
You are preparing a patch for the spx-examples repository:
https://github.com/HammerHeads-Engineers/spx-examples (branch: develop)

Goal: add deterministic MiL tests for a production client/device driver and generate a report from _test_logs.

Inputs:
- Model YAML: <MODEL_PATH> (relative path) + GitHub URL
- Production client details:
  - Repo URL (or local path): <CLIENT_REPO_URL>
  - Entry points / APIs to exercise:
  - If not public, ask me to paste the relevant files.

Hard requirements:
- Read and follow:
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/MODEL_LANGUAGE.md
- Use or extend existing SUT helpers when possible:
  - https://github.com/HammerHeads-Engineers/spx-examples/tree/develop/tests/devices
- Add the MiL test under `tests/shared/integration/` or `tests/packs/<pack>/integration/`.
- Keep tests deterministic: drive time from the test (no wall-clock sleeps for simulation behavior).
- Log test assertions into `attributes/_test_logs` (use existing patterns, e.g.:
  https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/tests/packs/smart_building_pack/integration/test_pack_instances_running.py)
- Report generation:
  - Read `instance["attributes"]["_test_logs"].internal_value` after the test.
  - Write a JSON or Markdown report under `build/test_reports/<test_name>.<json|md>` (create the folder if missing).
- If protocol ports/services are required, note the needed docker-compose port mappings.
- Do not claim you ran anything; output the exact commands I should run locally:
  - python tools/validate_models.py
  - pytest -k <new_test_name> (or poetry run pytest -k <new_test_name>)

Before coding:
- Find a similar existing test for the same protocol and copy its structure.
- List what the production client must send/receive and which attributes/scenarios validate correctness.

Deliverables:
- Patch with the MiL test, report generation, and any minimal SUT changes.
- Short PR summary + exact local validation commands.
```
