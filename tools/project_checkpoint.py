"""Back up small project metadata; restore missing local files without overwriting."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


METADATA = [
    'generated/beatmap.json', 'generated/timeline.compiled.json',
    'generated/animatic/animatic-data.json', 'generated/animatic/current-opening.json',
    'generated/animatic/current-media.json', 'generated/animatic/blocking-insert-manifest.json',
    'generated/animatic/motion-insert-manifest.json', 'generated/review/listening-notes.json',
    'generated/review/current-render.json',
    'generated/transcription/zoom-nine.alignment.json',
    'generated/transcription/audio.whisper.raw.json',
    'generated/transcription/lead.whisper.raw.json',
    'generated/transcription/leadRenaissance.whisper.raw.json',
]

# Preserve authored text from ignored production folders, without copying media,
# provider result URLs, account captures, caches or nested historical checkpoints.
PRODUCTION_METADATA = {
    'generation-input.json', 'source-verification.json', 'timing-check.json',
    'verification.json', 'review-manifest.json', 'review-options.json',
    'native-review.json', 'assembly-plan.json', 'pullback-frame-map.json',
    'reverse-frame-map.json', 'departure-manifest.json',
    'gallery-manifest.json', 'gallery-options.json', 'concat.txt', 'lyrics.ass',
    'generation-plan.json', 'still-validation.json',
    'selection-overrides.json', 'media-manifest.json', 'qa-observations.json',
    'source-manifest.json', 'star-tracks.json', 'title.ass',
}


def checkpoint_sources(base):
    names = {name for name in METADATA if (base/name).is_file()}
    generated = base/'generated'
    for source in generated.rglob('*'):
        if not source.is_file():
            continue
        relative = source.relative_to(generated)
        if {'__pycache__', 'checkpoints'} & set(relative.parts):
            continue
        authored = (source.suffix == '.py' or source.name.endswith('.prompt.txt')
                    or source.name.endswith('.prompt.json')
                    or source.name.endswith('.actual-generation.json'))
        metadata = source.name in PRODUCTION_METADATA
        receipt = (relative.parts[0] == 'kling-tests'
                   and source.name in {'request.json', 'submission.json'})
        if (authored or metadata or receipt) and source.stat().st_size <= 1024*1024:
            names.add(source.relative_to(base).as_posix())
    return sorted(names)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--restore', action='store_true')
    args = parser.parse_args()
    base = args.project.resolve().parent
    folder = base/'checkpoint'
    if args.restore:
        manifests = [folder/'manifest.json', base/'reference-images/manifest.json']
        for manifest in manifests:
            for entry in json.loads(manifest.read_text(encoding='utf-8'))['files']:
                source, target = base/entry['backup'], base/entry['source']
                assert base in source.resolve().parents and base in target.resolve().parents
                assert digest(source) == entry['sha256'], source
                if target.exists():
                    print('KEPT', entry['source'])
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                print('RESTORED', entry['source'])
    else:
        folder.mkdir(exist_ok=True)
        entries = []
        for name in checkpoint_sources(base):
            source = base/name
            if not source.exists():
                continue
            backup = folder/Path(name).relative_to('generated')
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, backup)
            assert digest(source) == digest(backup)
            entries.append({'source': name, 'backup': backup.relative_to(base).as_posix(),
                            'sha256': digest(backup), 'bytes': backup.stat().st_size})
        (folder/'manifest.json').write_text(json.dumps({'schemaVersion': 1,
            'purpose': 'Small metadata, authored scripts, exact prompts and job receipts; no new media, fonts, models or provider result URLs',
            'files': entries}, indent=2)+'\n', encoding='utf-8')
        print('CHECKPOINT', len(entries), 'metadata files')


if __name__ == '__main__':
    main()
