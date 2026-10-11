"""Register reviewed native selections before inserting the assembled passage."""
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
plan=read(BASE/'kling-station-concourse-v01.json')
assert len(plan['collectedShotIds'])==11
register=read(BASE/'shots/shotlist.json')
shots={s['id']:s for s in register['storyboardProposals']}
reviews=read(OUT/'native-review.json')
for take in plan['shots']:
    shot=shots[take['shotId']]
    review=reviews[take['shotId']]
    assert review['usable'], take['shotId']
    selected=dict(id=take['id'],motionRef=take['motionRef'],sourceEditStartFrame=take['sourceEditStartFrame'],
        sourceLeadInFrames=take['sourceEditStartFrame']-1,
        availableLeadOutFrames=take['nativeFrames']-(take['sourceEditStartFrame']-1)-take['editFrames'],
        userSelected=False,status='Agent-reviewed clean native draft; user playback review pending',
        generationId=take['generationId'],plan='kling-station-concourse-v01.json',reviewNotes=review['notes'])
    shot.setdefault('motionTests',[]).append(selected)
    shot.update(motionSelection=selected,motionRef=take['motionRef'],motionReview=dict(notes=review['notes']),
                status='Clean native motion ready for assembly',videoPrompt=take['prompt'])
register['concourseSequence']['motionRequest']['status']='Collected and agent-reviewed; assembling'
save(BASE/'shots/shotlist.json',register)
save(OUT/'review-options.json',dict(id='station-concourse-v01',output=OUT.relative_to(BASE).as_posix(),
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v44.mp4',
    useMotion=True,motionShotIds=[t['shotId'] for t in plan['shots']],draftForReview=True,
    presentation='Clean native concourse motion with stationary-image right-to-left flip wipes.',
    mediaLabel='Native motion / concourse flip wipes',
    continuationNotes='V45 replaces eleven concourse stills with reviewed clean Kling motion, frames2105–2595. Three four-frame right-to-left vertical reveal wipes on the flips, no image translation. Original master audio and full frame count retained. Native takes remain user playback review drafts.'))
print('Registered 11 reviewed native takes')
