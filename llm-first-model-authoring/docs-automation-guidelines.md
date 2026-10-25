# Docs automation guidelines

## Sources and ownership

`spx-docs/main` is the canonical product reference and publishing branch.
`version-1.0.0` is retained as historical rollback input. Public Examples owns
models, catalogs, profiles, runtime MCP modules, `AGENTS.md`, the modeling
playbook and task templates. Private installer sources are never CI inputs to
these public repositories.

`sources.json` records the coherent released runtime baseline. Its separate
`catalog` entry records the public Examples revision used for the generated
catalog. A catalog refresh must not silently change the released bundle baseline.
Examples uses `docs-source.json` to pin its generated offline model/MCP references.

## Two independent update flows

| Destination | Source paths | Reused branch | PR base |
| --- | --- | --- | --- |
| Docs device catalog | Public Examples catalog metadata on main | `codex/sync-examples-catalog` | Docs `main` |
| Examples offline context | Docs model definition and MCP reference on main | `codex/sync-docs-context` | Examples `develop` |

Each runs daily or by `workflow_dispatch`, resolves a full source commit, and
opens or updates one review PR. Neither merges automatically. Promote reviewed
Examples changes from develop to main through the normal repository workflow.
Publishing follows approved Docs PR merges to main via GitBook Git Sync.
Use GitBook change requests for editorial changes; do not bypass source review.

## Reproducibility and permissions

Checks fetch the exact manifest revision and fail if it is missing. They never
substitute HEAD or a floating branch. Updaters compare meaningful generated
content before updating provenance, so unrelated source commits do not create
metadata-only PRs. Offline sync reads only the two canonical source pages;
catalog sync does not read offline snapshots. This prevents feedback loops.

Normal validation has `contents: read`. Only the updater has own-repository
`contents: write`, `pull-requests: write`, and `actions: write` for explicit
validation dispatch. It uses the job's GITHUB_TOKEN; no PAT, private repository
token or GitBook credential belongs in public CI. Explicit workflow dispatch
runs validation on bot branches without relying on bot-generated PR events.
A reviewer still decides whether to merge.

## Validation and evidence

Run `python scripts/check_docs.py`, then generate/check the catalog with the
full commit from `sources.json` and a public Examples checkout. For semantic
updates, review the source version and affected implementation/tests, record
page → source path → exact commit → evidence in `docs/source-audit.md`, and
separate source inspection, simulated tests, live protocol tests and physical
hardware qualification. Do not claim any verification that was not executed.

Keep URLs, SUMMARY navigation, local assets and the existing OpenAPI spec name
`hammerheadsengineers-api` stable. New API exports come from the pinned runtime
routes, not a stale committed schema. Model/MCP export pages must remain portable
Markdown so offline agents have complete local context.

## Rollback

Revert the relevant main merge to restore source content and let Git Sync
publish it. The version branch and the pre-migration Git bundle retain the old
state. For a Git Sync problem, restore the previous branch/direction in the
existing space; do not create a replacement public site or change its domain.
