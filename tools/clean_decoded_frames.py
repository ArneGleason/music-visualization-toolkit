"""Verify every cached PNG against its local video before optionally deleting it.

Only animatic_media.Artwork caches with matching source stamps are eligible.
JPEG review samples and all other assets stay intact. Each deleted PNG is
reproducible with the recorded ffmpeg command. Run while rendering is idle.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

from PIL import Image
from project_media import digest


def inspect(folder):
    if folder.is_symlink() or any(p.is_symlink() for p in folder.parents):
        raise ValueError('Symlinked cache')
    source = folder.with_name(folder.name[:-7] + '.mp4')
    stamp = folder / 'source-stamp.txt'
    if source.is_symlink() or stamp.is_symlink():
        raise ValueError('Symlinked source/stamp')
    signature = ast.literal_eval(stamp.read_text())
    before = source.stat()
    if signature[:2] != (before.st_size, before.st_mtime_ns):
        raise ValueError('Source no longer matches cache stamp')
    fps = signature[2]
    if not isinstance(fps, (int, float)) or not 0 < fps <= 240:
        raise ValueError('Invalid fps')
    frames = sorted(p for p in folder.iterdir() if re.fullmatch(r'\d{5}\.png', p.name))
    if not frames or any(p.is_symlink() or not p.is_file() for p in frames):
        raise ValueError('Missing frames or symlinked frame')
    if [p.name for p in frames] != [f'{i:05d}.png' for i in range(len(frames))]:
        raise ValueError('Non-contiguous frame numbering')
    stats = [(p.stat().st_size, p.stat().st_mtime_ns) for p in frames]
    command = ['ffmpeg', '-v', 'error', '-i', str(source), '-map', '0:v:0', '-vf', f'fps={fps}',
               '-pix_fmt', 'rgb24', '-f', 'framemd5', '-']
    output = subprocess.run(command, check=True, capture_output=True, text=True).stdout
    hashes = [line.split(',')[-1].strip() for line in output.splitlines()
              if line and not line.startswith('#')]
    if len(hashes) != len(frames):
        raise ValueError('Decoded frame count differs')
    for path, expected in zip(frames, hashes):
        with Image.open(path) as im:
            actual = hashlib.md5(im.convert('RGB').tobytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'Cached image differs from source: {path.name}')
    record = {'cache': str(folder), 'source': str(source), 'sourceSha256': digest(source),
              'fps': fps, 'frameCount': len(frames),
              'bytes': sum(size for size, _ in stats) + stamp.stat().st_size,
              'regenerate': ['ffmpeg', '-y', '-v', 'error', '-i', str(source),
                             '-vf', f'fps={fps}', '-compression_level', '1',
                             '-start_number', '0', str(folder / '%05d.png')],
              'verification': 'Every RGB pixel of every PNG matches the decoded local video',
              'status': 'verified'}
    if (source.stat().st_size, source.stat().st_mtime_ns) != signature[:2]:
        raise ValueError('Source changed during verification')
    if [(p.stat().st_size, p.stat().st_mtime_ns) for p in frames] != stats:
        raise ValueError('Cache changed during verification')
    return record, frames, stamp


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--workers', type=int, choices=range(1, 5), default=2)
    args = parser.parse_args()
    project = args.project.absolute()
    if args.report.exists():
        parser.error('Choose a new report path; existing receipts are preserved')
    args.report.parent.mkdir(parents=True, exist_ok=True)
    records = []

    def save():
        args.report.write_text(json.dumps({'project': str(project), 'apply': args.apply,
                                          'caches': records}, indent=2) + '\n')

    def check(folder):
        try:
            return folder, inspect(folder), None
        except (ValueError, OSError, SyntaxError, subprocess.CalledProcessError) as error:
            return folder, None, str(error)

    folders = [p for p in sorted((project / 'generated').rglob('*-frames'))
               if p.is_dir() and (p / 'source-stamp.txt').exists()]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for folder, result, error in pool.map(check, folders):
            if error is not None:
                records.append({'cache': str(folder), 'status': 'skipped', 'reason': str(error)})
                save()
                print(f'Skipped {folder.name}: {error}', flush=True)
                continue
            record, frames, stamp = result
            records.append(record)
            save()  # Persist evidence before any deletion.
            if args.apply:
                # Remove stamp first: interrupted deletion must trigger full regeneration.
                stamp.unlink()
                for frame in frames:
                    frame.unlink()
                if not any(folder.iterdir()):
                    folder.rmdir()
                record['status'] = 'deleted'
                save()
            print(f'{record["status"]}: {folder.parent.name}/{folder.name} '
                  f'({record["bytes"] / 1024**3:.2f} GiB)', flush=True)
    print(f'Total removed: {sum(r.get("bytes", 0) for r in records if r["status"] == "deleted") / 1024**3:.2f} GiB')


if __name__ == '__main__':
    main()
