#!/usr/bin/env python3
"""Check a repository against the project memory standard.

Managed by project-standards; run `project_standard.py update` rather than
editing a project's copy. Uses only the standard library so it runs anywhere.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
CONFIG = '.project-standard.json'
REQUIRED = [
    'README.md',
    'AGENTS.md',
    'CLAUDE.md',
    'PROJECT_STATUS.md',
    '.gitignore',
    'docs/DECISIONS.md',
    'scripts/check_standard.py',
    'scripts/library.py',
    '.githooks/pre-commit',
    '.github/workflows/standard-check.yml',
]
REQUIRED_DIRS = ['docs/workstreams/active', 'docs/workstreams/completed']
MODULES = {
    'research': ['docs/entities/README.md', 'docs/timeline/README.md', 'docs/PROVENANCE.md'],
    'software': ['CHANGELOG.md', 'VERSION'],
    'hardware': ['experiments/README.md', 'environments/README.md'],
}
LOCAL_FOLDERS = ('library',)
STATUS_FIELDS = ['phase', 'updated', 'next']
WORKSTREAM_FIELDS = ['id', 'type', 'status']
STALE_DAYS = 30
MAX_LINES = 180
WARN_BYTES = 50 * 1024 * 1024
MAX_BYTES = 100 * 1024 * 1024
SCAN_BYTES = 1024 * 1024
SECRETS = {
    'GitHub token': re.compile(r'\bgh[pousr]_[A-Za-z0-9]{36,}|\bgithub_pat_[A-Za-z0-9_]{22,}'),
    'AWS access key': re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
    'API key': re.compile(r'(?<![A-Za-z0-9])sk-(?:ant-)?[A-Za-z0-9_-]{20,}'),
    'Google API key': re.compile(r'\bAIza[0-9A-Za-z_-]{35}\b'),
    'Slack token': re.compile(r'\bxox[abprs]-[A-Za-z0-9-]{10,}'),
    'private key': re.compile(r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----'),
}
KEY_FILES = {'id_rsa', 'id_ed25519', 'id_ecdsa'}
LINK = re.compile(r'!?\[[^\]]*\]\((<[^>]+>|(?:[^\s()]|\([^\s()]*\))+)(?:\s+"[^"]*")?\)')
CODE = re.compile(r'^(```|~~~).*?^\1[^\n]*$|`[^`\n]*`|<!--.*?-->', re.S | re.M)
DECISION = re.compile(r'^(?:\|\s*|#{2,4}\s+)(D\d{3,})\b', re.M)


def git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(['git', '-c', 'core.quotePath=false', *args], cwd=root,
                                capture_output=True, text=True, encoding='utf-8', errors='replace')
    except OSError:
        return None
    return result.stdout if result.returncode == 0 else None


def nfc(text: str) -> str:
    # macOS may store a name decomposed while Markdown holds the composed form.
    return unicodedata.normalize('NFC', text)


def list_files(root: Path, staged: bool) -> tuple[list[str], list[str]]:
    """Return (files to treat as present, files Git is tracking)."""
    tracked = git(root, 'ls-files', '-z', '--cached')
    if tracked is None:
        found = [path.relative_to(root).as_posix() for path in root.rglob('*')
                 if path.is_file() and not {'.git', 'node_modules', '__pycache__'} & set(path.parts)
                 and path.relative_to(root).parts[0] not in LOCAL_FOLDERS]
        return found, found
    cached = [name for name in tracked.split('\0') if name and (root / name).is_file()]
    if staged:
        return cached, cached
    others = git(root, 'ls-files', '-z', '--others', '--exclude-standard') or ''
    return cached + [name for name in others.split('\0') if name], cached


def excluded(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def read(path: Path) -> str:
    return path.read_bytes().decode('utf-8', 'replace')


def front_matter(text: str) -> dict[str, str]:
    lines = text.lstrip('﻿').splitlines()
    if not lines or lines[0].strip() != '---':
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == '---':
            return fields
        key, separator, value = line.partition(':')
        if separator and key and not key[0].isspace():
            fields[key.strip()] = value.strip()
    return {}


def load_config(root: Path, errors: list[str]) -> dict | None:
    path = root / CONFIG
    if not path.is_file():
        errors.append(f'Missing {CONFIG}.')
        return None
    try:
        config = json.loads(read(path))
    except ValueError as exc:
        errors.append(f'{CONFIG} is not valid JSON: {exc}')
        return None
    if not isinstance(config, dict):
        errors.append(f'{CONFIG} must be a JSON object.')
        return None
    if not re.fullmatch(r'\d+\.\d+\.\d+', str(config.get('standard', ''))):
        errors.append(f'{CONFIG}: standard must use X.Y.Z.')
    modules = config.get('modules', [])
    exclude = config.get('exclude', [])
    if not isinstance(config.get('local_name', ''), str):
        errors.append(f'{CONFIG}: local_name must be a string.')
    if config.get('library', True) is not False and 'library' in config:
        errors.append(f'{CONFIG}: library can only be false.')
    if not isinstance(modules, list) or not isinstance(exclude, list):
        errors.append(f'{CONFIG}: modules and exclude must be lists.')
        return None
    for module in modules:
        if module not in MODULES:
            errors.append(f'{CONFIG}: unknown module {module}.')
    return config


def check_required(config: dict, present: set[str], folders: set[str], errors: list[str]) -> None:
    needed = list(REQUIRED)
    for module in config.get('modules', []):
        needed += MODULES.get(module, [])
    for name in needed:
        if name not in present:
            errors.append(f'Missing required file: {name}')
    for name in REQUIRED_DIRS:
        if name not in folders:
            errors.append(f'Missing required folder: {name}/')


def check_links(root: Path, name: str, text: str, present: set[str], folders: set[str],
                errors: list[str]) -> None:
    for raw in LINK.findall(CODE.sub('', text)):
        target = raw.strip('<>')
        try:
            parsed = urlsplit(target)
        except ValueError:
            continue
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        local = unquote(parsed.path)
        base = root if local.startswith('/') else (root / name).parent
        resolved = (base / local.lstrip('/')).resolve()
        try:
            relative = nfc(resolved.relative_to(root.resolve()).as_posix())
        except ValueError:
            errors.append(f'Link leaves the repository in {name}: {target}')
            continue
        if relative != '.' and relative not in present and relative not in folders:
            errors.append(f'Broken link in {name}: {target}')


def check_status(text: str, today: dt.date, errors: list[str], warnings: list[str]) -> None:
    fields = front_matter(text)
    for key in STATUS_FIELDS:
        if not fields.get(key):
            errors.append(f'PROJECT_STATUS.md front matter lacks {key}.')
    updated = fields.get('updated', '')
    if not updated:
        return
    try:
        age = (today - dt.date.fromisoformat(updated)).days
    except ValueError:
        errors.append('PROJECT_STATUS.md updated must use YYYY-MM-DD.')
        return
    if age > STALE_DAYS:
        warnings.append(f'PROJECT_STATUS.md was last updated {age} days ago.')


def workstream_folder(name: str) -> str | None:
    """Return active/completed for a workstream record, or None for other files."""
    parts = name.split('/')
    if parts[:2] != ['docs', 'workstreams'] or len(parts) < 4 or parts[2] not in ('active', 'completed'):
        return None
    is_record = len(parts) == 4 and parts[3] != 'README.md'
    is_split_index = len(parts) == 5 and parts[4] == 'README.md'
    return parts[2] if is_record or is_split_index else None


def check_workstream(root: Path, name: str, folder: str, text: str, today: dt.date,
                     errors: list[str], warnings: list[str]) -> None:
    fields = front_matter(text)
    for key in WORKSTREAM_FIELDS:
        if not fields.get(key):
            errors.append(f'{name} front matter lacks {key}.')
    if fields.get('status') and fields['status'] != folder:
        errors.append(f'{name} has status {fields["status"]} but sits in {folder}/.')
    if folder != 'active':
        return
    stamp = (git(root, 'log', '-1', '--format=%ct', '--', name) or '').strip()
    if stamp:
        age = (today - dt.date.fromtimestamp(int(stamp))).days
        if age > STALE_DAYS:
            warnings.append(f'{name} has no commit for {age} days.')


def check_length(name: str, text: str, warnings: list[str]) -> None:
    current = name in ('PROJECT_STATUS.md', 'README.md', 'AGENTS.md') \
        or name.startswith(('docs/workstreams/active/', 'docs/entities/'))
    lines = text.count('\n') + 1
    if current and lines > MAX_LINES:
        warnings.append(f'{name} has {lines} lines; split it into an index and sub-pages.')


def check_tracked(root: Path, tracked: list[str], errors: list[str], warnings: list[str]) -> None:
    for name in tracked:
        path = root / name
        base = name.rsplit('/', 1)[-1]
        if (base == '.env' or base.startswith('.env.')) and base != '.env.example':
            errors.append(f'Environment file is tracked: {name}')
        if base in KEY_FILES:
            errors.append(f'Private key file is tracked: {name}')
        if name.split('/', 1)[0] in LOCAL_FOLDERS:
            errors.append(f'Local-only file is tracked: {name}')
            continue
        size = path.stat().st_size
        if size > WARN_BYTES and 'filter: lfs' not in (git(root, 'check-attr', 'filter', '--', name) or ''):
            megabytes = size // (1024 * 1024)
            message = f'{name} is {megabytes} MB without Git LFS.'
            (errors if size > MAX_BYTES else warnings).append(message)
        if size > SCAN_BYTES:
            continue
        data = path.read_bytes()
        if b'\0' in data[:8192]:
            continue
        text = data.decode('utf-8', 'replace')
        for label, pattern in SECRETS.items():
            match = pattern.search(text)
            if match:
                line = text.count('\n', 0, match.start()) + 1
                errors.append(f'Possible {label} in {name}:{line}')


def check_local_ignored(root: Path, config: dict, warnings: list[str]) -> None:
    if config.get('library') is False:
        return
    for folder in LOCAL_FOLDERS:
        # Exit code 1 means not ignored; other failures mean Git is unavailable.
        try:
            result = subprocess.run(['git', 'check-ignore', '-q', '--no-index', folder], cwd=root)
        except OSError:
            return
        if result.returncode == 1:
            warnings.append(f'.gitignore does not exclude {folder}; add the line /{folder}')


def check_repository(root: Path, staged: bool = False, today: dt.date | None = None):
    today = today or dt.date.today()
    errors: list[str] = []
    warnings: list[str] = []
    config = load_config(root, errors)
    if config is None:
        return errors, warnings, {}
    files, tracked = list_files(root, staged)
    present = {nfc(name) for name in files}
    folders = {str(parent.as_posix()) for name in present for parent in Path(name).parents}
    check_required(config, present, folders, errors)
    check_tracked(root, tracked, errors, warnings)
    check_local_ignored(root, config, warnings)

    exclude = [str(pattern) for pattern in config.get('exclude', [])]
    identifiers: dict[str, str] = {}
    documents = workstreams = 0
    for name in files:
        if not name.endswith('.md') or excluded(name, exclude):
            continue
        documents += 1
        text = read(root / name)
        check_links(root, name, text, present, folders, errors)
        check_length(name, text, warnings)
        identifier = front_matter(text).get('id')
        if identifier:
            if identifier in identifiers:
                errors.append(f'Duplicate id {identifier}: {identifiers[identifier]} and {name}')
            identifiers.setdefault(identifier, name)
        folder = workstream_folder(name)
        if folder:
            workstreams += 1
            check_workstream(root, name, folder, text, today, errors, warnings)
        if name == 'PROJECT_STATUS.md':
            check_status(text, today, errors, warnings)
        if name == 'docs/DECISIONS.md':
            found = DECISION.findall(CODE.sub('', text))
            for decision in sorted({item for item in found if found.count(item) > 1}):
                errors.append(f'Duplicate decision {decision} in docs/DECISIONS.md')
    return errors, warnings, {'standard': config.get('standard'), 'documents': documents,
                              'workstreams': workstreams}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true', help='Treat only files in the Git index as present.')
    parser.add_argument('--strict', action='store_true', help='Fail on warnings as well as errors.')
    args = parser.parse_args()
    errors, warnings, stats = check_repository(ROOT, args.staged)
    for warning in warnings:
        print('WARN: ' + warning)
    if errors:
        print('\n'.join('ERROR: ' + error for error in errors), file=sys.stderr)
    if errors or (args.strict and warnings):
        return 1
    print(f'PASS: standard {stats["standard"]}; {stats["documents"]} Markdown files; '
          f'{stats["workstreams"]} workstreams; {len(warnings)} warnings.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
