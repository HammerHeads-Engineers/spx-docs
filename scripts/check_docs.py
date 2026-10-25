#!/usr/bin/env python3
"""Check Markdown navigation, local targets, fragments and JSON/YAML model equivalence."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys
import unicodedata
import yaml

ROOT = Path(__file__).resolve().parents[1]


def prose(text):
    return re.sub(r'^```.*?^```[^\n]*', '', text, flags=re.M | re.S)


def anchors(text):
    found = set(re.findall(r'<a\s+(?:id|name)=[\"\']([^\"\']+)', text))
    counts = {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', prose(text), re.M):
        title = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', title)
        slug = ''.join(c for c in unicodedata.normalize('NFKC', title.lower()) if c.isalnum() or c in ' _-')
        slug = re.sub(r'\s', '-', slug)
        n = counts.get(slug, 0)
        found.add(slug + (f'-{n}' if n else ''))
        counts[slug] = n + 1
    return found


def frontmatter(text):
    if not text.startswith('---\n'):
        return {}
    match = re.match(r'^---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        raise ValueError('Unclosed YAML frontmatter')
    value = yaml.safe_load(match.group(1))
    if value is not None and not isinstance(value, dict):
        raise ValueError('YAML frontmatter must be a mapping')
    return value or {}


def check():
    errors = []
    pages = sorted(ROOT.rglob('*.md'))
    pages = [p for p in pages if not any(x.startswith('.') for x in p.relative_to(ROOT).parts)]
    for path in pages:
        text = path.read_text()
        try:
            frontmatter(text)
        except (ValueError, yaml.YAMLError) as error:
            errors.append(f'{path.relative_to(ROOT)}: invalid frontmatter: {error}')
        if re.search(r'^(<<<<<<< |=======\s*$|>>>>>>> )', text, re.M):
            errors.append(f'{path.relative_to(ROOT)}: unresolved conflict')
        for target in (re.findall(r'!?\[[^\]\n]*\]\(([^\n]*?)\)', prose(text)) + re.findall(r'(?:src|href)=[\"\']([^\"\']+)[\"\']', prose(text))):
            target = target.strip().split(' "', 1)[0].strip('<>')
            url = urlsplit(target)
            if url.scheme or url.netloc or not target or target.startswith('mailto:'):
                continue
            local = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not local.is_relative_to(ROOT):
                errors.append(f'{path.relative_to(ROOT)}: outside repository: {target}')
            elif not local.exists():
                errors.append(f'{path.relative_to(ROOT)}: missing target: {target}')
            elif url.fragment and local.is_file() and local.suffix == '.md' and unquote(url.fragment) not in anchors(local.read_text()):
                errors.append(f'{path.relative_to(ROOT)}: missing anchor: {target}')
    config = yaml.safe_load((ROOT / '.gitbook.yaml').read_text())
    for old_url, target in config.get('redirects', {}).items():
        destination = ROOT / target
        if not destination.is_file() or not destination.resolve().is_relative_to(ROOT):
            errors.append(f'Invalid GitBook redirect target: {old_url} -> {target}')
    sample = (ROOT / 'simulation-and-modeling/model-definition-reference.md').read_text()
    yml = re.search(r'```yaml\n(.*?)\n```', sample, re.S).group(1)
    jsn = re.search(r'```json\n(.*?)\n```', sample, re.S).group(1)
    if yaml.safe_load(yml) != json.loads(jsn):
        errors.append('PT100 YAML and JSON model definitions differ')
    manifest = json.loads((ROOT / 'sources.json').read_text())
    spec = json.loads((ROOT / 'api-v3-reference/openapi.json').read_text())
    if spec.get('x-spx-source-commit') != manifest['sources']['spx-server']['commit']:
        errors.append('OpenAPI provenance does not match the runtime baseline')
    if spec['info'] != {'title': 'SPX Server API', 'version': '3.0.0'}:
        errors.append('OpenAPI application metadata differs from the released server')
    if '/health' not in spec['paths'] or '/api/v3/system' not in spec['paths']:
        errors.append('OpenAPI omits root health or API v3 routes')
    for route, methods in spec['paths'].items():
        for method, operation in methods.items():
            if method not in {'get', 'post', 'put', 'delete', 'patch', 'options', 'head'}:
                continue
            secured = bool(operation.get('security', spec.get('security')))
            if secured != route.startswith('/api/v3/'):
                errors.append(f'OpenAPI authentication mismatch: {method} {route}')
    if errors:
        print('\n'.join(errors)); return 1
    print(f'OK: {len(pages)} Markdown pages, local links/anchors/assets, PT100 YAML/JSON parity')
    return 0


if __name__ == '__main__':
    sys.exit(check())
