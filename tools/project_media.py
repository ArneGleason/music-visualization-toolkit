"""Publish/restore a project media snapshot alongside Git, using GitHub Releases.

Git holds the manifest and authored work; a verified ZIP holds ignored media.
Restore refuses conflicting local edits before writing anything. Use a new tag
for each handoff, so an older checkout can always restore its matching snapshot.
"""
import argparse
from fnmatch import fnmatchcase
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def target(root, name):
    parts = PurePosixPath(name)
    if (parts.is_absolute() or '..' in parts.parts or '\\' in name
            or ':' in name or not parts.parts):
        raise ValueError(f'Unsafe media path: {name}')
    path = root.joinpath(*parts.parts)
    if root.resolve() not in path.resolve().parents:
        raise ValueError(f'Media path leaves checkout: {name}')
    return path


def pack(manifest_path, spec, tag):
    names = set()
    for name in spec['roots']:
        folder = target(ROOT, name)
        if not folder.is_dir():
            raise ValueError(f'Missing media directory: {name}')
        for path in folder.rglob('*'):
            name = path.relative_to(ROOT).as_posix()
            if (path.is_file() and '__pycache__' not in path.parts
                    and not any(fnmatchcase(name, pattern)
                                for pattern in spec.get('exclude', []))):
                names.add(name)
    archive = ROOT / 'out' / 'transfer' / f'{tag}.zip'
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        raise ValueError(f'Archive already exists; choose a new tag: {archive}')
    entries = []
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for name in sorted(names):
            path = target(ROOT, name)
            entries.append({'path': name, 'bytes': path.stat().st_size,
                            'sha256': digest(path)})
            bundle.write(path, name)
    spec.update(schemaVersion=1, tag=tag, archive=archive.name,
                sha256=digest(archive), bytes=archive.stat().st_size, files=entries)
    spec['url'] = (f'https://github.com/{spec["repository"]}/releases/download/'
                   f'{tag}/{archive.name}')
    manifest_path.write_text(json.dumps(spec, indent=2) + '\n', encoding='utf-8')
    print(f'Packed {len(entries)} files, {spec["bytes"]:,} bytes: {archive}')


def states(root, spec):
    result = {'matching': [], 'missing': [], 'changed': []}
    for entry in spec['files']:
        path = target(root, entry['path'])
        state = ('missing' if not path.exists() else
                 'matching' if path.is_file() and digest(path) == entry['sha256']
                 else 'changed')
        result[state].append(entry['path'])
    return result


def restore(root, spec, archive=None):
    current = states(root, spec)
    if current['changed']:
        raise ValueError('Local files differ; checkpoint or move them before restoring:\n'
                         + '\n'.join(current['changed']))
    if not current['missing']:
        print(f'All {len(spec["files"])} media files already match.')
        return
    if archive is None:
        archive = ROOT / 'out' / 'transfer' / spec['archive']
        archive.parent.mkdir(parents=True, exist_ok=True)
        if not archive.exists() or digest(archive) != spec['sha256']:
            print(f'Downloading {spec["bytes"]:,} bytes from {spec["url"]}', flush=True)
            partial = archive.with_suffix('.download')
            urllib.request.urlretrieve(spec['url'], partial)
            if digest(partial) != spec['sha256']:
                raise ValueError(f'Download checksum failed: {partial}')
            partial.replace(archive)
    if digest(archive) != spec['sha256']:
        raise ValueError('Archive checksum failed')
    # Stage and check every member before installing any file. Never extractall:
    # member paths and hashes must match the Git-tracked allowlist exactly.
    with zipfile.ZipFile(archive) as bundle, tempfile.TemporaryDirectory() as temp:
        stage = Path(temp)
        entries = spec['files']
        names = [entry['path'] for entry in entries]
        members = bundle.infolist()
        if len(set(names)) != len(names) or sorted(m.filename for m in members) != sorted(names):
            raise ValueError('Archive members do not match the manifest')
        for entry in entries:
            staged = target(stage, entry['path'])
            staged.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(entry['path']) as source, staged.open('wb') as dest:
                shutil.copyfileobj(source, dest)
            if staged.stat().st_size != entry['bytes'] or digest(staged) != entry['sha256']:
                raise ValueError(f'File checksum failed: {entry["path"]}')
        for name in current['missing']:
            dest = target(root, name)
            dest.parent.mkdir(parents=True, exist_ok=True)
            # Exclusive creation protects edits made while the download ran.
            with dest.open('xb') as stream, target(stage, name).open('rb') as source:
                shutil.copyfileobj(source, stream)
    print(f'Restored {len(current["missing"])} files; kept {len(current["matching"])} matching files.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['pack', 'restore', 'verify'])
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--tag', help='New immutable release tag, for pack')
    parser.add_argument('--archive', type=Path, help='Use a local ZIP instead of downloading')
    parser.add_argument('--root', type=Path, default=ROOT, help='Restore/verify another checkout')
    args = parser.parse_args()
    spec = json.loads(args.manifest.read_text(encoding='utf-8'))
    if args.command == 'pack':
        if not args.tag or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._' for c in args.tag):
            parser.error('pack needs a filename-safe --tag')
        pack(args.manifest, spec, args.tag)
    elif args.command == 'restore':
        restore(args.root.resolve(), spec, args.archive)
    else:
        result = states(args.root.resolve(), spec)
        print(json.dumps({key: len(value) if key == 'matching' else value
                          for key, value in result.items()}, indent=2))
        if result['missing'] or result['changed']:
            raise SystemExit(1)


if __name__ == '__main__':
    main()
