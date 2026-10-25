#!/usr/bin/env python3
"""Propose a catalog update from public Examples main; do nothing for metadata-only changes."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from check_sources import checkout
from generate_device_catalog import render_catalog


def content(text):
    text = re.sub(r'^Source snapshot:.*\n', '', text, flags=re.M)
    return re.sub(r'[0-9a-f]{40}', '<source>', text)


def main():
    manifest = Path('sources.json')
    sources = json.loads(manifest.read_text())
    source = dict(sources['catalog'])
    source['commit'] = subprocess.check_output(['git', 'ls-remote',
        'https://github.com/' + source['repository'] + '.git', 'refs/heads/main'], text=True).split()[0]
    output = Path('usage-scenarios-and-examples/device-catalog.md')
    with tempfile.TemporaryDirectory() as directory:
        checkout(Path(directory) / 'examples', source)
        rendered = render_catalog(Path(directory) / 'examples', source['commit'], None)
    if content(rendered) == content(output.read_text()):
        print('No catalog content changes; leaving the source pin untouched.')
        return
    output.write_text(rendered)
    sources['catalog'] = source
    manifest.write_text(json.dumps(sources, indent=2) + '\n')
    print('Catalog and exact public input updated; ready for a review PR.')


if __name__ == '__main__':
    main()
