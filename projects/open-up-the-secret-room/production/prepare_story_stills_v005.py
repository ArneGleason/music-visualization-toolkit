"""Bookend the society verse with an uncertain listening introduction."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def main():
    folder = BASE / 'production/story-stills-v005'
    folder.mkdir(exist_ok=True)
    canonical = BASE / 'shots/shotlist.json'
    if (folder / 'previous-shotlist.json').exists():
        raise ValueError('Already prepared; use retained render snapshot')
    shutil.copy2(canonical, folder / 'previous-shotlist.json')
    before = json.loads(canonical.read_text())
    arrival = next(s for s in before['shots'] if s['id'] == 'L2-I134')
    direction = 'The storyteller begins. Harper and Taffy both look worried and puzzled; neither smiles. Contrast with their different responses afterward.'
    shot = dict(id='L5-I156', sceneId='LISTENING', startAnchor='56.1',
                title='Before they understand', description=direction,
                reviewDirection=direction, imageLabel='Image 156',
                starterImage='generated/storyboard/story-listening-intro-v001/image-156.png',
                status='still_pacing_review')
    spec = dict(format='musical-anchors-v1', id='story-stills-v005',
                promptLock=before['shots'][0]['promptLock'], endAnchor='line-022:start',
                shots=[arrival, shot])
    save(folder / 'batch.json', spec)
    subprocess.run([sys.executable, str(ROOT / 'tools/shotplan.py'), '--merge', '--project',
                    str(BASE / 'project.json'), '--batch', str(folder / 'batch.json')], check=True)
    merged = json.loads(canonical.read_text())
    for s in merged['shots']:
        s['seconds'] = s['frames'] / 24
        if s['id'] in ('L2-I134', 'L5-I156'):
            s['boundaryBasis'] = dict(start=s['startAnchor'], end=s['end'], grid='generated/beatmap.json')
    merged['endFrameExclusive'] = merged['shots'][-1]['endFrameExclusive']
    merged['totalFrames'] = merged['endFrameExclusive']
    assert merged['totalFrames'] == before['totalFrames'] == 2923
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(merged['shots'], merged['shots'][1:]))
    assert len({s['promptLock'] for s in merged['shots']}) == 1
    prior = {s['id']:s for s in before['shots']}
    for s in merged['shots']:
        if s['id'] not in ('L2-I134','L5-I156'):
            assert s == prior[s['id']]
    merged['status'] = 'Society verse with contrasting listener bookends; pending review'
    merged['reviewScope'] = 'Opening storyteller156: both listeners worried/puzzled. Society tableaux keep their accepted lyric timing. Ending155: serious understanding Harper, smiling fascinated Taffy. Static review; future opening inserts and concealment motion remain unmade.'
    save(canonical, merged)
    save(folder / 'shotlist.json', merged)
    for name in ['timeline.json','lyrics.compiled.json']:
        shutil.copy2(BASE / 'production/story-stills-v004' / name, folder / name)
    for s in merged['shots']:
        if s['id'] in ('L2-I134','L5-I156'):
            print(s['imageLabel'],s['startFrame'],s['endFrameExclusive'],s['seconds'])


if __name__ == '__main__':
    main()
