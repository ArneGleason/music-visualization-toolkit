"""Prepare the V64 outro from retained, frame-exact V63 source choices."""
import copy
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
OLD = OUT.parent / 'first-contact-motion-v02'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

register = read(BASE/'shots/shotlist.json')
if not (OUT/'prior-shotlist.json').exists():
    assert register['activeReviewEdit'] == 'v63'
    save(OUT/'prior-shotlist.json', register)
entries = copy.deepcopy([e for e in read(OLD/'assembly-plan.json')['entries'] if e['startFrame'] >= 4446])
by_id = {e['shot']: e for e in entries}
by_id['contact-026'].update(frames=38, endFrameExclusive=4484)
by_id['contact-027'].update(startFrame=4484, frames=165)
assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(entries, entries[1:]))
assert sum(e['frames'] for e in entries) == 820
grid = read(BASE/'generated/animatic/animatic-data.json')['beats']
assert any(b['frame'] == 4484 and b['bar'] == 71 and b['beat'] == 2 for b in grid)

for sid in ['contact-027', 'contact-029', 'contact-030', 'contact-031']:
    e = by_id[sid]
    folder = OUT/'sources'/sid
    folder.mkdir(parents=True, exist_ok=True)
    count = e['frames']+8
    if sid == 'contact-027':
        # Use continuous native motion over the longer shot, with interpolated
        # frames and an additional Blender camera move. No frozen tail.
        vf = 'trim=start_frame=0:end_frame=121,setpts=PTS-STARTPTS,setpts=1.5*PTS,minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1'
        e['retiming'] = dict(sourceStartFrame=1, sourceFrames=121, speed=2/3, interpolation='motion compensated 24fps')
    else:
        vf = f"trim=start_frame={e['sourceIn']}:end_frame={e['sourceIn']+count},setpts=N/(24*TB)"
    vf += ',scale=1920:1080,setsar=1'
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(BASE/e['source']),'-vf',vf,'-frames:v',str(count),str(folder/'frame_%04d.png')],check=True)
    assert len(list(folder.glob('frame_*.png'))) == count
    e['effect'] = sid
    print('Prepared',sid,count,'frames',flush=True)

by_id['contact-027-travel']['effect'] = 'travel'
by_id['contact-028-travel']['reverse'] = True
by_id['contact-032']['effect'] = 'finale'
for e in entries:
    if e['shot'] != 'contact-026':
        e['transition'] = dict(type='dissolve',frames=4 if e['shot'] in ['contact-027','contact-032'] else 6,startFrame=e['startFrame'],outgoingHandles=True)

save(OUT/'assembly-plan.json',dict(version='v64',source='v63',fps=24,startFrame=4446,endFrameExclusive=5266,frames=820,entries=entries))
save(BASE/'outro-v63-review.json',dict(
    sourceVersion='v63', targetVersion='v64', newPaidCredits=0,
    directions=[
        'Leave Harper World by 3:07; advance System View to bar 71 beat 2 / frame 4484 and add motion.',
        'Reverse Travel 28 at 3:17.833, using the same selected source interval.',
        'Add a stronger push to Stellar Nursery, a pan/push to Red Star System moon, and a restrained move on Galactic Possibilities.',
        'Travel 27 gets a subtle dark cyan transparent sphere and mild spherical refraction, affecting background only.',
        'Preserve the accepted finale entry. Fade Harper from 3:34 to 3:36, leaving cosmic background.',
        'Final title A Right Little Something; smaller copyright © 2026 Arne Gleason underneath.'
    ],
    title='A Right Little Something',copyright='© 2026 Arne Gleason',
    copyrightNameEvidence='Existing Monsters Undone title credits in the same workspace and Git identity.',
    harperFade=dict(startFrame=5137,endFrame=5185,startSeconds=214,endSeconds=216),
    titleFade=dict(startFrame=5185,endFrame=5197),
    preservedVersion='v63'))
