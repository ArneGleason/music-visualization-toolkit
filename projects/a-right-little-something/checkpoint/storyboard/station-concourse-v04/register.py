"""Restore the annotated original gantry view and add an entrance reverse angle."""
import copy
import hashlib
import json
from pathlib import Path
from PIL import Image

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v47'
spec=read(OUT/'generation-input.json')
original=BASE/'generated/storyboard/station-concourse-v01/concourse-011.png'
assert hashlib.sha256(original.read_bytes()).digest()==hashlib.sha256((OUT/'original-gantry.png').read_bytes()).digest()
grid=read(BASE/'generated/beatmap.json')['bars']
assert round(next(b for b in grid if b['bar']==40)['beats'][0]*24)+1==2425
assert round(next(b for b in grid if b['bar']==42)['beats'][0]*24)+1==2556
for s in r['storyboardProposals']:
    if s.get('batch')!='station-concourse-v03':
        continue
    if s['id'] in ['concourse-010','concourse-011','concourse-012']:
        s.setdefault('revisionHistory',[]).append(copy.deepcopy({k:v for k,v in s.items() if k!='revisionHistory'}))
    if s['id']=='concourse-011':
        s.update(batch='station-concourse-v03-superseded',status='Superseded: original gantry view now spans both exterior beats in concourse-010')
        continue
    s['batch']='station-concourse-v04'
    if s['id'] not in ['concourse-010','concourse-012']:
        continue
    wide=s['id']=='concourse-010'
    image=OUT/('original-gantry.png' if wide else 'entrance-pov-closeup.png')
    with Image.open(image) as im:
        im.verify()
    with Image.open(image) as im:
        w,h=im.size
    start,end=(2425,2556) if wide else (2556,2595)
    direction=('Use the exact user-annotated Discover the opening ship original. One continuous exterior view: Harper approaches a little and stops midway on the gantry. Fixed camera or restrained slow move; preserve ship, station and gantry relationship. Stop outside; no boarding or cabin reveal.' if wide else
        'Cut decisively to the reverse angle from the ship entrance, looking back along the gantry toward the station. Harper remains midway on the gantry, nearly face-on, looking toward the entrance. Quiet practical positive decision, relaxed face and closed lips; no big smile. Station portal and railings behind her; sphere behind camera and out of frame.')
    prompt=(BASE/'generated/storyboard/station-concourse-v01/concourse-011.prompt.txt').read_text(encoding='utf-8') if wide else spec['prompt']
    s.update(title='Discover the opening ship — original gantry' if wide else 'Decision from the ship entrance',
        startFrame=start,endFrameExclusive=end,frames=end-start,startSeconds=(start-1)/24,endSeconds=(end-1)/24,
        timingBasis='DAWproject bar40 beat1 to bar42 beat1, then existing next-vocal boundary at2595.',
        description=direction,motionDirection=direction,imagePrompt=prompt,promptLock=spec['promptLock'],
        startingFrameDraft=dict(id='concourse-011-still-v01' if wide else 'entrance-pov-closeup-v01',
            image=image.relative_to(BASE).as_posix(),userSelected=wide,status='User reselected original' if wide else 'New reverse angle for review',
            generationMode='Reused original ImageGen still' if wide else 'built-in ImageGen',nativeWidth=w,nativeHeight=h),
        status='Reselected original gantry still' if wide else 'Reverse-angle still draft')
    for key in ['motionSelection','motionRef','videoPrompt','transitionIn','cameraMove']:
        s.pop(key,None)
seq=r['concourseSequence']
seq.setdefault('directionHistory',[]).append(dict(date='2026-10-11',stage='V47 spatial continuity rejected',sourceDirection=seq['sourceDirection']))
seq.update(status='V48: annotated original gantry restored, then entrance POV close-up',
    sourceDirection='User annotated Discover the opening ship, concourse-011-still-v01: back to using this one. Restore its unchanged gantry/ship composition, stop her there, then face-on close-up from entrance looking back toward station. Remove inconsistent successive exterior versions.',
    scaleReview='User reselected the exact original gantry still; its original ship scale supersedes the earlier approximate80percent variant.',
    stillReview='http://127.0.0.1:8768/storyboard/station-concourse-v04/')
save(BASE/'shots/shotlist.json',r)
options=read(OUT.parent/'station-concourse-v03/review-options.json')
options.update(id='station-concourse-v04',output=OUT.relative_to(BASE).as_posix(),sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v47.mp4',
    presentation='Restored exact original gantry view, followed by new entrance POV close-up.',
    mediaLabel='Original gantry / entrance reverse angle',
    continuationNotes='V48 consolidates frames2425–2556 into the exact annotated original gantry still, then uses a face-on entrance POV at2556–2595. Station is behind Harper in the close-up. No boarding or cabin reveal. Earlier scenes, full timing and master audio retained. Stills for review; no new Kling generation.')
save(OUT/'review-options.json',options)
print('Registered original gantry and entrance POV')
