# Repo-as-spec (spx-examples)

Use `spx-examples` as the canonical reference for:

- directory layout and naming,
- YAML structure and expressions,
- catalog metadata (what shows up in installers/profiles),
- MiL test conventions.

Spec files (GitHub, main):

- [`docs/LLM_SPEC.md`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/LLM_SPEC.md)
- [`docs/MODEL_LANGUAGE.md`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md)
- [`docs/LLM_TASK_TEMPLATE.md`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/LLM_TASK_TEMPLATE.md)

Repo root (browse): [spx-examples/tree/main](https://github.com/HammerHeads-Engineers/spx-examples/tree/main)

## Source pinning rule

When preparing automated docs/model updates, do not rely on floating `main` references alone.
Capture and report the exact source commit, for example:

```bash
git -C ../spx-examples rev-parse origin/develop
```

Use that SHA in page metadata or PR notes so review is reproducible.

## Evidence matrix (required for substantial updates)

For larger updates, include a compact table in PR notes:

| Docs section | Source file/URL | Source commit | Why changed |
| --- | --- | --- | --- |
| `<page>` | `<path-or-url>` | `<sha>` | `<rationale>` |

## Key directories (real paths)

- Models: `library/domains/<domain>/<vendor|generic>/*.yaml`
  - Browse: [library/domains](https://github.com/HammerHeads-Engineers/spx-examples/tree/main/library/domains)
  - Example (SCPI): [`multimeter__scpi.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/measurement_instruments/generic/multimeter__scpi.yaml)
  - Example (Modbus): [`thermal_controller__modbus.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/thermal_controllers/generic/thermal_controller__modbus.yaml)
  - Example (MQTT): [`environment_sensor__mqtt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/iot/generic/environment_sensor__mqtt.yaml)
  - Example (BLE): [`temperature_sensor__ble_gatt.yaml`](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/ble/generic/temperature_sensor__ble_gatt.yaml)
- Shared helpers used by models: `extensions/`
  - Browse: [extensions](https://github.com/HammerHeads-Engineers/spx-examples/tree/main/extensions)
- Catalogs:
  - `library/catalog/models.yaml` (required for every new model)
    - [models.yaml](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/catalog/models.yaml)
  - `library/catalog/domains.yaml`
    - [domains.yaml](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/catalog/domains.yaml)
  - `library/catalog/services.yaml`
    - [services.yaml](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/catalog/services.yaml)
  - `library/catalog/industries.yaml`
    - [industries.yaml](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/catalog/industries.yaml)
- Validation tooling: `tools/validate_models.py`
  - [validate_models.py](https://github.com/HammerHeads-Engineers/spx-examples/blob/main/tools/validate_models.py)
- Tests:
  - `tests/shared/integration/` (shared integration coverage)
    - [tests/shared/integration](https://github.com/HammerHeads-Engineers/spx-examples/tree/main/tests/shared/integration)
  - `tests/devices/` (SUT wrappers used by tests)
    - [tests/devices](https://github.com/HammerHeads-Engineers/spx-examples/tree/main/tests/devices)
  - `tests/packs/<pack>/` (pack-level test suites)
    - [tests/packs](https://github.com/HammerHeads-Engineers/spx-examples/tree/main/tests/packs)

## “Copy the closest thing” rule

1. Pick the closest existing model under `library/domains/…`.
2. Copy it and rename the file to `lower_snake_case` (keep the protocol suffix pattern, e.g. `__modbus`, `__mqtt`, `__ble_gatt`, `__scpi`).
3. Align `name:` with the file stem for new/updated models.
4. Keep YAML structure consistent with `docs/MODEL_LANGUAGE.md` (top-level keys, list vs mapping shapes).

## Required updates for new models

When you add a new model file:

1. Add a catalog entry in `library/catalog/models.yaml` (new `id`, `name`, `path`, `domain`, `protocols`, `services`, `packages`, `profiles`).
2. Add/update tests in `tests/` (shared tests or pack tests, depending on where the model belongs).
3. Run validation and tests:
   - `python tools/validate_models.py` (prints `Model validation passed.` on success)
   - `pytest`

## What to keep stable

- **Determinism**: time is driven explicitly from tests (MiL). Avoid wall-clock sleeps for simulation behavior.
- **Ports and services**: if a model relies on a protocol adapter, ensure `docker-compose.yml` exposes the required ports/services for the test suite.
- **Terminology**: use consistent terms across docs/tests: SPX Server, Models, Instances, Scenarios, MiL tests, Snapshots.
