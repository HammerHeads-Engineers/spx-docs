# Definition of Done (DoD)

This checklist is intentionally aligned with `spx-examples/docs/LLM_SPEC.md`:

- https://github.com/HammerHeads-Engineers/spx-examples/blob/develop/docs/LLM_SPEC.md

## DoD checklist

- [ ] Model YAML is under `library/domains/<domain>/<vendor|generic>/` and uses `lower_snake_case`.
- [ ] `name:` matches the file stem (for new/updated models).
- [ ] `attributes` is present and valid (types/defaults where needed).
- [ ] Protocol mappings follow existing patterns (no invented keys).
- [ ] Scenarios have clear `description`/`display_name` where user-facing.
- [ ] Catalog entry added/updated:
  - [ ] `library/catalog/models.yaml` (for every new model)
  - [ ] `library/catalog/domains.yaml` / `library/catalog/services.yaml` (only if adding new domain/service)
  - [ ] `library/catalog/industries.yaml` + `profiles/<pack>/*.yaml` (only if adding to packs/profiles)
- [ ] Validation passes: `python tools/validate_models.py` → `Model validation passed.`
- [ ] Tests added/updated under `tests/` and passing: `pytest`
- [ ] Deterministic stepping is preserved (MiL tests drive time; no wall-clock coupling)
- [ ] Optional sanity check: model loads and runs as an Instance; inspect in UI ([`ui-reference/README.md`](../ui-reference/README.md))

## DoD checklist (docs automation addendum)

- [ ] Working branch is `codex/docs-sync-latest-commits-v1-0-0` and rebased on `origin/version-1.0.0`.
- [ ] Source snapshot commit SHA(s) are captured in updated docs/PR notes.
- [ ] Navigation is updated when needed (`SUMMARY.md`, chapter `README.md` pages).
- [ ] Generated pages were regenerated from script (no manual table edits).
- [ ] Generated docs check passes:
  - [ ] `python scripts/generate_device_catalog.py --spx-examples ../spx-examples --source-ref origin/develop --source-branch develop --check`
  - [ ] Equivalent CI check is configured in your platform (GitLab CI or GitHub Actions).
- [ ] Claims about device models do not imply official manufacturer support unless formally verified.
- [ ] No secrets/tokens were added to docs examples.

## Common failure modes (and what to check)

- **`tools/validate_models.py` fails**
  - File name / `name:` not `lower_snake_case`
  - Missing `attributes` mapping
  - `communication` shape wrong (list vs mapping)
  - Catalog entry points to a non-existent `path`

- **Tests don’t run**
  - New test file name not collected by pytest (use `test_*.py`)
  - Missing dependencies in the virtualenv (install via Poetry if using `spx-examples`)
  - SPX Server not running (`docker compose ps`) or not reachable (`http://localhost:8000/`)

- **Scenario does nothing**
  - Scenario not `enabled: true`
  - Overrides target the wrong path/key (copy a working pattern from a nearby model)
  - Instance needs a restart/recreate after changing the model definition

- **Non-deterministic behavior**
  - Simulation logic depends on real time or sleeps
  - Time-aware actions used without a `timer` configuration

- **Protocol tests fail**
  - Required ports not exposed in `docker-compose.yml`
  - Model and service config disagree (hostnames/ports)
  - Product key missing (`SPX_PRODUCT_KEY`)

- **Docs PR has avoidable conflicts**
  - Branch was not rebased on `origin/version-1.0.0` before editing
  - Generated docs were edited manually instead of regenerated
  - Navigation updates were skipped (`SUMMARY.md`)
