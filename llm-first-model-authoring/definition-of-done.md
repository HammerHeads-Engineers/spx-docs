# Definition of Done (DoD)

This checklist is intentionally aligned with `spx-examples/docs/LLM_SPEC.md`:

- https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md

## Live runtime tasks

Use the [Agent Start Here](agent-start-here.md) stopping criteria. For a local
model/instance task report model ID, instance key, RUNNING state and required
endpoint details. Do not apply the repository checklist below unless persistence
is requested. Verify protocols only when requested or needed for diagnosis.

## Durable model contribution checklist

- [ ] Model YAML is under `library/domains/<domain_group>/<device_class>/<vendor|generic>/` and uses `lower_snake_case`.
- [ ] The working branch is based on `spx-examples/develop` and the PR targets `develop`.
- [ ] `name:` matches the file stem (for new/updated models).
- [ ] `attributes` is present and valid (types/defaults where needed).
- [ ] Protocol mappings follow existing patterns (no invented keys).
- [ ] Scenarios have clear `description`/`display_name` where user-facing.
- [ ] Catalog entry added/updated:
  - [ ] `library/catalog/models.yaml` (for every new model)
  - [ ] Every new model entry includes `id`, `name`, `path`, `domain`, `domain_group`, `device_class`, `vendor`, `protocols`, `services`, `packages` and `profiles`.
  - [ ] `library/catalog/domains.yaml` / `library/catalog/services.yaml` (only if adding new domain/service)
  - [ ] `library/catalog/industries.yaml` + `profiles/<pack>/*.yaml` (only if adding to packs/profiles)
- [ ] Validation passes: `python tools/validate_models.py` → `Model validation passed.`
- [ ] Tests added/updated under `tests/` and passing: `pytest`
- [ ] Deterministic stepping is preserved (MiL tests drive time; no wall-clock coupling)
- [ ] Optional sanity check: model loads and runs as an Instance; inspect in UI ([`ui-reference/README.md`](../ui-reference/README.md))

- [ ] Source revisions, changed files and actually executed checks are recorded in the PR.
- [ ] Claims about device models do not imply official manufacturer support unless formally verified.
- [ ] No secrets or tokens were added to examples.

For a separate `spx-docs/main` contribution, use the
[documentation maintenance checklist](https://github.com/HammerHeads-Engineers/spx-docs/blob/main/docs/documentation-maintenance.md#review-checklist).
Its commands run in the Docs checkout; the model checklist above runs in Examples.

## Common failure modes (and what to check)

- **`tools/validate_models.py` fails**
  - File name / `name:` not `lower_snake_case`
  - Missing `attributes` mapping
  - `communication` shape wrong (list vs mapping)
  - Catalog entry points to a non-existent `path`
  - Catalog entry omits taxonomy or required list fields

- **Tests don’t run**
  - New test file name not collected by pytest (use `test_*.py`)
  - Missing dependencies in the virtualenv (install via Poetry if using `spx-examples`)
  - SPX Server not running (`docker compose ps`) or not reachable (`http://localhost:8000/`)

- **Scenario does nothing**
  - Scenario has not been started explicitly (or automatic start was intentionally disabled)
  - Overrides target the wrong path/key (copy a working pattern from a nearby model)
  - Instance needs a restart/recreate after changing the model definition

- **Non-deterministic behavior**
  - Simulation logic depends on real time or sleeps
  - Time-aware actions used without a `timer` configuration

- **Protocol tests fail**
  - Required ports not exposed in `docker-compose.yml`
  - Model and service config disagree (hostnames/ports)
  - Product key missing (`SPX_PRODUCT_KEY`)
