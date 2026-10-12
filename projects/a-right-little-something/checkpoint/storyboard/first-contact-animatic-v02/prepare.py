"""Retime the closing tour on DAW beats and archive the removed ship insert."""
import copy
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')


path = BASE/'shots/shotlist.json'
register = read(path)
backup = OUT/'prior-shotlist.json'
if not backup.exists():
    save(backup, register)
prior = read(backup)
data = read(BASE/'generated/animatic/animatic-data.json')
beats = {(b['bar'], b['beat']): b['frame'] for b in data['beats']}
schedule = [
    ('contact-027', 72, 4), ('contact-027-travel', 73, 4),
    ('contact-028', 74, 2), ('contact-028-travel', 75, 2),
    ('contact-029', 75, 4), ('contact-029-travel', 76, 4),
    ('contact-030', 77, 2), ('contact-030-travel', 78, 1),
    ('contact-031', 78, 3), ('contact-032', 79, 3),
]
ids = [row[0] for row in schedule]
cuts = [beats[(bar, beat)] for _, bar, beat in schedule] + [data['frames']+1]
assert cuts[-2] == 5031 and (cuts[-2]-1)/data['fps'] <= 210
removed_id = 'contact-031-travel'
removed = next((s for s in register['storyboardProposals'] if s['id'] == removed_id), None)
if removed:
    removed = copy.deepcopy(removed)
    removed.update(status='Removed from V61 at user request; source preserved',
                   supersededBy='contact-032', supersededInVersion='v61')
    register['supersededStoryboardProposals'].append(removed)
    register['storyboardProposals'] = [s for s in register['storyboardProposals'] if s['id'] != removed_id]
entries = []
for index, (shot_id, bar, beat) in enumerate(schedule):
    shot = next(s for s in register['storyboardProposals'] if s['id'] == shot_id)
    original = next(s for s in prior['storyboardProposals'] if s['id'] == shot_id)
    start, end = cuts[index:index+2]
    timing = dict(startFrame=start, endFrameExclusive=end, frames=end-start)
    shot.setdefault('timingHistory', [])
    if not any(h.get('animaticVersion') == 'v60' for h in shot['timingHistory']):
        shot['timingHistory'].append(dict(animaticVersion='v60', **{k: original[k] for k in timing}))
    shot.update(**timing, startSeconds=(start-1)/24, endSeconds=(end-1)/24,
                timingBasis=f'V61 user-requested earlier finale; DAW beat {bar}.{beat}')
    assert len(shot['storyboardSegments']) == 1
    shot['storyboardSegments'][0].update(timing)
    if shot_id == 'contact-032':
        shot['compositePlan'].update(timing)
        shot['compositePlan']['entryDirection'] = 'Direct cut from galaxy, Harper already visible; no intervening ship shot.'
    entries.append(dict(shot=shot_id, image=shot['still'], beat=f'{bar}.{beat}', **timing))
sequence = sorted((s for s in register['storyboardProposals'] if s.get('batch') == 'first-contact-v01'), key=lambda s:s['startFrame'])
assert len(sequence) == 36
assert all(a['endFrameExclusive'] == b['startFrame'] for a, b in zip(sequence, sequence[1:]))
assert sequence[-2]['id'] == 'contact-031' and sequence[-1]['id'] == 'contact-032'
save(path, register)
save(OUT/'assembly-plan.json', dict(version='v61', sourceVersion='v60', fps=24,
    startFrame=cuts[0], endFrameExclusive=cuts[-1], frames=cuts[-1]-cuts[0],
    entries=entries, removedShotIds=[removed_id],
    direction='Cut from galaxy directly to Harper superimposition at 3:29.583, holding to song end.',
    finaleBlender='finale-two-plates.blend', separateVideoSources=True))
save(OUT/'review-options.json', dict(id='first-contact-v01', shotIds=ids,
    output=OUT.relative_to(BASE).as_posix(),
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v60.mp4',
    draftForReview=False, mediaLabel='Earlier Harper finale / still animatic',
    presentation='V60 through frame4582; tightened destination holds, four travel bridges, galaxy directly into Harper at frame5031.',
    continuationNotes='V61: Harper superimposition begins on DAW beat79.3 at 3:29.583 and lasts235frames. Final ship insert removed. Separate video plates remain planned for Blender. Timing review pending; V60 preserved.'))
print('Planned V61: 36 total shots, direct galaxy-to-Harper cut at frame5031, 235-frame finale.')
