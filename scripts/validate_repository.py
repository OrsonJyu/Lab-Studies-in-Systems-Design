#!/usr/bin/env python3
"""Validate documentation, graph references and the imported archive.

Default mode supports a normal checkout with LFS pointers. --hash requires
materialized originals and verifies their original SHA-256 checksums.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hash', action='store_true', help='Verify original bytes; run git lfs pull first.')
    args = parser.parse_args()
    errors: list[str] = []
    version = (ROOT / 'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        errors.append('VERSION must use X.Y.Z.')
    state = json.loads((ROOT / 'PROJECT_STATE.json').read_text())
    if state['repository_version'] != version:
        errors.append('PROJECT_STATE.json version differs from VERSION.')
    for name in ['README.md', 'README.en.md', 'CHANGELOG.md']:
        if version not in (ROOT / name).read_text():
            errors.append(f'{name} does not mention version {version}.')
    for label, target in state['entrypoints'].items():
        if not (ROOT / target).is_file():
            errors.append(f'Missing state entrypoint {label}: {target}')

    manifest = json.loads((ROOT / 'provenance/source-manifest.json').read_text())
    entries = manifest['entries']
    destinations: dict[str, str] = {}
    checked: set[str] = set()
    for record in entries:
        relative = record['repository_path']
        path = ROOT / relative
        if not path.resolve().is_relative_to(ROOT):
            errors.append(f'Manifest path escapes repository: {relative}')
            continue
        prior = destinations.setdefault(relative, record['sha256'])
        if prior != record['sha256']:
            errors.append(f'Different source bytes assigned to the same path: {relative}')
        if not path.is_file():
            errors.append(f'Missing imported file: {relative}')
            continue
        if args.hash and relative not in checked:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != record['sha256']:
                errors.append(f'Original bytes differ (or LFS object is missing): {relative}')
            if path.stat().st_size != record['bytes']:
                errors.append(f'Original size differs: {relative}')
            checked.add(relative)
    if len(entries) != state['archive']['source_records']:
        errors.append('Source-record count differs from PROJECT_STATE.json.')
    if len(destinations) != state['archive']['distinct_imported_paths']:
        errors.append('Imported-path count differs from PROJECT_STATE.json.')

    graph = json.loads((ROOT / 'knowledge/GRAPH.json').read_text())
    node_ids = {node['id'] for node in graph['nodes']}
    if len(node_ids) != len(graph['nodes']):
        errors.append('Knowledge graph contains duplicate node IDs.')
    edge_ids: set[str] = set()
    for edge in graph['edges']:
        if edge['id'] in edge_ids:
            errors.append(f'Duplicate edge ID: {edge["id"]}')
        edge_ids.add(edge['id'])
        if edge['source'] not in node_ids or edge['target'] not in node_ids:
            errors.append(f'Unknown node in edge: {edge["id"]}')
        for key in ['relation', 'status', 'reason', 'sources']:
            if not edge.get(key):
                errors.append(f'Edge {edge["id"]} is missing {key}.')
    for item in graph['nodes'] + graph['edges']:
        for source in item.get('sources', []):
            if not (ROOT / source).is_file():
                errors.append(f'Missing knowledge source: {source}')

    # Imported originals and historical transcripts keep old URLs verbatim.
    # Validate only newly maintained navigation, including alias/landing pages.
    imported = set(destinations)
    link_pattern = re.compile(r'(?<!!)\[[^\]]+\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)')
    checked_docs = 0
    for path in ROOT.rglob('*.md'):
        relative = path.relative_to(ROOT).as_posix()
        if '.git' in path.parts or relative in imported or relative.startswith('docs/history/'):
            continue
        checked_docs += 1
        content = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for raw in link_pattern.findall(content):
            target = raw.strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or target.startswith('#'):
                continue
            local = unquote(parsed.path)
            if local and not (path.parent / local).resolve().exists():
                errors.append(f'Broken maintained link in {relative}: {target}')

    if errors:
        print('\n'.join('ERROR: ' + error for error in errors), file=sys.stderr)
        return 1
    print(f'PASS: version {version}; {len(entries)} source records; {len(destinations)} imported paths; '
          f'{len(node_ids)} graph nodes / {len(edge_ids)} edges; {checked_docs} maintained Markdown files; '
          f'{len(checked)} original checksums verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
