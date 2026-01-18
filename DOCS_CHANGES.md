# Docs changes (non-UI, non-LLM-first)

## Pages filled / improved

- `overview/start-here.md` — Added a role-based “golden path” (Integrator / Developer / QA/CI).
- `spx-development-guide/spx-sdk/imports/README.md` — Filled the stub “Imports” page with practical guidance and a minimal `python_file` example.
- `spx-development-guide/spx-sdk/imports/pythonfile.md` — Updated to match current SDK behavior (SpxComponent vs plain classes, lifecycle `methods`, repo-relative path guidance).
- `troubleshooting-and-support/common-issues-and-solutions.md` — Expanded to 10 issues in Symptom/Cause/Fix format with concrete debug commands.
- `troubleshooting-and-support/faqs.md` — Expanded to 14 FAQs for integrators/dev/QA (determinism, CI, version pinning, validation).
- `appendices/glossary-of-terms.md` — Expanded to ~20 core terms with consistent terminology.
- `release-notes.md` — Documented release/tag sources, versioning expectations, and a safe upgrade checklist.
- `getting-started/use-in-unit-tests-mil.md` — Standardized server base URL env var to `SPX_BASE_URL`.
- `spx-development-guide/spx-python-client-wrapper/testing-helpers-and-logging.md` — Standardized server base URL env var to `SPX_BASE_URL`.

## Navigation

- `SUMMARY.md` — Added `overview/start-here.md` under the Overview section.

## Pages hidden

- None in this pass.

## Consistency decisions

- Python: `>=3.9` (docs target `3.9–3.12`)
- Docker: Docker Compose v2 (`docker compose`); compose file name `docker-compose.yml`
- Env vars: `SPX_PRODUCT_KEY` (required), `SPX_BASE_URL` (optional, defaults to `http://localhost:8000`)
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
