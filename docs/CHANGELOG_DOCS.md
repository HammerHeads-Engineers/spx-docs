# Docs audit + fix plan

This file tracks documentation QA work for this PR (repo-wide scan + targeted fixes).

## Fix plan (audit findings)

- [x] `README.md` — Marketing-heavy overview; lacks concrete “what is SPX / where to start”. Proposed: rewrite to dev-first overview + links to Quick Start, Snapshots, MiL tests, SDK.
- [x] `overview/introduction.md` — Title typo (“Whats”); content is generic/marketing. Proposed: fix typo + rewrite as concise SPX mental model (SPX Server / SDK / UI, Models, Instances, Scenarios, MiL tests, Snapshots).
- [x] `overview/purpose-and-key-features.md` — Long marketing prose. Proposed: convert to concise, technical feature list with links to relevant chapters.
- [x] `overview/use-case-and-applications.md` — Generic industry examples; not grounded in repo reality. Proposed: replace with SPX-specific workflows (protocol mapping, MiL tests, snapshots) and link to `spx-examples` paths.
- [x] `overview/system-requirements-and-capability.md` — Inconsistent Python requirement (“3.6+”), generic hardware sizing. Proposed: align with `spx-examples` (`Python >=3.9`, `docker compose` v2), list required ports and minimal runtime prerequisites.

- [x] `getting-started/installation-guide.md` — Wrong domain (`simplephysics.io`, `simplephysx.io` + Wix URL); pins an old image tag. Proposed: switch to `https://simplephysx.com`, remove/soften pinned tag, keep commands aligned with `docker compose`.
- [x] `spx-development-guide/quick-start-spx-sdk-in-5-minutes.md` — Placeholder clone URL (`github.com/your-org/...`). Proposed: use canonical repo URL and keep Python range consistent.
- [x] `spx-development-guide/spx-sdk/actions.md` — FunctionAction docs and examples lag behind the `spx-examples` DSL (missing `imports`/`prepare_call`, under-documenting `params`, inconsistent `$in/$out/$attr/$ext` usage). Proposed: align examples with the canonical DSL and document `imports`, derived params, and deterministic seeding patterns.

- [x] `spx-core/README.md` — Broken internal link (`system.md`). Proposed: fix links to `spx-core/system/README.md` and `spx-core/communications/README.md`.
- [x] `spx-core/communications/ble.md` — Broken link to a sibling repo (`../../spx-ble-adapter/...`) and local-only `cd ../...` instructions. Proposed: link to public repo + show `git clone` flow.
- [x] `simulation-and-modeling/extending-simulations/ble-device-simulation.md` — Same broken `spx-ble-adapter` link + local-only instructions. Proposed: link to public repo + show `git clone` flow.

- [x] `api-v3-reference/README.md` — Empty page. Proposed: explain API v3 base URL, auth/env vars, and link to the embedded OpenAPI page + code examples.
- [x] `api-v3-reference/code-examples.md` — Empty page. Proposed: add minimal curl examples + spx-python equivalents (Models/Instances/Logs).
- [x] `spx-development-guide/server-api/README.md` — Empty page. Proposed: outline API basics, auth, versioning, and where to find the OpenAPI reference.

- [x] `simulation-and-modeling/extending-simulations/README.md` — Too thin (only 1 link). Proposed: add concise index + “when to extend” guidance and point to subpages.
- [x] `simulation-and-modeling/extending-simulations/filters-and-signal-processing.md` — Empty page. Proposed: add a minimal “filter as component” pattern + example.
- [x] `simulation-and-modeling/extending-simulations/hardware-bridges-and-backends.md` — Empty page. Proposed: document backend/bridge patterns (ports, Docker networking, determinism constraints).
- [x] `simulation-and-modeling/extending-simulations/testing-and-hot-reload.md` — Empty page. Proposed: add a practical loop (edit → reload → pytest/MiL) and common gotchas.

- [x] `ui-reference/README.md` — Empty page. Proposed: describe UI scope and cross-link to key concepts (Models/Instances/Scenarios/Snapshots/Logs).
- [x] `ui-reference/general-view.md` — Empty page. Proposed: document the General view (what you can inspect and typical debugging workflow).
- [x] `usage-scenarios-and-examples/README.md` — Wrong title (“Configuration”). Proposed: fix title + describe what belongs in the chapter and link to examples.

- [x] `testing-and-validation.md` — Placeholder. Proposed: add MiL tests + snapshots + CI pointers with concrete commands.
- [x] `performance-optimization.md` — Placeholder. Proposed: add a short checklist (timer dt, polling frequency, snapshot size, logs).
- [x] `security-considerations.md` — Placeholder. Proposed: add a short checklist (product key handling, network exposure, container hardening).
- [x] `integration-with-other-systems.md` — Placeholder. Proposed: add patterns + links to protocol docs (Modbus/MQTT/HTTP/BLE).
- [x] `release-notes.md` — Empty skeleton. Proposed: link to release sources and explain version compatibility at a high level.
- [x] `troubleshooting-and-support/README.md` — Placeholder. Proposed: turn into a runbook index.
- [x] `troubleshooting-and-support/common-issues-and-solutions.md` — Empty page. Proposed: add 8–10 common issues with actionable fixes.
- [x] `troubleshooting-and-support/faqs.md` — Empty page. Proposed: short FAQ focused on deterministic simulation + licenses + CI.
- [x] `troubleshooting-and-support/how-to-get-support.md` — Empty page. Proposed: concrete “what to include” checklist (logs, compose, versions).

- [x] `appendices/README.md` — Empty page. Proposed: explain appendix purpose and link to subpages.
- [x] `appendices/glossary-of-terms.md` — Empty page. Proposed: glossary with consistent terminology (Models, Instances, Scenarios, MiL tests, Snapshots).
- [x] `appendices/licensing-information.md` — Empty page. Proposed: how product key is used + where it’s configured (env/compose) + safe handling.
- [x] `appendices/additional-resources-and-readings.md` — Empty page. Proposed: curated links to repos (`spx-examples`, SDK, clients).

- [x] `appendices.md` / `troubleshooting-and-support.md` / `simulation-and-modeling/extending-simulations.md` — Duplicate/out-of-nav pages. Proposed: delete or convert into a short “moved” pointer to the canonical section to avoid conflicting guidance.

## Follow-ups (this pass)

- [x] `spx-development-guide/spx-sdk/imports/README.md` — Stub page (heading-only). Proposed: add a short “what imports are for” overview + links to `PythonFile` and registry patterns.
- [x] `troubleshooting-and-support/common-issues-and-solutions.md` — Too short and not structured as Symptom/Cause/Fix; missing several common failure modes. Proposed: expand to 8–12 issues with symptom/cause/fix and real debug commands.
- [x] `troubleshooting-and-support/faqs.md` — Too few FAQs (needs 10–15, integrator/dev/QA focused). Proposed: expand with practical Q&A (determinism, ports, adapters, CI, snapshots, version pinning).
- [x] `appendices/glossary-of-terms.md` — Glossary is under-sized (needs ~15–25 terms). Proposed: add missing core terms (Domains, Services, Catalogs, Profiles/Packs, Hooks, Conditions, Determinism, Faults).
- [x] `release-notes.md` — Missing explicit “source of truth” and versioning/compatibility policy for multi-artifact releases. Proposed: document where releases/tags live and how to pin/upgrade safely.
- [x] Repo-wide examples — Inconsistent base URL env var usage (`SPX_ADDRESS` / `SPX_API_URL` vs `SPX_BASE_URL`). Proposed: standardize docs to `SPX_BASE_URL` (matches `spx-python` docs/tests).
