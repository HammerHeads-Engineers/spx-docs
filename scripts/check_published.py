#!/usr/bin/env python3
"""Read-only verification of the published GitBook index and corrected contracts."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

SITE = 'https://docs.simplephysx.com'
EXPECT = {
    '/readme/start-here.md': ['Which repository or workspace?', 'Python'],
    '/quick-start-spx-sdk-in-5-minutes.md': ['from spx_sdk.model import Model', '97.48'],
    '/using-spx-python.md': ["inst['timer'].time = tick / 10", 'PAUSED'],
    '/snapshots-guide.md': ['42', '20', 'not a checkpoint'],
    '/agent-start-here.md': ['Source order', 'runtime_mcp', 'repo_dev'],
    '/model-definition-reference.md': ['Agent source order and runtime semantics'],
    '/mcp-reference.md': ['Agent entry point and documentation provenance'],
}


def fetch(url):
    request = Request(url, headers={'User-Agent': 'SPX-documentation-check', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=30) as response:
        return response.status, response.geturl(), response.read().decode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Optional JSON evidence file outside generated docs')
    args = parser.parse_args()
    _, _, index = fetch(SITE + '/llms.txt')
    urls = list(dict.fromkeys(re.findall(r'\]\((https://docs\.simplephysx\.com/[^)]+)\)', index)))
    if not urls:
        raise SystemExit('Published index is empty')
    errors = []
    results = []
    contents = {}
    def inspect(url):
        try:
            status, destination, content = fetch(url)
            return {'url': url, 'status': status, 'destination': destination}, content
        except Exception as error:
            return {'url': url, 'error': str(error)}, ''
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result, content in pool.map(inspect, urls):
            results.append(result)
            contents[urlsplit(result['url']).path] = content
            if result.get('status') != 200:
                errors.append(result)
    for suffix, required in EXPECT.items():
        candidates = [body for path, body in contents.items() if path.endswith(suffix)]
        if len(candidates) != 1:
            errors.append(f'Missing or ambiguous published page: {suffix}')
        else:
            for text in required:
                if text not in candidates[0]:
                    errors.append(f'Unpublished correction in {suffix}: {text}')
    if 'docs_backlog_v1_0_0_sync' in index.lower():
        errors.append('Historical backlog remains in the current agent index')
    placeholders = [url for url in urls if any(x in contents[urlsplit(url).path]
                                               for x in ('Image placeholder:', '| link...'))]
    if placeholders:
        errors.append({'production_placeholders': placeholders})
    try:
        status, destination, _ = fetch(SITE + '/operations-and-support/docs_backlog_v1_0_0_sync')
        if status != 200 or not destination.rstrip('/').endswith('/release-notes'):
            errors.append('Legacy backlog URL does not redirect to current release notes: ' + destination)
    except Exception as error:
        errors.append('Legacy backlog URL failed: ' + str(error))
    evidence = {'checked_at': datetime.now(timezone.utc).isoformat(), 'site': SITE,
                'indexed_pages': len(urls), 'pages': results, 'errors': errors}
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({k: evidence[k] for k in ('site', 'indexed_pages', 'errors')}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
