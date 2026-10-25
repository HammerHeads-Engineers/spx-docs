#!/usr/bin/env python3
"""Keep published tutorial blocks byte-for-byte aligned with executable sources."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r'<!-- tutorial:([a-z_]+\.py):start -->.*?<!-- tutorial:\1:end -->', re.S)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = []
    for page in ROOT.rglob('*.md'):
        if any(p.startswith('.') for p in page.relative_to(ROOT).parts):
            continue
        original = page.read_text()
        def render(match):
            source = ROOT / 'examples/tutorials' / match[1]
            return (f'<!-- tutorial:{match[1]}:start -->\n```python\n' + source.read_text().rstrip()
                    + f'\n```\n<!-- tutorial:{match[1]}:end -->')
        result = PATTERN.sub(render, original)
        if result != original:
            changed.append(str(page.relative_to(ROOT)))
            if not args.check:
                page.write_text(result)
    if args.check and changed:
        raise SystemExit('Stale tutorial blocks: ' + ', '.join(changed))
    print('Tutorial source blocks match.' if args.check else f'Rendered {len(changed)} tutorial pages.')


if __name__ == '__main__':
    main()
