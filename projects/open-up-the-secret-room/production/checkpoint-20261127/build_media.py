"""Rebuild this checkpoint's media archive from its retained explicit inventory."""
import hashlib
import json
from pathlib import Path
import zipfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parents[1]
TAG = 'secret-room-20261127-stills-v001'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    names = json.loads((HERE / 'media-files.json').read_text())
    archive = ROOT / 'out/transfer' / (TAG + '.zip')
    archive.parent.mkdir(parents=True, exist_ok=True)
    entries = []
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for name in names:
            source = ROOT / name
            assert source.resolve().is_relative_to(ROOT)
            assert 'wip' not in source.parts
            entries.append(dict(path=name, bytes=source.stat().st_size, sha256=digest(source)))
            bundle.write(source, name)
    manifest = dict(schemaVersion=1, repository='ArneGleason/music-visualization-toolkit',
                    access='public', tag=TAG, archive=archive.name,
                    sha256=digest(archive), bytes=archive.stat().st_size,
                    scope='All Secret Room stills through Image160, references and concept alternatives; source audio and cached timing; two reused original opening clips. No rendered MP4 previews or WIP caches.',
                    files=entries,
                    url=f'https://github.com/ArneGleason/music-visualization-toolkit/releases/download/{TAG}/{archive.name}')
    (PROJECT / 'media-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Packed {len(entries)} files, {archive.stat().st_size:,} bytes: {archive}')


if __name__ == '__main__':
    main()
