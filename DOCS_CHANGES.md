# Docs changes (non-UI, non-LLM-first)

## Pages filled / improved

- `overview/start-here.md` — Added a role-based “golden path” (Integrator / Developer / QA/CI).
- `README.md` / `overview/introduction.md` / hub pages — Replaced “Next page: `path`” / backtick paths with real clickable links (non-UI, non-LLM-first).
- `getting-started/choose-a-protocol-adapter.md` — Added an integrator routing page (pick an adapter, link to docs, link to `spx-examples` models).
- `spx-development-guide/spx-sdk/imports/README.md` — Filled the stub “Imports” page with practical guidance and a minimal `python_file` example.
- `spx-development-guide/spx-sdk/imports/pythonfile.md` — Updated to match current SDK behavior (SpxComponent vs plain classes, lifecycle `methods`, repo-relative path guidance).
- `spx-development-guide/spx-sdk/actions.md` — Expanded `function`/`call` documentation (`imports`, `params`, multi-line calls, local helper imports aligned with `spx-examples`).
- `spx-development-guide/spx-sdk/communication.md` — Removed legacy `class:` examples; aligned with SPX Server adapter keys (`modbus_slave`, `http_endpoint`) and linked to the authoritative adapter docs.
- `spx-core/communications/ascii.md` — Documented ASCII port auto-assignment and aligned scenario naming with `spx-examples`.
- `spx-core/communications/README.md` — Rebuilt as a routing hub listing all protocol adapters implemented in `spx-server` (with YAML keys and grouping).
- `spx-core/communications/http.md` — Rewritten to match `http_endpoint` + `endpoints` schema and grounded in `spx-examples`.
- `spx-core/communications/mqtt.md` — Rewritten to match bindings-based `mqtt` schema; added `mqtt-ha` coverage (brokers, availability, discovery).
- `spx-core/communications/modbus.md` — Rewritten to cover `modbus_slave` / `modbus_tcp` / `modbus_master` and the correct Modbus area codes (`h_r/i_r/c_o/d_i`).
- `spx-core/communications/bacnet.md` / `coap.md` / `dali.md` / `knx.md` / `lwm2m.md` / `matter.md` / `mbus.md` / `ocpp.md` / `opcua.md` / `profinet.md` / `redfish.md` / `snmp.md` — Added minimal, test-grounded pages for all remaining SPX Server communication adapters.
- `getting-started/add-communication-protocol.md` — Tightened Modbus tutorial consistency (env vars, mapping text vs YAML, float decoding example, port exposure note).
- `troubleshooting-and-support/common-issues-and-solutions.md` — Expanded to 10 issues in Symptom/Cause/Fix format with concrete debug commands.
- `troubleshooting-and-support/faqs.md` — Expanded to 14 FAQs for integrators/dev/QA (determinism, CI, version pinning, validation).
- `appendices/glossary-of-terms.md` — Expanded to ~20 core terms with consistent terminology.
- `release-notes.md` — Documented release/tag sources, versioning expectations, and a safe upgrade checklist.
- `getting-started/installation-guide.md` — Rebuilt with complete Compose + `.env` templates, `/health` verification, and “next steps” links.
- `getting-started/build-your-first-simulation.md` — Switched verification to `/health`, removed pinned versions, and standardized `SPX_BASE_URL` usage.
- `getting-started/use-in-unit-tests-mil.md` — Standardized server base URL env var to `SPX_BASE_URL`.
- `getting-started/ci-cd-setup-github-actions.md` — Added a Python matrix (3.9–3.12), standardized readiness probe to `/health`, and included `SPX_BASE_URL` in workflow env.
- `getting-started/snapshots-guide.md` — Removed hard-coded server version requirement and cleaned up formatting.
- `usage-scenarios-and-examples/common-use-cases.md` — Re-grounded the SCPI multimeter walkthrough in `spx-examples` (real file paths, scenarios, runnable commands).
- `spx-development-guide/spx-python-client-wrapper/testing-helpers-and-logging.md` — Standardized server base URL env var to `SPX_BASE_URL`.

## Navigation

- `SUMMARY.md` — Added `overview/start-here.md` under the Overview section.
- `SUMMARY.md` — Added `getting-started/choose-a-protocol-adapter.md` under Quick Start.
- `SUMMARY.md` — Expanded “Communication Adapters” to include all protocol pages.

## Pages hidden

- None in this pass.

## Consistency decisions

- Python: `>=3.9` (tested in CI on `3.9–3.12`)
- Docker: Docker Compose v2 (`docker compose`); compose file name `docker-compose.yml`
- Env vars: `SPX_PRODUCT_KEY` (required), `SPX_BASE_URL` (optional, defaults to `http://localhost:8000`)
- Health check: `GET http://localhost:8000/health`
- Canonical product site: `https://simplephysx.com`

## Validate locally

1) Check GitBook navigation targets and relative `.md` links:

```bash
python - <<'PY'
import re
from pathlib import Path

root = Path('.')

summary = root / 'SUMMARY.md'
text = summary.read_text(encoding='utf-8')
links = re.findall(r'\\]\\(([^)]+)\\)', text)

missing = []
for href in links:
    if href.startswith('http') or href.startswith('#'):
        continue
    path = href.split('#', 1)[0]
    if not path:
        continue
    if not (root / path).exists():
        missing.append(href)

md_files = [p for p in root.rglob('*.md') if p.is_file()]
rel_missing = []
link_re = re.compile(r'\\]\\(([^)]+\\.md(?:#[^)]+)?)\\)')
for md in md_files:
    t = md.read_text(encoding='utf-8')
    for href in link_re.findall(t):
        if href.startswith('http'):
            continue
        path = href.split('#', 1)[0]
        if not (md.parent / path).exists():
            rel_missing.append((md.as_posix(), href))

print('SUMMARY missing:', len(missing))
for h in missing:
    print('  ', h)
print('Relative .md missing:', len(rel_missing))
for f, h in rel_missing:
    print('  ', f, '->', h)

if missing or rel_missing:
    raise SystemExit(1)
print('OK')
PY
```
