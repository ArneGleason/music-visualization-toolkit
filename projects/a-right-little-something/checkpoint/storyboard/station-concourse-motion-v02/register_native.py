"""Register reviewed replacement motion, keeping the two short flips as stills."""
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

plan=read(BASE/'kling-station-concourse-v02.json')
assert len(plan['collectedShotIds'])==5
r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v49'
reviews=read(OUT/'native-review.json')
shots={s['id']:s for s in r['storyboardProposals'] if s.get('batch')=='station-concourse-v05'}
for take in plan['shots']:
    review=reviews[take['shotId']]
    assert review['usable'],take['shotId']
    for placement in take['placements']:
        s=shots[placement['shotId']]
        source_start=placement['sourceEditStartFrame']
        selected=dict(id=take['id'],motionRef=take['motionRef'],sourceEditStartFrame=source_start,
            sourceLeadInFrames=source_start-1,availableLeadOutFrames=take['nativeFrames']-source_start+1-s['frames'],
            generationId=take['generationId'],plan='kling-station-concourse-v02.json',userSelected=False,
            status='Reviewed native draft; user playback pending',reviewNotes=review['notes'])
        s.setdefault('motionTests',[]).append(selected)
        s.update(motionSelection=selected,motionRef=take['motionRef'],videoPrompt=take['prompt'],motionReview=dict(notes=review['notes']))
for sid in plan['stillShotIds']:
    s=shots[sid]
    for key in ['motionSelection','motionRef']:
        s.pop(key,None)
    s['status']='User selected still for short flip; no native clip used'
    s['motionReview']={'notes':'Approved still with right-to-left reveal wipe; no light-flash overlay requested in this pass.'}
r['concourseSequence']['motionRequest'].update(status='Five replacement takes collected and reviewed; assembling V50',actualCredits=plan['actualCredits'])
save(BASE/'shots/shotlist.json',r)
options=read(BASE/'generated/storyboard/station-concourse-v05/review-options.json')
options.update(output=OUT.relative_to(BASE).as_posix(),sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v49.mp4',
    motionShotIds=plan['retainNativeShotIds']+[p['shotId'] for t in plan['shots'] for p in t['placements']],
    presentation='Clean replacement motion with still bioship/sailcraft flips; walk, consider, resume uses the same native wide take.',
    mediaLabel='Concourse native motion / still ship flips',
    continuationNotes='V50 uses five new native takes for captain, food, market, gantry and entrance close-up. Two sequential gantry excerpts surround consideration. First two ship flips stay approved stills with reveal wipes. Original master audio and full frame count retained. User playback review pending.')
save(OUT/'review-options.json',options)
print('Registered five new takes for six placements; two still flips')
