# Model Brief template

Copy this template into an issue/PR description before asking an LLM to generate or modify a model.

## 1) Goal

- What device/system are we modeling?
- What is the Software Under Test (SUT)?
- What protocols must the SUT use (Modbus/MQTT/HTTP/SCPI/BLE/etc.)?

## 2) Starting point (spx-examples template)

- Template file: `library/domains/<domain>/<vendor|generic>/<template>.yaml`
- Template URL (GitHub, main): https://github.com/HammerHeads-Engineers/spx-examples/blob/main/library/domains/<domain>/<vendor|generic>/<template>.yaml
- Why this template is the closest match:

## 3) Target files (paths)

- Model YAML:
  - New: `library/domains/<domain>/<vendor|generic>/<new_model>.yaml`
  - Or update: `<existing_model>.yaml`
- Catalog updates:
  - `library/catalog/models.yaml` (required for new models)
  - `library/catalog/domains.yaml` / `library/catalog/services.yaml` (only if adding new domain/service)
  - `library/catalog/industries.yaml` + `profiles/<pack>/*.yaml` (only if adding to packs/profiles)
- Tests:
  - `tests/shared/integration/<test>.py` and/or `tests/packs/<pack>/integration/<test>.py`

## 4) Model definition (YAML contract)

### Attributes

List each attribute and its contract:

- `name`:
  - type:
  - default:
  - units (suffix convention like `_c`, `_pct`, `_ms`, `_kw`, …):
  - notes:

### Actions / dynamics

- Time-aware actions used (`ramp`, `saw`, `interpolate`, `pid`):
  - `timer` requirements (`timer.dt`, etc.):
- Deterministic update rules:

### Communication mapping

For each protocol adapter:

- Protocol: (e.g., `modbus`, `mqtt`, `ascii/scpi`, `http`, `ble`)
- Port(s) / service(s):
- Mapping rules:
  - inbound → attribute (write direction)
  - attribute → outbound (read/publish direction)

### Scenarios (faults + demos)

For each scenario:

- `scenario_name`:
  - enabled: true/false
  - duration / schedule:
  - description (user-facing):
  - overrides / actions:
  - expected SUT behavior:

## 5) Acceptance criteria

- [ ] `python tools/validate_models.py` passes
- [ ] `pytest` passes (or documented skips)
- [ ] Tests cover:
  - [ ] happy path
  - [ ] at least 1 fault scenario
- [ ] Deterministic stepping (no wall-clock coupling)
- [ ] UI smoke check: instance loads and expected attributes/scenarios are visible (see [`ui-reference/README.md`](../ui-reference/README.md))

## 6) Notes for the LLM

- Follow the specs in `spx-examples`:
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/LLM_SPEC.md
  - https://github.com/HammerHeads-Engineers/spx-examples/blob/main/docs/MODEL_LANGUAGE.md
- Do not invent new YAML keys or protocols.
- Prefer copying patterns from an existing model + its tests.
