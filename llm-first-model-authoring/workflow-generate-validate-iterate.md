# Workflow: Generate → Validate → Iterate

This workflow assumes you are contributing to `spx-examples` (or mirroring its conventions in your own model repo).

## Branch synchronization first (for docs automation)

If you are updating `spx-docs`, work from the single sync branch and rebase before making changes:

```bash
git fetch origin
git checkout codex/docs-sync-latest-commits-v1-0-0
git rebase origin/version-1.0.0
```

Do this at the start of each run and again before opening/updating a PR.

## Prereqs (one-time)

```bash
git clone https://github.com/HammerHeads-Engineers/spx-examples.git
cd spx-examples
```

Set your product key (pick one):

- Edit `.env` and set `SPX_PRODUCT_KEY=...`
- Or export it in your shell: `export SPX_PRODUCT_KEY=...`

Install Python tooling:

```bash
poetry install --with dev
```

Start SPX Server:

```bash
docker compose up -d
```

## Generate

1. Pick the closest template under `library/domains/...`.
2. Copy it into the correct domain/vendor folder.
3. Keep `name:` aligned with the file stem and keep YAML structure consistent with `docs/MODEL_LANGUAGE.md`:
   - https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md

## Validate

Run repo validation (model files + catalog references):

```bash
poetry run python tools/validate_models.py
```

Expected success output:

```text
Model validation passed.
```

If your change touches generated docs pages in `spx-docs`, also run:

```bash
python scripts/generate_device_catalog.py --spx-examples ../spx-examples --source-ref origin/develop --source-branch develop --check
```

And verify the change boundary before PR:

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

- `library/domains/measurement_instruments/generic/multimeter__scpi.yaml`
- https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/measurement_instruments/generic/multimeter__scpi.yaml

2) Copy it:

```bash
cp library/domains/measurement_instruments/generic/multimeter__scpi.yaml \\
  library/domains/measurement_instruments/generic/multimeter_overrange__scpi.yaml
```

3) Edit the new model:

- File: `library/domains/measurement_instruments/generic/multimeter_overrange__scpi.yaml`
- Update:
  - `name: multimeter_overrange__scpi`
  - Add a scenario under `scenarios:` (follow patterns in the source template)

Example scenario shape:

```yaml
scenarios:
  overrange_spike:
    enabled: true
    description: "Brief overrange voltage spike for driver robustness tests."
    duration: 1.0
    overrides:
      $out(voltage): 400.0
```

4) Register it in the catalog:

- File: `library/catalog/models.yaml`
- https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/catalog/models.yaml
- Add a new entry with:
  - `path: library/domains/measurement_instruments/generic/multimeter_overrange__scpi.yaml`
  - `domain: measurement_instruments`
  - `protocols: [scpi]`
  - `services: [{id: scpi_tcp_stack}]` (match existing SCPI models)

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

- Start the UI container (see `spx-examples/docker-compose.yml` for the `spx-ui` service):
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docker-compose.yml
- Open the UI and inspect the instance attributes/scenarios.

## Output contract for automation runs

Include these in your final update/PR description:

- source snapshot (repo + commit SHA),
- files changed,
- commands executed for validation,
- assumptions and open questions.

## Next steps on simplephysx.com

Explore the embedded testing workflow for validating generated models:

- [Embedded Software Testing](https://www.simplephysx.com/embedded-software-testing)
