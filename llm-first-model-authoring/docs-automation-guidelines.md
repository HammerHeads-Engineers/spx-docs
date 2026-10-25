---
icon: wand-magic-sparkles
---

# Docs automation guidelines

Use this page as the operational contract for automated documentation updates in `spx-docs`.
The goal is simple: keep docs continuously aligned with `spx-examples` and `version-1.0.0` with low-risk PRs.

## Branch strategy (mandatory)

- Use one long-lived docs branch: `codex/docs-sync-latest-commits-v1-0-0`.
- Keep that branch rebased on `origin/version-1.0.0`.
- Open PRs from that single branch into `version-1.0.0`.
- Rebase cadence:
  - before every automation run,
  - before opening or updating a PR,
  - and at least once per working day when active.

Recommended command sequence:

```bash
git fetch origin
git checkout codex/docs-sync-latest-commits-v1-0-0
git rebase origin/version-1.0.0
```

If rebase conflicts appear, resolve immediately in the same run. Do not continue with stale branch state.

## Run preflight checklist

Before generating/updating docs in automation:

- Confirm you are on `codex/docs-sync-latest-commits-v1-0-0`.
- Confirm rebase base is `origin/version-1.0.0`.
- Confirm working tree is clean before starting a new run.
- Confirm source repo path exists (or clone it in the run).

## Top 10 rules

1. **Single branch + rebase discipline**
   - Never create ad-hoc docs branches for routine sync work.
   - Keep all automation history in the single sync branch.
2. **Pin source inputs**
   - For each automated change, record the exact `spx-examples` commit SHA used as source.
   - Do not rely on unpinned `main` in change summaries.
3. **Evidence table for every substantial docs update**
   - Include: `doc section -> source file/url -> source commit -> change rationale`.
4. **Separate execution mode**
   - Distinguish `web LLM` mode from `local agent` mode in instructions.
   - Never claim local command execution in web-only flows.
5. **Use a dedicated docs-update prompt**
   - Require scope, target pages, source references, and expected output format.
   - Require explicit assumptions and open questions.
6. **Docs-specific Definition of Done**
   - Verify navigation (`SUMMARY.md`) updates when adding/removing pages.
   - Verify link integrity, naming consistency, and disclaimers where required.
7. **Generated pages must be reproducible**
   - Regenerate from script, never by manual editing.
   - Current generator:
     - `python scripts/generate_device_catalog.py --spx-examples ../spx-examples --source-ref origin/develop --source-branch develop`
8. **CI drift guard is required**
   - Generated pages must be validated in CI (`--check` mode) to prevent silent drift.
   - This is required regardless of CI platform (GitLab CI or GitHub Actions).
9. **Safety and wording**
   - No secrets in docs examples.
   - Do not mark vendor models as official unless formally certified.
   - Keep risk disclaimers explicit for reference simulations.
10. **Stop on ambiguity, do not invent**
    - If source docs are incomplete or conflicting, stop and list blocking questions.
    - Do not fabricate mappings, features, or compatibility claims.

## Standard output contract for automation runs

Every automated docs update should produce:

- Files changed.
- Source snapshot(s): repo + commit SHA.
- Validation performed (commands and results).
- Open risks/assumptions.

## Generated docs policy

For generated pages in this repository:

- Source-of-truth data lives outside `spx-docs` (for example `spx-examples` catalogs).
- Regeneration command must be documented in the page or nearby guideline.
- CI must fail when generated output is stale.

Current check command:

```bash
python scripts/generate_device_catalog.py --spx-examples ../spx-examples --source-ref origin/develop --source-branch develop --check
```

## GitLab CI example (recommended)

If your canonical pipeline is GitLab CI, add a drift check job equivalent to GitHub Actions:

```yaml
docs:generated-check:
  stage: test
  image: python:3.11
  script:
    - pip install pyyaml
    - git clone --depth 1 --branch develop https://github.com/HammerHeads-Engineers/spx-examples.git .tmp/spx-examples
    - python scripts/generate_device_catalog.py --spx-examples .tmp/spx-examples --source-ref origin/develop --source-branch develop --check
```
