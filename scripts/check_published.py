#!/usr/bin/env python3
"""Verify task navigation and legacy URLs on a GitBook preview or published site."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from check_navigation import entries, SECTIONS

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://docs.simplephysx.com'
MANIFEST = ROOT / 'docs/navigation/legacy-pages.json'
REQUIRED = {
    'README.md': ['Use the browser UI', 'Work with an agent', 'Write Python'],
    'getting-started/README.md': ['my_temperature_sensor', '31.25', 'k__temperature_c'],
    'getting-started/installation-guide.md': ['Installation complete', 'MCP is optional'],
    'spx-development-guide/quick-start-spx-sdk-in-5-minutes.md': ['python sdk_sensor.py yaml', 'Activate.ps1', '97.48'],
    'simulation-and-modeling/using-spx-python.md': ["inst['timer'].time = tick / 10", 'PAUSED'],
    'getting-started/snapshots-guide.md': ['42', '20', 'not a checkpoint'],
    'llm-first-model-authoring/agent-start-here.md': ['Source order', 'runtime_mcp', 'repo_dev'],
    'llm-first-model-authoring/prompt-recipes.md': ['Live runtime task', 'Durable model contribution', 'Do not hand-edit'],
    'simulation-and-modeling/model-definition-reference.md': ['Deployment and communication parameters'],
}


def fetch(url):
    request = Request(url, headers={'User-Agent': 'SPX-documentation-check', 'Cache-Control': 'no-cache'})
    with urlopen(request, timeout=30) as response:
        return response.status, response.geturl(), response.read().decode()


def normalize(url, site):
    """Compare a preview route and the corresponding canonical route."""
    path = urlsplit(url).path
    prefix = urlsplit(site).path.rstrip('/')
    if prefix and path.startswith(prefix + '/'):
        path = path[len(prefix):]
    path = path.rstrip('/') or '/'
    if path in ('/readme', '/readme.md'):
        return '/' if not path.endswith('.md') else '/readme.md'
    return path


def at_site(url, site):
    path = urlsplit(url).path
    prefix = urlsplit(site).path.rstrip('/')
    if prefix and path.startswith(prefix + '/'):
        path = path[len(prefix):]
    return site.rstrip('/') + path


def index_routes(index, summary, site):
    links = list(dict.fromkeys(re.findall(r'^- \[([^]]+)\]\((https://docs\.simplephysx\.com/[^)]+)\)', index, re.M)))
    labels = {}
    for title, url in links:
        labels.setdefault(title.casefold(), []).append(url)
    routes = {}
    for _, title, source in entries(summary):
        matches = labels.get(title.casefold(), [])
        if len(matches) != 1:
            raise ValueError(f'Missing/ambiguous published title {title!r}: {matches}')
        path = normalize(matches[0], site)
        routes[source] = {'title': title, 'markdown_url': ORIGIN + path,
                          'url': ORIGIN + ('/' if source == 'README.md' else path.removesuffix('.md'))}
    for title in ('SPX Server API', 'Models'):
        matches = labels.get(title.casefold(), [])
        if len(matches) != 1:
            raise ValueError(f'Missing/ambiguous generated API page: {title}')
        path = normalize(matches[0], site)
        routes['openapi:' + title] = {'title': title, 'markdown_url': ORIGIN + path,
                                      'url': ORIGIN + path.removesuffix('.md')}
    return links, routes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', default=ORIGIN, help='Public site or exact GitBook PR preview root')
    parser.add_argument('--navigation-file', type=Path, help='Observed preview sidebar links; preview llms.txt reflects production')
    parser.add_argument('--record-routes', action='store_true', help='Record observed canonical routes in the migration manifest')
    parser.add_argument('--output', help='Optional JSON evidence file')
    args = parser.parse_args()
    site = args.site.rstrip('/')
    if urlsplit(site).netloc != 'docs.simplephysx.com' or urlsplit(site).scheme != 'https':
        parser.error('Use the existing HTTPS documentation site or its revision preview')
    if args.navigation_file:
        if not urlsplit(site).path.startswith('/~/revisions/'):
            parser.error('--navigation-file is only for preview verification')
        observed = json.loads(args.navigation_file.read_text())
        seen = set()
        lines = []
        for item in observed:
            title, url = item['title'], item['url']
            if not title or not url.startswith(site) or (title, url) in seen:
                continue
            seen.add((title, url))
            route = '/readme' if url.rstrip('/') == site else normalize(url, site)
            lines.append(f'- [{title}]({ORIGIN}{route}.md)')
        index = '\n'.join(lines)
    else:
        if urlsplit(site).path:
            parser.error('Preview verification requires --navigation-file from its rendered sidebar')
        _, _, index = fetch(site + '/llms.txt')
    manifest = json.loads(MANIFEST.read_text())
    links, routes = index_routes(index, (ROOT / 'SUMMARY.md').read_text(), site)
    errors = []
    if args.record_routes:
        manifest['current_routes'] = routes
        MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')
    elif manifest.get('current_routes') != routes:
        errors.append('Published routes differ from the reviewed migration map; record/review the preview routes first')
    requests = [(at_site(url, site), 'published', None, None) for _, url in links]
    for row in manifest['pages']:
        source = row['target_source'] or 'openapi:' + row['title']
        target = routes[source]
        requests.append((at_site(row['old_url'], site), 'legacy-html', target['url'], source))
        requests.append((at_site(row['old_markdown_url'], site), 'legacy-markdown', target['markdown_url'], source))
    results = []
    content = {}
    def inspect(item):
        url, kind, target, source = item
        try:
            status, destination, text = fetch(url)
            result = {'url': url, 'kind': kind, 'status': status, 'destination': destination}
            if target:
                result['expected'] = at_site(target, site)
                if normalize(destination, site) != normalize(target, site):
                    result['error'] = 'Wrong redirect destination'
            # A preview check must not quietly read old production content.
            prefix = urlsplit(site).path.rstrip('/')
            if prefix and not urlsplit(destination).path.startswith(prefix + '/'):
                result['error'] = 'Redirect escaped the preview'
            return result, text
        except Exception as error:
            return {'url': url, 'kind': kind, 'error': str(error)}, ''
    with ThreadPoolExecutor(max_workers=6) as pool:
        for result, text in pool.map(inspect, requests):
            results.append(result)
            if result['kind'] == 'published':
                content[normalize(result['url'], site)] = text
            if result.get('status') != 200 or 'error' in result:
                errors.append(result)
    for source, expected in REQUIRED.items():
        body = content.get(normalize(routes[source]['markdown_url'], site), '')
        for phrase in expected:
            if phrase.casefold() not in body.casefold():
                errors.append(f'Missing correction in {source}: {phrase}')
    for suffix in ('docs_backlog_v1_0_0_sync', 'docs-automation-guidelines'):
        if suffix in index.lower():
            errors.append('Maintainer/archive page remains in current navigation: ' + suffix)
    for path, body in content.items():
        if 'Image placeholder:' in body or '| link...' in body:
            errors.append('Unfinished production content: ' + path)
    evidence = {'checked_at': datetime.now(timezone.utc).isoformat(), 'site': site,
                'sections': SECTIONS, 'indexed_pages': len(links),
                'legacy_pages': len(manifest['pages']), 'index_source': 'observed-preview-sidebar' if args.navigation_file else 'published-llms', 'checks': results, 'errors': errors}
    if args.output:
        Path(args.output).write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({'site': site, 'indexed_pages': len(links), 'legacy_pages': len(manifest['pages']),
                      'failed_checks': len(errors), 'errors': errors[:12]}, indent=2))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
