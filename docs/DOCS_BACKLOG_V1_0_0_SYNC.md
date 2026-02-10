# Docs backlog (v1.0.0 sync)

This backlog was prepared after reviewing recent commits in:

- `spx-examples`
- `spx-server`
- `spx-ui`
- `spx-sdk`
- `spx-python`

The goal is to keep SPX Docs aligned with runtime/UI behavior on branch `version-1.0.0`.

## Latest sync check (2026-02-10)

- No new documentation-impacting changes found for the `version-1.0.0` docs scope.
- Source repo heads are unchanged from the 2026-02-09 snapshot.
- Review performed against the current local heads for each source repo.

## Source snapshot (2026-02-10)

| Repo | SHA |
| --- | --- |
| `spx-examples` | `801ded93e16a847528664de15c0d1cdc271136fa` |
| `spx-server` | `d6404af0e94375fcaed436234a245cdca9034fd5` |
| `spx-ui` | `575ecb92f2e1202c792cb1c213242cb8cbfa8a95` |
| `spx-sdk` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` |
| `spx-python` | `6f4647c3e6947e832e48af862f17ef9f898ebde8` |

## Latest sync check (2026-02-09)

- No new documentation-impacting changes found for the `version-1.0.0` docs scope.
- Review performed against the current local heads for each source repo.
- Only `spx-server` changed since the previous sync, and the changes are test-only.

## Source snapshot (2026-02-09)

| Repo | SHA |
| --- | --- |
| `spx-examples` | `801ded93e16a847528664de15c0d1cdc271136fa` |
| `spx-server` | `d6404af0e94375fcaed436234a245cdca9034fd5` |
| `spx-ui` | `575ecb92f2e1202c792cb1c213242cb8cbfa8a95` |
| `spx-sdk` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` |
| `spx-python` | `6f4647c3e6947e832e48af862f17ef9f898ebde8` |

## Latest sync check (2026-02-08)

- This pass keeps docs aligned with the `version-1.0.0` documentation scope.
- Baseline repos were reviewed from local tracking branches used in this workspace.
- Remote `main` heads were also snapshot-checked to avoid hidden drift.

## Reviewed commit set

Latest review (2026-02-10): no newly triaged documentation-impacting commits for the `version-1.0.0` docs scope.

Delta since 2026-02-09:

- No source repo changes (SHAs unchanged).

Workspace baseline heads used for the review:

- `spx-examples`: `801ded9` (2026-01-21) Merge pull request #3 from HammerHeads-Engineers/feat/ci-cd
- `spx-server`: `41ed479` (2026-02-06) Release v1.0.0-rc.56
- `spx-ui`: `575ecb9` (2026-02-06) Release v1.0.0-rc.57
- `spx-sdk`: `7f3d438` (2025-12-22) chore(release): v1.0.0-rc.21 [skip ci]
- `spx-python`: `6f4647c` (2026-02-02) fix: Update logging attribute names to use "_test_logs" and normalize attribute definitions

Remote `main` snapshot at check time (informational):

- `spx-examples/main`: `8d03be0`
- `spx-server/main`: `2da4bc3`
- `spx-ui/main`: `09215c7`
- `spx-sdk/main`: `1d7bb61`
- `spx-python/main`: `24959aa`

### spx-examples

- `8d03be0` (2026-02-06): release v1.0.3 (no docs changes)
- `3b25b54` (2026-02-05): installer wizard flow split into model/instance options

### spx-server

- `cf21a0c` (2026-02-06): CORS env configuration and defaults
- `e49f405` (2026-02-02): snapshot import teardown + delete response status flags
- `8275549` (2026-02-01): template meta-parameter type promotion
- `5b8e4a6` (2026-02-01): snapshot import preserves/clamps runtime limits

### spx-ui

- `a2b818f` (2026-02-06): improved connection validation/error handling
- `81052d8` (2026-02-06): new Logs page with source + severity filters
- `f4a4c4a` (2026-02-03): AttributeValuePopover refactor + InstanceTab tooltips
- `20c69a4` (2026-02-03): attribute unit display and responsive unit column
- `026afc6` (2026-02-02): historical data limit raised to 100000

### spx-sdk

- `d024f0a` (2025-12-22): FunctionAction params accept expressions (docs already aligned)

### spx-python

- `6f4647c` (2026-02-02): logging helpers default to `_test_logs` attribute name

## Implemented in this docs branch

- Added UI page: `ui-reference/logs.md`
- Added Logs entry in GitBook navigation (`SUMMARY.md`) and links from UI overview pages
- Updated UI docs:
  - `ui-reference/instances.md`
  - `ui-reference/models.md`
  - `ui-reference/settings.md`
  - `ui-reference/snapshots.md`
- Updated runtime/server docs:
  - `spx-core/communications/modbus.md`
  - `spx-core/snapshots.md`
  - `spx-core/system/templates.md`
  - `spx-core/system/instances.md`
  - `spx-development-guide/server-api/README.md`
  - `security-considerations.md`
- Updated spx-python docs:
  - `spx-development-guide/spx-python-client-wrapper/testing-helpers-and-logging.md`
  - `llm-first-model-authoring/prompt-recipes.md`
- Updated installer docs:
  - `getting-started/installer-and-packs.md`
- Added API v3 delete response example (`destroyed`, `removed_from_parent`) in `api-v3-reference/code-examples.md`
- Added CORS environment variable section + placeholder to `getting-started/installation-guide.md`

## Suggested next updates (not fully covered yet)

### P0 - before public 1.0.0 docs freeze

1. Add end-to-end example for multi-model Modbus on one `host:port` with unique unit IDs.
2. Add root endpoint response example including `license_user` field.

Image placeholders to add:

- Image placeholder: API client screenshot showing bearer token setup in Swagger/OpenAPI UI.
- Image placeholder: Example response JSON including `license_user`.

### P1 - short-term polish

1. Add screenshots for new UI Logs page filters and source selector.
2. Add screenshots for Test model meta-parameter modal.
3. Add screenshots for Settings connection diagnostic messages (401/network/CORS).
4. Add import/export screenshots showing `run.instances` include/exclude behavior.

Image placeholders to add:

- Image placeholder: Logs page with source dropdown (`System` vs instance).
- Image placeholder: Test model modal with required meta parameters.
- Image placeholder: Import modal with `Start instances listed in configuration` option.

### P2 - content consistency and examples

1. Add a small “Model naming/style conventions” appendix (covering `k__`, hidden `_cycle_time_s`, helper attribute placement).
2. Add Home Assistant section in integration docs mentioning packaged default theme availability.
3. Add changelog snippets in `release-notes.md` that point to behavior changes relevant for docs users (CORS, logs page, snapshots, Modbus shared server).

Image placeholders to add:

- Image placeholder: Side-by-side model snippet before/after `k__` convention adoption.
- Image placeholder: Home Assistant theme selection showing `spx_default`.
