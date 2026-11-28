"""Replace the history narrative with lyric-led society tableaux."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from timeline import MusicalGrid


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def main():
    folder = BASE / 'production/story-stills-v003'
    folder.mkdir(exist_ok=True)
    canonical = BASE / 'shots/shotlist.json'
    backup = folder / 'previous-shotlist.json'
    if backup.exists():
        raise ValueError('Already prepared; render from the retained snapshot')
    shutil.copy2(canonical, backup)
    old = json.loads(backup.read_text())
    grid = MusicalGrid(json.loads((BASE / 'generated/beatmap.json').read_text()))
    index = {x['label']: x['path'] for x in json.loads(
        (BASE / 'production/image-index.json').read_text())['images']}
    lock = old['shots'][0]['promptLock']
    shots = copy.deepcopy([s for s in old['shots'] if s['endFrameExclusive'] <= 2295])
    for shot in shots:
        shot['startAnchor'] = grid.position(shot['startFrame'] / 24).text()
    entries = [
        (148, 'line-022:start', 'The family beneath the rock',
         'The whole hidden community: connected homes, shared places and living infrastructure. A portrait of society.'),
        (149, 'line-023:start', 'All for one and one for all',
         'Different ant collaborators and living infrastructure contribute to one shared sound-and-light artwork.'),
        (151, 'line-024:start', 'Different roles, connected spaces',
         'Art, research and biological co-design occupy distinct adjoining spaces. Teal, jade and amber color phase.'),
        (152, 'line-025:start', 'One living network supports all',
         'Ants provide reciprocal inputs to the living junction; its branches support the occupied rooms. Ochre and olive.'),
        (153, 'line-026:start', 'Collective reserves',
         'Place gathered and produced goods into fitted storage niches, then let the stores rest on “Keeping quiet to itself”.'),
        (154, 'line-028:start', 'Hidden from the outside',
         'Planned motion: pull back as the cutaway fades beneath still rock; the outside survey craft passes without finding them.'),
    ]
    for number, anchor, title, direction in entries:
        shots.append(dict(id=f'L3-I{number:03}', sceneId='SOCIETY', startAnchor=anchor,
                          title=title, description=direction, reviewDirection=direction,
                          imageLabel=f'Image {number}', starterImage=index[f'Image {number}'],
                          promptLock=lock, status='still_pacing_review'))
    spec = dict(format='musical-anchors-v1', id='story-stills-v003',
                promptLock=lock, endAnchor='line-030:start', shots=shots)
    save(folder / 'batch.json', spec)
    subprocess.run([sys.executable, str(ROOT / 'tools/shotplan.py'), '--merge',
                    '--project', str(BASE / 'project.json'), '--batch', str(folder / 'batch.json')], check=True)
    merged = json.loads(canonical.read_text())
    ids = [s['id'] for s in shots]
    by_id = {s['id']: s for s in merged['shots']}
    merged.setdefault('supersededShots', []).extend(
        dict(s, supersededByBatch=spec['id']) for s in merged['shots'] if s['id'] not in ids)
    merged['shots'] = [by_id[sid] for sid in ids]
    for shot in merged['shots']:
        shot['seconds'] = shot['frames'] / 24
        shot['boundaryBasis'] = dict(start=shot['startAnchor'], end=shot['end'], grid='generated/beatmap.json')
        if shot.get('starterImage'):
            assert (BASE / shot['starterImage']).exists()
    merged['totalFrames'] = merged['endFrameExclusive']
    merged['status'] = 'Lyric-led society tableaux pacing review; later story unplaced'
    merged['reviewScope'] = 'Opening through the lyric-led society verse. Six mixed-media tableaux replace the historical exploration story. Storage carries both shelf/quiet phrases. Final concealment motion is described, not yet generated.'
    assert merged['shots'][0]['startFrame'] == 0
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(merged['shots'], merged['shots'][1:]))
    assert len({s['promptLock'] for s in merged['shots']}) == 1
    assert merged['totalFrames'] == 2877
    for before, after in zip(old['shots'], merged['shots']):
        if before['endFrameExclusive'] > 2295:
            break
        assert (before['startFrame'], before['endFrameExclusive']) == (after['startFrame'], after['endFrameExclusive'])
    save(canonical, merged)
    save(folder / 'shotlist.json', merged)
    for name in ['timeline.json', 'lyrics.compiled.json']:
        shutil.copy2(BASE / 'production/story-stills-v002' / name, folder / name)
    for shot in merged['shots'][-6:]:
        print(f"{shot['startFrame']/24:.3f}–{shot['endFrameExclusive']/24:.3f}: {shot['imageLabel']} ({shot['frames']} frames, {shot['seconds']:.3f}s)")


if __name__ == '__main__':
    main()
