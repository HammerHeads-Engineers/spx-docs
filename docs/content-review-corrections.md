# Content review corrections — 25 October 2026

This closes the documentation-and-tests scope of the 20-finding review. It does
not change product behavior or claim that every protocol, OS or hardware device
has been exercised. A complete machine-readable DSL schema remains a separate
feature, with the present validation limitations explicitly documented.

## Findings and evidence

| Finding | Priority | Correction / evidence |
| --- | --- | --- |
| F01 | P1 | Keyword client initialization in the generated and runtime-tested client program. |
| F02 | P1 | Correct SDK imports, three serialization variants and executable HeatLoss example; tested using published wheels. |
| F03 | P1 | Separate SDK/proxy timer contracts; actual clock sequence and paused single-step tested. |
| F04 | P1 | Snapshot definition corrected across overview, glossary, FAQ, Core, UI and walkthrough; 20/42/77/20 restore tested. |
| F05 | P1 | Base SDK and runtime lifecycle separated, uppercase states fixed and transition tests added. |
| F06 | P1 | Central component/version/Python matrix; SDK/client dependencies pinned and CI uses Python 3.12. |
| F07 | P2 | Source-backed Python/Cython architecture; unsupported distributed/multi-tenant promises removed. |
| F08 | P2 | Wrapper meaning and external override reset explained and tested. |
| F09 | P2 | Plain-data registry YAML/JSON, no Python object tags; safe loading tested. |
| F10 | P2 | Historical backlog removed from navigation/agent index, source marked archive and legacy redirect configured. |
| F11 | P2 | Agent entry point distinguishes runtime, durable contributions and Docs; Model Brief no longer specifies docs-bot branch. |
| F12 | P2 | Ownership corrected in entry points; public packages versus private source access labelled. |
| F13 | P2 | Navigable role/backend/SUT/limits matrix; source evidence distinguished from physical qualification. |
| F14 | P2 | Complete generated source examples with commands/results/cleanup; signature fragments and JSONC labelled. |
| F15 | P2 | Public executable tutorial contracts, private pinned runtime CI and published-site checker added. |
| F16 | P2 | Per-instance seeded RNG and interleaved regression test; clock versus stochastic/network repeatability explained. |
| F17 | P2 | Installation-specific diagnostics identify actual Compose file, interpreter and managed private binding. |
| F18 | P2 | UI placeholders replaced with instructions and descriptive image text; real support destination and redaction guidance. |
| F19 | P3 | One primary entry, three task paths, reference chapter shortened; OpenAPI schemas explicitly distinguished. |
| F20 | P3 | Agent source order, mode/DoD and identifier glossary; full DSL JSON Schema absence documented as a separate future task. |

## Validation

- 11 public tests pass on Python 3.12 with published SDK RC21/client RC3 wheels.
- 4 runtime contracts pass on the pinned RC76 server, including YAML/JSON API smoke.
- Private runtime CI: [successful run](https://github.com/HammerHeads-Engineers/spx-server/actions/runs/40221253926).
- Existing server CI passed on Python 3.12 and 3.13 for the workflow-only PR.
- Local Markdown/navigation/assets, generated blocks and catalog checks remain required.
- Live-site verification is performed after GitBook publication using `scripts/check_published.py`.
- Offline references must be refreshed through the existing public Examples sync mechanism.

## Deliberate limits

Protocol integration recipes require the configured backend and SUT. The matrix
does not certify physical BLE, Matter, PROFINET or any manufacturer device.
Current screenshots are retained as illustrations; textual instructions explain
the controls and expected state. A snapshot is a structural/configuration restore,
not a new runtime checkpoint feature. The runtime release baseline is unchanged.

See [maintenance instructions](documentation-maintenance.md) for reproduction.
