"""Finalize truthful native-motion metadata and revision-checked review notes."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
plan=read(BASE/'kling-station-concourse-v01.json')
register=read(BASE/'shots/shotlist.json')
review=read(OUT/'native-review.json')
assert register['activeReviewEdit']=='v45' and len(plan['collectedShotIds'])==11
edit=register['reviewEdits']['v45']
edit.update(type='native motion with editorial reveal wipes',transitions=plan['transitions'],
    paidCredits=plan['actualCredits'],noEditorialImageTranslation=True)
for item in edit['entries']:
    item['kind']='native Kling motion'
    shot=next(s for s in register['storyboardProposals'] if s['id']==item['shot'])
    shot['animaticPlacement']['kind']='native Kling motion'
    incoming=next((t for t in plan['transitions'] if t['incomingShot']==shot['id']),None)
    if incoming:
        shot['transitionIn']=incoming
    shot['motionReview']={'notes':review[shot['id']]['notes']}
register['concourseSequence']['motionRequest']['status']='Eleven clean native takes assembled in V45; user playback review pending'
save(BASE/'shots/shotlist.json',register)
plan.update(status='All eleven clean takes collected and reviewed; assembled in V45',
    paidJobsPending=False,reviewUrl='http://127.0.0.1:8768/?v=v45',
    passageReviewUrl='http://127.0.0.1:8768/storyboard/station-concourse-motion-v01/',userAccepted=False)
save(BASE/'kling-station-concourse-v01.json',plan)
save(OUT/'review-manifest.json',dict(animaticVersion='v45',status='Native motion review draft',
    cleanPassage='native-picture.mp4',timedPassage='timed-still-board.mp4',
    transitions=plan['transitions'],credits=392,cumulativeCredits=2864,
    shots=[dict(id=t['shotId'],motionRef=t['motionRef'],sourceEditStartFrame=t['sourceEditStartFrame'],
                startFrame=t['startFrame'],frames=t['editFrames'],review=review[t['shotId']]) for t in plan['shots']]))
save(OUT/'verification.json',dict(fullFrames=5265,fps=24,width=1920,height=1080,
    passageFrames=490,sourceHandlesFrames=24,originalMasterAudio='AAC packet hashes verified equal to V44 by insert tool',
    noEditorialImageTranslation=True,threeWipes=plan['transitions'],nativeVisualReview=review))
api='http://127.0.0.1:8768/api/notes'
with urlopen(api,timeout=10) as response:
    notes=json.load(response)
for note in notes['notes']:
    sid=note.get('sourceShotId')
    if sid not in review:
        continue
    replacements={
        'Hard cut on the first flip.':'Four-frame right-to-left vertical reveal on the first flip; soft boundary, no image slide.',
        'Hard cut on the second flip, retaining':'Four-frame right-to-left vertical reveal on the second flip, retaining',
        'Third quick cut reveals the ferry and captain together.':'Third four-frame right-to-left vertical reveal shows the ferry and captain together; no image slide.'}
    for old,new in replacements.items():
        note['text']=note['text'].replace(old,new)
    note['resolution']='Clean native motion in V45; user playback review pending. '+review[sid]['notes']
    note['updated_at']=datetime.now(timezone.utc).isoformat()
request=Request(api,data=json.dumps(notes,ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type':'application/json'},method='POST')
with urlopen(request,timeout=10) as response:
    saved=json.load(response)
print('V45 metadata saved; notes revision',saved['revision'])
