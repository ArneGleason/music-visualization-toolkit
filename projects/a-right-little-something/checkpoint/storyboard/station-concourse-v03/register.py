"""Replace only the rejected boarding shot with approach and decision coverage."""
import copy
import json
from pathlib import Path
from PIL import Image

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

register=read(BASE/'shots/shotlist.json')
assert register['activeReviewEdit']=='v46'
spec=read(OUT/'generation-input.json')
items={i['id']:i for i in spec['items']}
grid=read(BASE/'generated/beatmap.json')['bars']
cut=round(next(b for b in grid if b['bar']==42)['beats'][0]*24)+1
assert cut==2556
rows=[('concourse-011','gantry-approach',2507,cut,
       'Keep the exterior camera in the same place or use a very slow restrained move. Harper approaches along the gantry and stops one or two paces before the entrance, still outside. Keep the entry closed or visually opaque; no cabin reveal or threshold crossing.'),
      ('concourse-012','decision-closeup',cut,2595,
       'Cut to a shoulders-up close-up looking screen right toward the ship. A quiet practical positive decision: yes, I think that will do. Relaxed brow and closed lips; no broad smile or excited performance. End on her decision, before boarding.')]
for _,iid,_,_,_ in rows:
    with Image.open(items[iid]['destination']) as im:
        im.verify()
    receipt=read(OUT/(iid+'.actual-generation.json'))
    assert spec['promptLock'] in receipt.get('prompt',receipt.get('actual_prompt'))

prior=next(s for s in register['storyboardProposals'] if s['id']=='concourse-011')
prior.setdefault('revisionHistory',[]).append(copy.deepcopy({k:v for k,v in prior.items() if k!='revisionHistory'}))
for shot in register['storyboardProposals']:
    if shot.get('batch')=='station-concourse-v02':
        shot['batch']='station-concourse-v03'

for sid,iid,start,end,direction in rows:
    if sid=='concourse-011':
        shot=prior
    else:
        shot=dict(id=sid,batch='station-concourse-v03',type='concept',
            sourceNoteId='concourse-012-direction-oct11',handles=dict(leadInFrames=24,leadOutFrames=24,status='Reserved for later native motion'))
        register['storyboardProposals'].append(shot)
    item=items[iid]
    receipt=read(OUT/(iid+'.actual-generation.json'))
    prompt=receipt.get('prompt',receipt.get('actual_prompt'))
    with Image.open(item['destination']) as im:
        w,h=im.size
    shot.update(title=item['title'],startFrame=start,endFrameExclusive=end,frames=end-start,
        startSeconds=(start-1)/24,endSeconds=(end-1)/24,lyrics=['Instrumental into All, all calling'],
        timingBasis='Existing final-shot start 2507; decision cut at DAWproject bar 42 beat 1, frame 2556; next-vocal boundary 2595 unchanged.',
        description=direction,motionDirection=direction,promptLock=spec['promptLock'],imagePrompt=prompt,
        status='Revised still draft; motion not generated',
        startingFrameDraft=dict(id=iid+'-v01',image=Path(item['destination']).relative_to(BASE).as_posix(),
            userSelected=False,status='Revised ending for user review',generationMode='built-in ImageGen',nativeWidth=w,nativeHeight=h))
    for key in ('motionSelection','motionRef','videoPrompt','transitionIn','cameraMove'):
        shot.pop(key,None)

seq=register['concourseSequence']
seq.setdefault('directionHistory',[]).append(dict(date='2026-10-11',stage='V46 ending revision',sourceDirection=seq['sourceDirection']))
seq.update(status='V47 preserves approved shots; ending approaches, stops outside and cuts to a restrained positive decision',
    sourceDirection='All V46 shots accepted except final boarding view: interior seen through port is incompatible. Replace it with calm gantry approach, stop before entrance, then quiet positive-decision face close-up. Do not show boarding or invent an interior.',
    stillReview='http://127.0.0.1:8768/storyboard/station-concourse-v03/')
save(BASE/'shots/shotlist.json',register)
old=read(OUT.parent/'station-concourse-v02/review-options.json')
old.update(id='station-concourse-v03',output=OUT.relative_to(BASE).as_posix(),
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v46.mp4',
    presentation='Approved prior shots with two revised ending stills: stop outside, then a quiet positive decision.',
    mediaLabel='Approved concourse / revised decision ending',
    continuationNotes='V47 replaces only V46 final boarding still at 2507–2595: gantry approach and stop outside (2507–2556), restrained decision close-up (2556–2595). No interior or boarding shown. Other shots, original master audio and full frame count preserved. New motion awaits still review.')
save(OUT/'review-options.json',old)
save(OUT/'executed.prompt.json',dict(tool='built-in ImageGen',items=[dict(id=i['id'],image=i['destination'],
    prompt=read(OUT/(i['id']+'.actual-generation.json')).get('prompt',read(OUT/(i['id']+'.actual-generation.json')).get('actual_prompt'))) for i in spec['items']]))
print('Registered approach and decision ending, frames2507–2595')
