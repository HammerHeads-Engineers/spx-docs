#!/usr/bin/env python3
"""Validate task navigation and legacy source coverage without contacting GitBook."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ['Start here', 'Guides', 'Models & packs', 'Integrations', 'Agents & MCP',
            'Reference', 'Operations & support']


def entries(summary):
    return [(len(m[1]) // 2, m[2], m[3]) for m in
            re.finditer(r'^( *)\* \[([^]]+)\]\(([^)]+)\)', summary, re.M)]


def navigation_errors(summary):
    parsed = entries(summary)
    errors = []
    if [title for depth, title, _ in parsed if depth == 0] != SECTIONS:
        errors.append('Expected seven task sections in the agreed order')
    sources = [path for _, _, path in parsed]
    if len(set(sources)) != len(sources):
        errors.append('Each source page must have one navigation location')
    if any(depth > 2 for depth, _, _ in parsed):
        errors.append('Navigation exceeds two levels below a section')
    if 'llm-first-model-authoring/docs-automation-guidelines.md' in sources:
        errors.append('Maintainer automation belongs outside the user navigation')
    if summary.count('spec: hammerheadsengineers-api') != 1:
        errors.append('Keep exactly one existing OpenAPI integration')
    return errors


def main():
    text = (ROOT / 'SUMMARY.md').read_text()
    errors = navigation_errors(text)
    sources = {p for _, _, p in entries(text)}
    migration = json.loads((ROOT / 'docs/navigation/legacy-pages.json').read_text())
    for row in migration['pages']:
        target = row['target_source']
        if target and target not in sources:
            errors.append('Legacy page has no published successor: ' + row['old_url'])
    for source in sources:
        if not (ROOT / source).is_file():
            errors.append('Missing published source: ' + source)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'OK: 7 task sections, {len(sources)} unique sources, {len(migration["pages"])} legacy pages covered')


if __name__ == '__main__':
    main()
