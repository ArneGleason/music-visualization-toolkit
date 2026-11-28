"""Assemble the reviewed lyric-led opening through the hidden-world history."""
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
    folder = BASE / 'production/story-stills-v002'
    folder.mkdir(exist_ok=True)
    canonical = BASE / 'shots/shotlist.json'
    backup = folder / 'previous-shotlist.json'
    if backup.exists():
        raise ValueError('Preparation already performed; use the saved snapshot for rendering')
    shutil.copy2(canonical, backup)
    old = json.loads(backup.read_text())
    grid = MusicalGrid(json.loads((BASE / 'generated/beatmap.json').read_text()))
    index = {x['label']: x['path'] for x in json.loads(
        (BASE / 'production/image-index.json').read_text())['images']}
    lock = old['shots'][0]['promptLock']
    # Preserve the accepted first thirty seconds, including original source trims.
    opening = copy.deepcopy(old['shots'][:9])
    for shot in opening:
        shot['startAnchor'] = grid.position(shot['startFrame'] / 24).text()
    entries = [
        (99, grid.position(723/24).text(), 'A living threshold',
         'Move into ant territory: plain stone, dignified statue and living lights; no relief-reading.'),
        (102, 'line-006:start', 'The route leads downward',
         'Follow the stairs toward the dignified gateway; living machinery pulses and works below.'),
        (105, 'line-008:start', 'A platform over the depths',
         'Board the large solid platform. Its motion is supported invisibly; no gears or energy bridge.'),
        (106, 'line-009:start', 'Descending into the world',
         'Closer on the pair as the platform descends; the entrance recedes high above them.'),
        (109, 'line-010:start', 'Something beyond the dark hall',
         'Approach through a wide dark hall. Keep the gathering indistinct until the chorus reveal.'),
        (112, 'line-012:start', 'Harper smiles',
         'Cut onto Harper smiling on “I gotta smile on”; Taffy watches from deeper shadow.'),
        (120, 'line-014:start', 'The secret is a living society',
         'Reveal the communal comedy on “Open up the secret room”; a broad audience joins the performance.'),
        (122, 'line-015:start', 'Come on through',
         'Harper beckons Taffy into the sheltered aisle. Both remain unnoticed.'),
        (123, 'line-016:start', 'Hiding from the surveyors',
         'Human mineral prospectors scan the crater. Concealment makes the hidden city appear unpromising.'),
        (124, 'line-017:start', 'Faster than we go',
         'The complete survey craft accelerates away; hold on the apparently ordinary crater wall.'),
        (125, 'line-018:start', 'Back to the comedy',
         'The woodlouse reaches for the offered snack; performers play the comic beat.'),
        (127, 'line-019:start', 'Still here together',
         'Taffy suppresses a laugh; Harper shares the moment. They have not yet noticed the guard.'),
        (132, 'line-020:start', 'Backing into the waiting guard',
         'Detected, they recoil into the guard already behind them. His lamp reveals the encounter.'),
        (133, 'line-021:end', 'A courteous direction',
         'Reverse angle: the guard gestures down the hall. Polite guidance also removes their freedom to roam.'),
        (134, '54.1', 'Comfortable hospitality',
         'Arrive in the waiting chamber: food, curved seating and a welcoming host. Settle before the story.'),
        (135, 'line-022:start', 'Hear the story of the family',
         'The host begins; Harper and Taffy listen with interest and concern. Cut into a different illustrative style.'),
        (141, 'line-023:start', 'Scouts leave home',
         'Paper history: explorers depart together from their home world.'),
        (143, 'line-023:end', 'Exploration across nearby stars',
         'Four scouts take separate routes to distinct systems; let the map read before following one.'),
        (140, 'line-024:end', 'An overwhelming discovery',
         'The scout encounters a vast unfamiliar civilization. Unease develops through posture, not an attack.'),
        (145, 'line-025:end', 'The scout withdraws',
         'Hard cut to the wide view; the scout departs diagonally away. Outsider ships remain stationary.'),
        (146, 'line-026:end', 'Inventing concealment together',
         'Ant controls and living infrastructure cooperate; a rock-pattern illusion flows across the gateway.'),
        (147, 'line-028:start', 'Hidden and protected',
         'A cutaway reveals the civilization deep beneath barren rock. Close on “hidden from memory / where we can’t see”.'),
    ]
    shots = opening
    for number, anchor, title, direction in entries:
        shots.append(dict(id=f'L2-I{number:03}', sceneId='HISTORY' if number >= 135 else 'LYRIC2',
                          startAnchor=anchor, title=title, description=direction,
                          reviewDirection=direction, imageLabel=f'Image {number}',
                          starterImage=index[f'Image {number}'], promptLock=lock,
                          status='still_pacing_review'))
    spec = dict(format='musical-anchors-v1', id='story-stills-v002',
                promptLock=lock, endAnchor='line-030:start', shots=shots)
    save(folder / 'batch.json', spec)
    subprocess.run([sys.executable, str(ROOT / 'tools/shotplan.py'), '--merge',
                    '--project', str(BASE / 'project.json'), '--batch', str(folder / 'batch.json')], check=True)
    merged = json.loads(canonical.read_text())
    ids = [s['id'] for s in shots]
    by_id = {s['id']: s for s in merged['shots']}
    retired = [s for s in merged['shots'] if s['id'] not in ids]
    merged.setdefault('supersededShots', []).extend(
        dict(s, supersededByBatch=spec['id']) for s in retired)
    merged['shots'] = [by_id[sid] for sid in ids]
    for shot in merged['shots']:
        shot['seconds'] = shot['frames'] / 24
        shot['boundaryBasis'] = dict(start=shot['startAnchor'],
                                    end=shot['end'], grid='generated/beatmap.json')
        if shot.get('starterImage'):
            assert (BASE / shot['starterImage']).exists(), shot['starterImage']
    merged['totalFrames'] = merged['endFrameExclusive']
    merged['status'] = 'Lyric-led second-pass review through history ending; later story intentionally unplaced'
    merged['reviewScope'] = 'Opening through the hidden-world history, ending before the next chorus. Later holding-room hack and council remain unplaced; prior full-song plan retained in previous-shotlist.json and supersededShots.'
    assert merged['shots'][0]['startFrame'] == 0
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(merged['shots'], merged['shots'][1:]))
    assert len({s['promptLock'] for s in merged['shots']}) == 1
    save(canonical, merged)
    save(folder / 'shotlist.json', merged)
    shutil.copy2(BASE / 'production/story-stills-v001/timeline.json', folder / 'timeline.json')
    shutil.copy2(BASE / 'generated/timeline.compiled.json', folder / 'lyrics.compiled.json')
    for shot in merged['shots']:
        print(f"{shot['startFrame']/24:7.3f}–{shot['endFrameExclusive']/24:7.3f}  {shot['frames']:3}f  {shot.get('imageLabel', 'MOTION'):9} {shot['title']}")


if __name__ == '__main__':
    main()
