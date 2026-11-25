"""Inventory media; prune only explicitly disposable, versioned preview folders.

Layout: generated/wip/previews/<series>/<version>/.disposable
The marker contains a reproduction recipe. A .keep file pins a version.
Dry-run by default. Source media, native projects and legacy folders are excluded.
"""
import argparse
import json
from pathlib import Path
import shutil
import time


PREVIEW_SUFFIXES = {'.mp4', '.webm', '.png', '.jpg', '.jpeg', '.json', '.txt', '.html', '.ass', '.srt'}


def files_under(folder):
    """Never follow symlinks, including directory links."""
    for item in folder.iterdir():
        if item.is_symlink():
            continue
        if item.is_dir():
            yield from files_under(item)
        elif item.is_file():
            yield item


def inventory(project):
    groups = {}
    generated = project / 'generated'
    if not generated.exists():
        return groups
    if generated.is_symlink():
        raise ValueError('generated must not be a symlink')
    for path in files_under(generated):
        key = ('decoded-frame candidates' if any(p.endswith('-frames') for p in path.parts)
               else path.suffix.lower() or 'other')
        entry = groups.setdefault(key, {'files': 0, 'bytes': 0})
        entry['files'] += 1
        entry['bytes'] += path.stat().st_size
    return groups


def candidates(project, keep=2, days=7, now=None):
    if keep < 2 or days < 1:
        raise ValueError('Keep at least two versions and one day of grace')
    now = time.time() if now is None else now
    base = project / 'generated/wip/previews'
    for folder in [project / 'generated', project / 'generated/wip', base]:
        if folder.is_symlink():
            raise ValueError('Preview directories must not be symlinks')
    if not base.exists():
        return []
    result = []
    for series in sorted(base.iterdir()):
        if not series.is_dir() or series.is_symlink():
            continue
        versions = []
        for version in series.iterdir():
            if not version.is_dir() or version.is_symlink():
                continue
            paths = list(version.rglob('*'))
            # Fail closed on links, nested directories, unknown files or native edits.
            marker = version / '.disposable'
            if (not marker.is_file() or any(p.is_symlink() or not p.is_file() for p in paths)
                    or not marker.read_text(encoding='utf-8').strip()
                    or any(p.name not in {'.disposable', '.keep'}
                           and p.suffix.lower() not in PREVIEW_SUFFIXES for p in paths)):
                continue
            newest = max(p.stat().st_mtime for p in paths)
            versions.append((newest, version, paths))
        versions.sort(key=lambda row: (row[0], row[1].name), reverse=True)
        for newest, version, paths in versions[keep:]:
            if (version / '.keep').exists() or now - newest < days * 86400:
                continue
            result.append({'path': str(version), 'bytes': sum(p.stat().st_size for p in paths)})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--keep', type=int, default=2)
    parser.add_argument('--days', type=int, default=7)
    parser.add_argument('--apply', action='store_true', help='Delete eligible disposable previews')
    args = parser.parse_args()
    project = args.project.resolve()
    if not project.is_dir():
        parser.error('Project directory does not exist')
    items = candidates(project, args.keep, args.days)
    print(json.dumps({'inventory': inventory(project), 'eligible': items,
                      'eligibleBytes': sum(p['bytes'] for p in items),
                      'apply': args.apply}, indent=2))
    if args.apply:
        # Run only when rendering/review is idle; re-evaluate protection before deletion.
        for item in items:
            if item not in candidates(project, args.keep, args.days):
                raise ValueError('Preview changed during cleanup; retry when idle')
            shutil.rmtree(item['path'])


if __name__ == '__main__':
    main()
