"""Register the user-requested pacing revision after all five stills exist."""
import copy
import json
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def save(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

spec = read(OUT/'generation-input.json')
register = read(BASE/'shots/shotlist.json')
assert register['activeReviewEdit'] == 'v45', 'Revision already registered or source changed'
items = {i['id']: i for i in spec['items']}
beats = read(BASE/'generated/beatmap.json')['bars']
def beat_frame(bar, beat):
    return round(next(b for b in beats if b['bar']==bar)['beats'][beat-1]*24)+1

b38, b39, b40, b412 = [beat_frame(*x) for x in [(38,1),(39,1),(40,1),(41,2)]]
assert (b38,b39,b40,b412) == (2294,2359,2425,2507)
revisions = {
    'concourse-006': ('captain-exchange',2211,b38,'Third flip through Guess not and instrumental: hold one two-shot. Captain makes his pitch; Harper calmly shakes her head. Replace the abrupt reaction and near-duplicate departure cuts. Dissolve into the food concourse.'),
    'concourse-008': ('food-concourse',b38,b39,'Harper threads left to right through a lively food concourse. Alien vendors, diners and passing travelers animate the space while she continues her search.'),
    'concourse-009': ('outfitter-market',b39,b40,'Continue left to right through a distinct parts, travel-outfit and exotic-goods arcade. Keep movement purposeful and the aisle legible; no shopping detour.'),
    'concourse-010': ('gantry-pause',b40,b412,'At the gantry entrance Harper pauses, looks toward her ship and gives a small approving smile. Sphere and engine assembly are approximately 80 percent of prior physical size relative to Harper, with a human-sized entrance.'),
    'concourse-011': ('boarding-cut-in',b412,2595,'Cut closer to the entry as Harper steps aboard. Omit the long wide approach; preserve the smaller ship scale and left-to-right travel. Settle inside by the next vocal.'),
}
for sid,(iid,start,end,direction) in revisions.items():
    item=items[iid]
    with Image.open(item['destination']) as im:
        im.verify()
    receipt=read(OUT/(iid+'.actual-generation.json'))
    prompt=receipt.get('prompt',receipt.get('actual_prompt'))
    assert spec['promptLock'] in prompt, iid

for shot in register['storyboardProposals']:
    if shot.get('batch') != 'station-concourse-v01':
        continue
    if shot['id']=='concourse-007':
        shot['batch']='station-concourse-v01-superseded'
        shot['status']='Superseded by continuous captain exchange in V46'
        continue
    shot['batch']='station-concourse-v02'
    if shot['id'] not in revisions:
        shot['motionSelection']['userSelected']=True
        continue
    iid,start,end,direction=revisions[shot['id']]
    item=items[iid]
    shot.setdefault('revisionHistory',[]).append(copy.deepcopy({k:v for k,v in shot.items() if k!='revisionHistory'}))
    receipt=read(OUT/(iid+'.actual-generation.json'))
    prompt=receipt.get('prompt',receipt.get('actual_prompt'))
    with Image.open(item['destination']) as im:
        w,h=im.size
    shot.update(title=item['title'],startFrame=start,endFrameExclusive=end,frames=end-start,
        startSeconds=(start-1)/24,endSeconds=(end-1)/24,
        timingBasis='DAWproject beat grid; first captain onset retains provisional third flip at frame 2211; final boundary retains next vocal at 2595.',
        description=direction,motionDirection=direction,promptLock=spec['promptLock'],imagePrompt=prompt,
        status='Revised still draft; native replacement footage not generated',
        startingFrameDraft=dict(id=iid+'-v01',image=Path(item['destination']).relative_to(BASE).as_posix(),
            userSelected=False,status='Revised composition for user review',generationMode='built-in ImageGen',nativeWidth=w,nativeHeight=h))
    for key in ('motionSelection','motionRef','videoPrompt','transitionIn','cameraMove'):
        shot.pop(key,None)

plan=read(BASE/'kling-station-concourse-v01.json')
transitions=copy.deepcopy(plan['transitions'])
transitions.append(dict(type='dissolve',incomingShot='concourse-008',startFrame=b38-6,endFrameExclusive=b38+6,frames=12))
register['concourseSequence'].setdefault('directionHistory',[]).append(dict(date='2026-10-11',stage='V45 review and requested revision',sourceDirection=register['concourseSequence']['sourceDirection']))
register['concourseSequence'].update(status='V46 still revision: extended captain interaction, inhabited market route, approving pause and smaller-ship boarding cut-in',
    sourceDirection='User requested stills first: extend last flip into captain pitch and head-shake, dissolve to alien-populated food and resources markets, pause approvingly at gantry, reduce personal ship to about 80 percent and cut closer for boarding.',
    stillReview='http://127.0.0.1:8768/storyboard/station-concourse-v02/',
    revisionTransitions=transitions)
save(BASE/'shots/shotlist.json',register)
save(OUT/'review-options.json',dict(id='station-concourse-v02',output=OUT.relative_to(BASE).as_posix(),
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v45.mp4',
    useMotion=True,motionShotIds=['concourse-%03d'%i for i in range(1,6)],draftForReview=True,
    presentation='Accepted native arrival and first two flips followed by five revised still compositions; motion beats are directions, not new animation.',
    mediaLabel='Native opening / revised concourse stills',
    continuationNotes='V46 retains the accepted arrival and ship choices, extends captain exchange and replaces empty walkways with food and resource markets. Five new stills preview the gantry pause, approximately 80 percent ship scale and boarding cut-in. No replacement Kling generation; review stills and pacing first. Original music and 5265-frame timing preserved.',
    transitions=transitions))
print('Registered five revised stills; ten-shot hybrid concourse')
