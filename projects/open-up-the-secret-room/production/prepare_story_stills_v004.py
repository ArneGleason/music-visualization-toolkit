"""Append the contrasting listening response on the next smile lyric."""
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
    folder = BASE / 'production/story-stills-v004'
    folder.mkdir(exist_ok=True)
    canonical = BASE / 'shots/shotlist.json'
    if (folder / 'previous-shotlist.json').exists():
        raise ValueError('Already prepared; render from snapshot')
    shutil.copy2(canonical, folder / 'previous-shotlist.json')
    before = json.loads(canonical.read_text())
    direction = 'Only Taffy smiles in fascination. Harper is serious and thoughtful, understanding why the civilization must remain hidden.'
    shot = dict(id='L4-I155', sceneId='LISTENING', startAnchor='line-030:start',
                title='A smile and an understanding', description=direction,
                reviewDirection=direction, imageLabel='Image 155',
                starterImage='generated/storyboard/story-listening-response-v001/image-155.png',
                status='still_pacing_review')
    spec = dict(format='musical-anchors-v1', id='story-stills-v004',
                promptLock=before['shots'][0]['promptLock'], endAnchor='line-031:start', shots=[shot])
    save(folder / 'batch.json', spec)
    subprocess.run([sys.executable, str(ROOT / 'tools/shotplan.py'), '--merge', '--project',
                    str(BASE / 'project.json'), '--batch', str(folder / 'batch.json')], check=True)
    merged = json.loads(canonical.read_text())
    assert merged['shots'][:-1] == before['shots']
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(merged['shots'], merged['shots'][1:]))
    last = merged['shots'][-1]
    last['seconds'] = last['frames'] / 24
    last['boundaryBasis'] = dict(start='line-030:start', end='line-031:start', grid='generated/beatmap.json')
    merged['totalFrames'] = merged['endFrameExclusive']
    merged['status'] = 'Society verse plus listening response on smile lyric; pending review'
    merged['reviewScope'] = 'Opening and lyric-led society tableaux, followed by Image155 on I gotta smile on. Only Taffy smiles; Harper is serious. Ends at the next lyric; later story remains unplaced. Static review, no generated concealment motion.'
    assert len({s['promptLock'] for s in merged['shots']}) == 1
    save(canonical, merged)
    save(folder / 'shotlist.json', merged)
    for name in ['timeline.json', 'lyrics.compiled.json']:
        shutil.copy2(BASE / 'production/story-stills-v003' / name, folder / name)
    print(f"Image155: {last['startFrame']}–{last['endFrameExclusive']} exclusive, {last['frames']} frames; total {merged['totalFrames']}")


if __name__ == '__main__':
    main()
