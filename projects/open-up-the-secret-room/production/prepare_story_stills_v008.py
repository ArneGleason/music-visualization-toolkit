"""Split the storage verse on Keeping quiet to itself."""
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
    folder = BASE / 'production/story-stills-v008'
    folder.mkdir(exist_ok=True)
    canonical = BASE / 'shots/shotlist.json'
    if (folder / 'previous-shotlist.json').exists():
        raise ValueError('Already prepared; use retained render snapshot')
    shutil.copy2(canonical, folder / 'previous-shotlist.json')
    before = json.loads(canonical.read_text())
    arrival = next(s for s in before['shots'] if s['id'] == 'L3-I153')
    direction = 'Close view of provisions resting beneath living membranes. Quiet, dim blue-plum storage; a faint settling movement planned. Cut on Keeping quiet to itself.'
    shot = dict(id='L8-I159', sceneId='SOCIETY', startAnchor='line-027:start',
                title='Keeping quiet to itself', description=direction,
                reviewDirection=direction, imageLabel='Image 159',
                starterImage='generated/storyboard/society-quiet-stores-v001/image-159.png',
                status='still_pacing_review')
    spec = dict(format='musical-anchors-v1', id='story-stills-v008',
                promptLock=before['shots'][0]['promptLock'], endAnchor='line-028:start',
                shots=[arrival, shot])
    save(folder / 'batch.json', spec)
    subprocess.run([sys.executable, str(ROOT / 'tools/shotplan.py'), '--merge', '--project',
                    str(BASE / 'project.json'), '--batch', str(folder / 'batch.json')], check=True)
    merged = json.loads(canonical.read_text())
    for s in merged['shots']:
        s['seconds'] = s['frames'] / 24
        if s['id'] in ('L3-I153', 'L8-I159'):
            s['boundaryBasis'] = dict(start=s['startAnchor'], end=s['end'], grid='generated/beatmap.json')
    merged['endFrameExclusive'] = merged['shots'][-1]['endFrameExclusive']
    merged['totalFrames'] = merged['endFrameExclusive']
    assert merged['totalFrames'] == before['totalFrames'] == 2923
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(merged['shots'], merged['shots'][1:]))
    assert len({s['promptLock'] for s in merged['shots']}) == 1
    prior = {s['id']:s for s in before['shots']}
    for s in merged['shots']:
        if s['id'] not in ('L3-I153','L8-I159'):
            assert s == prior[s['id']]
    merged['status'] = 'Society verse with separate quiet storage close-up; pending review'
    merged['reviewScope'] = 'Split only storage153 at line-027:start into quiet close-up159. All other timing and images unchanged. Static review; motion remains unmade.'
    save(canonical, merged)
    save(folder / 'shotlist.json', merged)
    for name in ['timeline.json','lyrics.compiled.json']:
        shutil.copy2(BASE / 'production/story-stills-v007' / name, folder / name)
    for s in merged['shots']:
        if s['id'] in ('L3-I153','L8-I159'):
            print(s['imageLabel'],s['startFrame'],s['endFrameExclusive'],s['seconds'])


if __name__ == '__main__':
    main()
