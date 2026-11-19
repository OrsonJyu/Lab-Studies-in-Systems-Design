#!/usr/bin/env python3
"""Connect a project to its file library and keep the two in order.

Managed by project-standards; run `project_standard.py update` rather than
editing a project's copy.

The library is one folder outside the repository, in iCloud Drive, Google
Drive or on local disk. Each checkout or worktree links it as library/, which
Git ignores, so every worktree sees the same files:

    library/localdata/   research and sensitive data
    library/localfiles/  large or re-obtainable files
    library/outcomes/    deliverables, kept in step with the repository's outcomes/
    library/tmp/         files taken out of the repository to edit elsewhere
    library/<other>      waiting to be sorted

commands:
  link [--set PATH]  link library/; PATH is saved in this machine's Git config,
                     and PATH `none` records in .project-standard.json that the
                     project has no library
  check              report the link without changing anything
  status             list files to sort, edited tmp files and outcome changes
  sync               copy edited tmp files and changed outcomes; never deletes
  clean              delete tmp/ and unsorted files whose content is on the remote

Without a saved PATH the library is $PROJECT_FILES_ROOT/<local_name>, where the
root defaults to ~/ProjectFiles and local_name comes from .project-standard.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = '.project-standard.json'
MANIFEST = '.library-sync.json'
LINK = 'library'
FOLDERS = ('localdata', 'localfiles', 'outcomes', 'tmp')
GIT_KEY = 'projectstandard.library'
DEFAULT_ROOT = '~/ProjectFiles'
REPO_BYTES = 50 * 1024 * 1024
MAX_BYTES = 100 * 1024 * 1024
JUNK = {'.DS_Store', '.localized', 'Icon\r'}
# States that need the user's decision before anything moves.
ASK = {'ambiguous', 'conflict', 'deleted in library', 'deleted in repository'}


def git(*args: str) -> str | None:
    try:
        result = subprocess.run(['git', '-c', 'core.quotePath=false', *args], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', errors='replace')
    except OSError:
        return None
    return result.stdout if result.returncode == 0 else None


def read_config() -> dict:
    try:
        config = json.loads((ROOT / CONFIG).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}
    return config if isinstance(config, dict) else {}


def write_config(config: dict) -> None:
    text = json.dumps(config, ensure_ascii=False, indent=2) + '\n'
    (ROOT / CONFIG).write_text(text, encoding='utf-8')


def disabled() -> bool:
    return read_config().get('library') is False


def report_disabled() -> int:
    print(f'No library: this project sets "library": false in {CONFIG}. '
          f'Run link --set PATH to give it one.')
    return 0


def main_checkout_name() -> str:
    # A worktree's own folder name differs per task; the shared .git does not.
    common = (git('rev-parse', '--path-format=absolute', '--git-common-dir') or '').strip()
    return Path(common).parent.name if common else ROOT.name


def library_path() -> Path:
    saved = (git('config', '--get', GIT_KEY) or '').strip()
    if saved:
        return Path(saved).expanduser()
    name = str(read_config().get('local_name') or '')
    base = Path(os.environ.get('PROJECT_FILES_ROOT') or DEFAULT_ROOT).expanduser()
    return base / (name or main_checkout_name())


def tilde(path: Path) -> str:
    try:
        return '~/' + path.relative_to(Path.home()).as_posix()
    except ValueError:
        return str(path)


def blob(path: Path) -> str:
    """Git's blob id, so library files compare directly with repository history."""
    digest = hashlib.sha1(b'blob %d\0' % path.stat().st_size)
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def junk(name: str) -> bool:
    return name in JUNK or name.startswith('._')


def files_under(folder: Path) -> dict[str, Path]:
    found: dict[str, Path] = {}
    if not folder.is_dir():
        return found
    for base, dirs, names in os.walk(folder):
        dirs[:] = sorted(name for name in dirs if not name.startswith('.'))
        for name in sorted(names):
            if not junk(name):
                path = Path(base) / name
                found[path.relative_to(folder).as_posix()] = path
    return found


def unsorted(home: Path) -> list[Path]:
    if not home.is_dir():
        return []
    return sorted(path for path in home.iterdir()
                  if path.name not in FOLDERS and not junk(path.name) and not path.name.startswith('.'))


def ignored() -> bool:
    result = subprocess.run(['git', 'check-ignore', '-q', '--no-index', LINK], cwd=ROOT)
    return result.returncode != 1


def linked(home: Path) -> str:
    """Return ok, missing, elsewhere or real for the library/ link."""
    path = ROOT / LINK
    if path.is_symlink():
        return 'ok' if path.resolve() == home.resolve() else 'elsewhere'
    return 'real' if path.exists() else 'missing'


def report_link(home: Path, state: str) -> int:
    path = ROOT / LINK
    problems = 0
    if state == 'ok':
        print(f'OK: {LINK} -> {tilde(home)}')
    elif state == 'elsewhere':
        print(f'WARN: {LINK} points to {os.readlink(path)}, not {tilde(home)}. '
              f'Run link --set PATH to choose one.')
        problems += 1
    elif state == 'real':
        print(f'WARN: {LINK} is a real folder. Move its contents to {tilde(home)}, '
              f'remove the empty folder, then run link again.')
        problems += 1
    else:
        print(f'MISSING: {LINK}; run python3 scripts/library.py link')
        problems += 1
    if not ignored():
        print(f'WARN: .gitignore does not exclude {LINK}; add the line /{LINK}')
        problems += 1
    return problems


def link(args: argparse.Namespace) -> int:
    config = read_config()
    if args.set == 'none':
        config['library'] = False
        write_config(config)
        git('config', '--unset', GIT_KEY)
        if (ROOT / LINK).is_symlink():
            (ROOT / LINK).unlink()  # Only the symlink; the folder it pointed to is untouched.
        print(f'Recorded "library": false in {CONFIG}; commit it so every machine skips the library.')
        return 0
    if args.set and config.get('library') is False:
        del config['library']
        write_config(config)
    elif disabled():
        return report_disabled()
    if args.set:
        target = Path(args.set).expanduser().absolute()
        if git('config', GIT_KEY, tilde(target)) is None:
            print('Could not save the library path in Git config.')
            return 2
    home = library_path()
    path = ROOT / LINK
    state = linked(home)
    if state == 'elsewhere' and args.set:
        path.unlink()  # Only the symlink; the folder it pointed to is untouched.
        state = 'missing'
    if state in ('ok', 'missing'):
        for folder in FOLDERS:
            (home / folder).mkdir(parents=True, exist_ok=True)
    if state == 'missing':
        path.symlink_to(home, target_is_directory=True)
        print(f'Linked: {LINK} -> {tilde(home)}')
        state = 'ok'
    return 1 if report_link(home, state) else 0


def check(args: argparse.Namespace) -> int:
    if disabled():
        return report_disabled()
    home = library_path()
    problems = report_link(home, linked(home))
    for folder in FOLDERS:
        if not (home / folder).is_dir():
            print(f'MISSING: {tilde(home / folder)}')
            problems += 1
    return 1 if problems else 0


def history(target: str) -> set[str]:
    found: set[str] = set()
    for line in (git('log', '--format=', '--raw', '--no-abbrev', '--', target) or '').splitlines():
        parts = line.split()
        if line.startswith(':') and len(parts) >= 4:
            found.update(parts[2:4])
    return found


def tmp_plan(home: Path) -> list[tuple[str, str, Path, str]]:
    """(state, name in tmp/, file, matching repository path or '')."""
    by_name: dict[str, list[str]] = {}
    for name in (git('ls-files', '-z') or '').split('\0'):
        if name:
            by_name.setdefault(name.rsplit('/', 1)[-1], []).append(name)
    plan = []
    for name, file in files_under(home / 'tmp').items():
        matches = by_name.get(file.name, [])
        if len(matches) != 1:
            plan.append(('ambiguous' if matches else 'new', name, file, ''))
            continue
        target = matches[0]
        digest = blob(file)
        current = ROOT / target
        stamp = (git('log', '-1', '--format=%ct', '--', target) or '0').strip() or '0'
        stat = file.stat()
        taken = getattr(stat, 'st_birthtime', stat.st_mtime)
        if current.is_file() and blob(current) == digest:
            state = 'unchanged'
        elif digest in history(target):
            state = 'old copy'
        elif int(stamp) > taken:
            state = 'conflict'
        else:
            state = 'edited'
        plan.append((state, name, file, target))
    return plan


def load_manifest() -> dict[str, str]:
    path = ROOT / MANIFEST
    if not path.is_file():
        return {}
    try:
        return dict(json.loads(path.read_text(encoding='utf-8')).get('outcomes', {}))
    except (ValueError, AttributeError):
        return {}


def outcome_plan(home: Path, manifest: dict[str, str]) -> list[tuple[str, str, str | None, str | None]]:
    """(state, path inside outcomes/, repository blob, library blob)."""
    repo = files_under(ROOT / 'outcomes')
    library = files_under(home / 'outcomes')
    plan = []
    for name in sorted(set(repo) | set(library) | set(manifest)):
        mine, theirs = repo.get(name), library.get(name)
        if theirs and not mine and theirs.stat().st_size > REPO_BYTES:
            plan.append(('library only', name, None, None))
            continue
        here = blob(mine) if mine else None
        there = blob(theirs) if theirs else None
        base = manifest.get(name)
        if here == there:
            state = 'same' if here else 'gone'
        elif here == base:
            state = 'to repository' if there else 'deleted in library'
        elif there == base:
            state = 'to library' if here else 'deleted in repository'
        else:
            state = 'conflict'
        plan.append((state, name, here, there))
    return plan


def size(path: Path) -> str:
    if path.is_dir():
        count = len(files_under(path))
        return f'folder, {count} files'
    return f'{path.stat().st_size / (1024 * 1024):.1f} MB'


def show(home: Path, tmp: list, outcomes: list) -> int:
    waiting = unsorted(home)
    print(f'Library: {tilde(home)}')
    print(f'\nTo sort ({len(waiting)}):')
    for path in waiting:
        print(f'  {path.name}  ({size(path)})')
    print(f'\ntmp/ ({len(tmp)}):')
    for state, name, _, target in tmp:
        print(f'  [{state}] {name}' + (f' -> {target}' if target else ''))
    changes = [item for item in outcomes if item[0] not in ('same', 'gone')]
    print(f'\noutcomes/ changes ({len(changes)}):')
    for state, name, _, _ in changes:
        print(f'  [{state}] {name}')
    asks = [item for item in tmp + outcomes if item[0] in ASK]
    if asks:
        print(f'\nNEEDS USER: {len(asks)} item(s) marked {", ".join(sorted({item[0] for item in asks}))}.')
    return len(asks)


def status(args: argparse.Namespace) -> int:
    if disabled():
        return report_disabled()
    home = library_path()
    if linked(home) != 'ok':
        return check(args)
    show(home, tmp_plan(home), outcome_plan(home, load_manifest()))
    return 0


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def sync(args: argparse.Namespace) -> int:
    if disabled():
        return report_disabled()
    home = library_path()
    if linked(home) != 'ok':
        return check(args)
    tmp = tmp_plan(home)
    for state, name, file, target in tmp:
        if state == 'edited':
            copy(file, ROOT / target)
            print(f'tmp -> repository: {target}')
    manifest = load_manifest()
    outcomes = outcome_plan(home, manifest)
    for state, name, here, there in outcomes:
        if state == 'to repository':
            copy(home / 'outcomes' / name, ROOT / 'outcomes' / name)
            print(f'library -> repository: outcomes/{name}')
            manifest[name] = there
        elif state == 'to library':
            copy(ROOT / 'outcomes' / name, home / 'outcomes' / name)
            print(f'repository -> library: outcomes/{name}')
            manifest[name] = here
        elif state == 'same':
            manifest[name] = here
        elif state == 'gone':
            manifest.pop(name, None)
    text = json.dumps({'outcomes': dict(sorted(manifest.items()))}, ensure_ascii=False, indent=2) + '\n'
    path = ROOT / MANIFEST
    if manifest or path.exists():
        if not path.is_file() or path.read_text(encoding='utf-8') != text:
            path.write_text(text, encoding='utf-8')
    asks = [item for item in tmp + outcomes if item[0] in ASK]
    for item in asks:
        print(f'NEEDS USER: [{item[0]}] {item[1]}')
    return 1 if asks else 0


def prune(folder: Path) -> None:
    """Remove folders left empty, apart from Finder's own files."""
    for base, dirs, names in os.walk(folder, topdown=False):
        here = Path(base)
        if all(junk(name) for name in names) and not any((here / name).exists() for name in dirs):
            for name in names:
                (here / name).unlink()
            here.rmdir()


def clean(args: argparse.Namespace) -> int:
    if disabled():
        return report_disabled()
    home = library_path()
    if linked(home) != 'ok':
        return check(args)
    upstream = (git('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}') or '').strip()
    if not upstream:
        print('This branch has no upstream; push it first.')
        return 2
    # Every object the remote branch holds, history included, so each deleted
    # file can be recovered from the remote.
    remote = {line.split()[0] for line in (git('rev-list', '--objects', upstream) or '').splitlines() if line}
    candidates = [(home / 'tmp', list(files_under(home / 'tmp').values()))]
    for path in unsorted(home):
        candidates.append((path, list(files_under(path).values()) if path.is_dir() else [path]))
    removed = 0
    for top, files in candidates:
        for file in files:
            if file.stat().st_size <= MAX_BYTES and blob(file) in remote:
                file.unlink()
                print(f'Deleted (on {upstream}): {tilde(file)}')
                removed += 1
        if top.is_dir() and top != home / 'tmp':
            prune(top)
        elif top == home / 'tmp':
            for child in top.iterdir():
                if child.is_dir():
                    prune(child)
    print(f'{removed} file(s) deleted.')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest='command', required=True)
    start = commands.add_parser('link', help='Link library/ to the project library.')
    start.add_argument('--set', metavar='PATH', help='Library folder to use from now on on this machine.')
    start.set_defaults(run=link)
    for name, run in (('check', check), ('status', status), ('sync', sync), ('clean', clean)):
        commands.add_parser(name).set_defaults(run=run)
    args = parser.parse_args()
    return args.run(args)


if __name__ == '__main__':
    raise SystemExit(main())
