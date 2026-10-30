# Workflow: Generate → Validate → Iterate

Use this workflow for a durable model contribution (`repo_dev`) to public
`spx-examples`. For a live simulation, use the
[runtime prompt](prompt-recipes.md#live-runtime-task).

## Branch synchronization

Model changes target `spx-examples/develop`. All commands below run from the
**Examples checkout root**. Product documentation changes use a separate
`spx-docs/main` checkout and the
[documentation maintenance guide](https://github.com/HammerHeads-Engineers/spx-docs/blob/main/docs/documentation-maintenance.md).

## Prereqs (one-time)

```bash
git clone --branch develop https://github.com/HammerHeads-Engineers/spx-examples.git
cd spx-examples
git switch -c codex/multimeter-overrange
```

Choose an unused `codex/<task>` branch name for your own contribution. Read
`AGENTS.md`, `docs/LLM_SPEC.md` and `docs/MODEL_LANGUAGE.md` in that checkout.
Use Python 3.12 and Poetry to install the development dependencies:

```bash
poetry env use python3.12
poetry install --with dev --no-root
```

On Windows, use your Python 3.12 executable path in `poetry env use`.

Repository validation does not need a running server or product key. Live
integration tests do: start a disposable environment with **SPX Start** or the
[server-only Compose guide](../getting-started/manual-docker-compose.md), then
set the [connection environment variables](../simulation-and-modeling/using-spx-python.md#set-your-connection)
in the terminal used for `poetry run pytest`.

Record the Examples revision for the review:

```bash
git rev-parse HEAD
```

## Generate

1. Pick the closest template under `library/domains/...`.
2. Copy it into the correct domain/vendor folder.
3. Keep `name:` aligned with the file stem and keep YAML structure consistent with `docs/MODEL_LANGUAGE.md`:
   - https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/MODEL_LANGUAGE.md

## Validate

Run repo validation (model files + catalog references):

```bash
poetry run python tools/validate_models.py
```

Expected success output:

```text
Model validation passed.
```

Verify the change boundary before PR:

```bash
git diff --name-only
```

## Iterate (tests + UI)

Run the test suite (or target a subset first):

```bash
poetry run pytest
```

For interactive debugging, inspect the running Instance in the UI:

- UI concepts: [`ui-reference/README.md`](../ui-reference/README.md)
- MiL tests (deterministic stepping): [`getting-started/use-in-unit-tests-mil.md`](../getting-started/use-in-unit-tests-mil.md)

## End-to-end example (real template → edit → test)

Goal: create a SCPI multimeter variant with a new fault scenario and a regression test.

1) Start from the template:

- `library/domains/lab/instrument/generic/multimeter__scpi.yaml`
- https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/domains/lab/instrument/generic/multimeter__scpi.yaml

2) Copy it:

```bash
cp library/domains/lab/instrument/generic/multimeter__scpi.yaml \
  library/domains/lab/instrument/generic/multimeter_overrange__scpi.yaml
```

3) Edit the new model:

- File: `library/domains/lab/instrument/generic/multimeter_overrange__scpi.yaml`
- Update:
  - `name: multimeter_overrange__scpi`
  - Add a scenario under `scenarios:` (follow patterns in the source template)

Add this scenario alongside the existing scenarios:

```yaml
scenarios:
  overrange_spike:
    enabled: false
    description: "Brief overrange voltage spike for driver robustness tests."
    duration: 1.0
    overrides:
      $out(voltage): 400.0
```

Start `overrange_spike` explicitly in the test so it does not inject a fault
during normal instance startup.

4) Register it in the catalog:

- File: `library/catalog/models.yaml`
- https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/library/catalog/models.yaml
- Append this complete entry to the catalog's existing `models` list:

```yaml
- id: Lab.MultimeterOverrange.Scpi
  name: SCPI Multimeter with Overrange Fault
  path: library/domains/lab/instrument/generic/multimeter_overrange__scpi.yaml
  domain: lab
  domain_group: lab
  device_class: instrument
  vendor: generic
  protocols: [scpi]
  services:
    - id: scpi_tcp_stack
  packages: []
  profiles: []
```

Use a unique `id` and keep the taxonomy aligned with the model's directory.
This entry is standalone. If adding it to a pack or profile, also update that
membership and its generated index according to Examples `AGENTS.md`.

5) Add a MiL test:

- Copy an existing pattern:
  - `tests/shared/integration/scpi_multimeter_sut_example.py`
- Create a new test under a `test_*.py` file (so `pytest` collects it), e.g.:
  - `tests/core/integration/test_scpi_multimeter_overrange.py`
- Minimal assertions to include:
  - loads the model from disk,
  - creates an Instance,
  - starts the new Scenario,
  - reads the SCPI response and asserts the expected range/behavior.

6) Run:

```bash
poetry run python tools/validate_models.py
poetry run pytest -k scpi_multimeter
```

7) Inspect in UI (optional):

- Start the installed environment with UI enabled using SPX Start.
- Open the UI and inspect the instance attributes/scenarios.

## Output contract for automation runs

Include these in your final update/PR description:

- source snapshot (repo + commit SHA),
- files changed,
- commands executed for validation,
- assumptions and open questions.

Use the [model completion checklist](definition-of-done.md) before review.
If the change also needs product documentation, make that a separate Docs
contribution using its maintenance guide.

## Next steps on simplephysx.com

Explore the embedded testing workflow for validating generated models:

- [Embedded Software Testing](https://www.simplephysx.com/embedded-software-testing)
