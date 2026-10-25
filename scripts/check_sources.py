#!/usr/bin/env python3
"""Fetch the exact public catalog input. Never fall back to a branch."""
import argparse
import json
import re
import subprocess
from pathlib import Path


def checkout(destination, source):
    sha = source['commit']
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('A full commit SHA is required')
    if source['repository'] != 'HammerHeads-Engineers/spx-examples':
        raise ValueError('Only the public examples repository is an allowed catalog input')
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    subprocess.run(['git', 'init', str(destination)], check=True, capture_output=True)
    subprocess.run(['git', '-C', str(destination), 'fetch', '--depth=1',
                    'https://github.com/' + source['repository'] + '.git', sha], check=True)
    subprocess.run(['git', '-C', str(destination), 'checkout', '--detach', sha], check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', required=True)
    args = parser.parse_args()
    checkout(args.checkout, json.loads(Path('sources.json').read_text())['catalog'])
