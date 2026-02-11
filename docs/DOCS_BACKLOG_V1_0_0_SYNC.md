# Docs backlog (v1.0.0 sync)

This backlog was prepared after reviewing recent commits in:

- `spx-examples`
- `spx-server`
- `spx-ui`
- `spx-sdk`
- `spx-python`

The goal is to keep SPX Docs aligned with runtime/UI behavior on branch `version-1.0.0`.

## Latest sync check (2026-02-11)

- Reviewed latest commits for the `version-1.0.0` docs scope using current local heads.
- `spx-examples` latest changes are CI/CD + release metadata; no device catalog updates required.
- `spx-ui` continues to include Logs page + connection error handling; already documented on this branch.
- `spx-server`, `spx-sdk`, and `spx-python` changes are test/release or logging attr normalization; no new docs updates beyond existing edits.
- Note: local source heads differ from the 2026-02-10 snapshot because several repos are on non-release branches (see snapshot).

## Source snapshot (2026-02-11)

| Repo | SHA |
| --- | --- |
| `spx-examples` | `801ded93e16a847528664de15c0d1cdc271136fa` |
| `spx-server` | `8c374a1ffcf4b9400ae193246e88bb1acc7a16d0` |
| `spx-ui` | `575ecb92f2e1202c792cb1c213242cb8cbfa8a95` |
| `spx-sdk` | `7f3d43887f3b81f27be2b2076d0172090db8b0dd` |
| `spx-python` | `6f4647c3e6947e832e48af862f17ef9f898ebde8` |

## Latest sync check (2026-02-10)

- Reviewed latest commits for the `version-1.0.0` docs scope using current local heads.
- `spx-examples` added multiple new device models; device catalog regenerated to reflect the expanded catalog.
- No additional doc changes identified for `spx-server`, `spx-ui`, `spx-sdk`, or `spx-python` beyond release-only commits.

## Source snapshot (2026-02-10)

| Repo | SHA |
| --- | --- |
| `spx-examples` | `d3422bbc8247da6b742a7906b41a55ef91066650` |
| `spx-server` | `2da4bc3da0a820aacb732a03e84bc138c44da28f` |
| `spx-ui` | `09215c7832074707590bb12aef83019f9bc48f41` |
| `spx-sdk` | `1d7bb611af077cfdd4fabefa6e782a8a7cb3253b` |
| `spx-python` | `24959aa1110bcdfbe0b309ccd32d93855b874857` |

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

Latest review (2026-02-11): CI/CD, tests, and release metadata only; existing docs updates already cover known behavior changes (logs page, connection error handling, FunctionAction expressions, _test_logs usage).

Delta since 2026-02-10:

- `spx-examples`: local head now at CI/CD release merge (no model catalog changes).
- `spx-server`: local head includes only test coverage improvements.
- `spx-ui`: local head still includes logs page + connection error handling (already documented).
- `spx-sdk`: local head still includes FunctionAction expression params (already documented).
- `spx-python`: local head includes `_test_logs` attribute normalization (already documented).

Latest review (2026-02-10): `spx-examples` model catalog expansion required a device catalog refresh; no other docs updates were necessary.

Delta since 2026-02-09:

- `spx-examples`: multiple new Modbus + SCPI device models and related catalog entries (Tektronix, Prevac, Siglent, Eastron, APC, Siemens, Schneider, ABB, etc.).
- `spx-server`: current head is a `v0.2.0` release with Dockerfile/compose updates; outside the `version-1.0.0` docs scope.
- `spx-ui`: release v1.0.0 merge (no docs deltas).
- `spx-sdk`: release v1.0.0 merge (no docs deltas).
- `spx-python`: release v1.0.0 merge (no docs deltas).

Workspace baseline heads used for the review:

- `spx-examples`: `d3422bb` (2026-02-10) feat: add Tektronix MDO3000 SCPI model
- `spx-server`: `2da4bc3` (2025-07-30) Release v0.2.0
- `spx-ui`: `09215c7` (2025-04-06) Release v1.0.0
- `spx-sdk`: `1d7bb61` (2026-01-21) chore(release): v1.0.0 [skip ci]
- `spx-python`: `24959aa` (2026-01-21) chore(release): v1.0.0 [skip ci]

Workspace baseline heads used for the review (2026-02-11):

- `spx-examples`: `801ded9` (2026-02-09) Merge pull request #3 from HammerHeads-Engineers/feat/ci-cd
- `spx-server`: `8c374a1` (2026-02-10) test: improve coverage for opcua/lwm2m/coap
- `spx-ui`: `575ecb9` (2026-02-10) Release v1.0.0-rc.57
- `spx-sdk`: `7f3d438` (2026-02-10) chore(release): v1.0.0-rc.21 [skip ci]
- `spx-python`: `6f4647c` (2026-02-10) fix: Update logging attribute names to use "_test_logs" and normalize attribute definitions

Local head snapshot at check time (informational):

- `spx-examples`: `801ded9`
- `spx-server`: `8c374a1`
- `spx-ui`: `575ecb9`
- `spx-sdk`: `7f3d438`
- `spx-python`: `6f4647c`

### spx-examples (2026-02-11 review)

- `801ded9` (2026-02-09): Merge pull request #3 from HammerHeads-Engineers/feat/ci-cd
- `c70fb46` (2026-02-09): chore(release): v1.0.0-alpha.8 [skip ci]
- `5e26ab3` (2026-02-09): feat: Ensure SPX_PACKAGES_TOKEN is set before publishing to GitHub Packages
- `7d93e2a` (2026-02-09): chore(release): v1.0.0-alpha.7 [skip ci]
- `bf43808` (2026-02-09): feat: Refactor GitHub Packages upload steps to use environment variable for SPX_PACKAGES_TOKEN

### spx-server (2026-02-11 review)

- `8c374a1` (2026-02-10): test: improve coverage for opcua/lwm2m/coap
- `d6404af` (2026-02-10): test: expand comms unit coverage
- `0445db7` (2026-02-08): test(coverage): checkpoint top-5 branch-gap targets
- `2f7afe7` (2026-02-08): test: add unit coverage for transports and opcua
- `41ed479` (2026-02-06): Release v1.0.0-rc.56

### spx-ui (2026-02-11 review)

- `575ecb9` (2026-02-10): Release v1.0.0-rc.57
- `a2b818f` (2026-02-10): feat: enhance connection error handling and validation in NewConnection component
- `9c96af1` (2026-02-10): Release v1.0.0-rc.56
- `81052d8` (2026-02-10): feat: implement system logging functionality with filters and source selection
- `dfdef82` (2026-02-10): Release v1.0.0-rc.55

### spx-sdk (2026-02-11 review)

- `7f3d438` (2026-02-10): chore(release): v1.0.0-rc.21 [skip ci]
- `d024f0a` (2026-02-10): feat: Enhance FunctionAction to support parameter expressions and add corresponding test case
- `49c8385` (2026-02-10): chore(release): v1.0.0-rc.20 [skip ci]
- `553be7e` (2026-02-10): feat: Update Hooks.run method to be a no-op and add corresponding test case
- `fb94ef6` (2026-02-10): chore(release): v1.0.0-rc.19 [skip ci]

### spx-python (2026-02-11 review)

- `6f4647c` (2026-02-10): fix: Update logging attribute names to use "_test_logs" and normalize attribute definitions
- `24959aa` (2026-02-10): chore(release): v1.0.0 [skip ci]
- `64b26f7` (2026-02-09): Merge pull request #3 from HammerHeads-Engineers/develop
- `08e9bab` (2026-02-09): chore(release): v1.0.0-rc.3 [skip ci]
- `02ac252` (2026-02-09): feat: Add documentation for LLM integration and testing guidelines

### spx-examples

- `d3422bb` (2026-02-10): Tektronix MDO3000 SCPI model
- `587e87c` (2026-02-10): Prevac XR40B-EC Modbus model
- `f18ddc2` (2026-02-10): Prevac TSP04-PS Modbus model
- `2157901` (2026-02-10): Prevac M1600PDC-PS Modbus model
- `5cd1e32` (2026-02-10): PM5560 Modbus energy meter model
- `da186af` (2026-02-08): Siglent SDS1000X-E SCPI oscilloscope model
- `30f8d7a` (2026-02-08): Siglent SDG1032X SCPI function generator model
- `08ce113` (2026-02-08): Siglent SDM3055 SCPI multimeter model
- `cc5b233` (2026-02-08): Eastron SDM630 Modbus energy meter
- `3d60e81` (2026-02-07): Rigol DP800 SCPI power supply model

### spx-server

- `2da4bc3` (2026-02-10): release v0.2.0 (no docs deltas)

### spx-ui

- `09215c7` (2026-02-10): release v1.0.0 (no docs deltas)

### spx-sdk

- `1d7bb61` (2026-02-10): release v1.0.0 (FunctionAction expression params already documented)

### spx-python

- `02ac252` (2026-01-10): LLM integration and testing guidelines added in spx-python docs
- `24959aa` (2026-02-10): release v1.0.0 (includes LLM/testing docs)

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
  - `simulation-and-modeling/using-spx-python.md`
- Updated installer docs:
  - `getting-started/installer-and-packs.md` (protocol-only defaults, env vars, launchers, Home Assistant theme note)
- Added API v3 delete response example (`destroyed`, `removed_from_parent`) in `api-v3-reference/code-examples.md`
- Added CORS environment variable section + placeholder to `getting-started/installation-guide.md`
- Added protocol-only wizard default note to `getting-started/installation-guide.md`

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
2. Add changelog snippets in `release-notes.md` that point to behavior changes relevant for docs users (CORS, logs page, snapshots, Modbus shared server).

Image placeholders to add:

- Image placeholder: Side-by-side model snippet before/after `k__` convention adoption.
- Image placeholder: Home Assistant theme selection showing `spx_default`.
