"""Finalize V50 selections, receipts and local review notes after assembly."""
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

r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v50'
plan=read(BASE/'kling-station-concourse-v02.json')
assert len(plan['collectedShotIds'])==5 and plan['actualCredits']==240
reviews=read(OUT/'native-review.json')
spec=read(OUT/'review-options.json')
shots={s['id']:s for s in r['storyboardProposals'] if s.get('batch')==spec['id']}
review_by_shot={p['shotId']:reviews[t['shotId']] for t in plan['shots'] for p in t['placements']}
edit=r['reviewEdits']['v50']
edit.update(type='native character motion and still ship flips',transitions=spec['transitions'],newPaidCredits=240,
    stillShotIds=plan['stillShotIds'],noEditorialImageTranslation=True)
for entry in edit['entries']:
    s=shots[entry['shot']]
    if entry['shot'] in spec['motionShotIds']:
        entry['kind']='native Kling motion'
        s['animaticPlacement']['kind']='native Kling motion'
    if entry['shot'] in plan['stillShotIds']:
        entry.update(kind='static still with reveal wipe',userSelected=True)
        s['animaticPlacement'].update(kind='static still with reveal wipe',userSelected=True)
        s['status']='User-selected still flip in V50'
        s['motionReview']={'notes':'Approved still with right-to-left reveal wipe; no native footage or lighting overlay used.'}
        for field in ['startingFrameDraft','startingFrameSelection']:
            s[field]['userSelected']=True
    if entry['shot'] in review_by_shot:
        s['motionReview']=review_by_shot[entry['shot']]
    transition=next((t for t in plan['transitions'] if t['incomingShot']==entry['shot']),None)
    if transition:
        s['transitionIn']=transition
r['concourseSequence']['motionRequest'].update(status='Five replacement takes assembled in V50; user playback review pending',actualCredits=240,cumulativeCredits=3104)
r['concourseSequence']['gantryMotionPlan']['status']='Generated and assembled; see Kling v02 plan for actual source selections'
save(BASE/'shots/shotlist.json',r)
opening=read(BASE/'generated/animatic/current-opening.json')
for item in opening['shots']:
    if item['id'] in shots:
        item['review']=shots[item['id']]['motionReview']
save(BASE/'generated/animatic/current-opening.json',opening)
plan.update(status='Five clean takes collected and assembled in V50; user playback pending',paidJobsPending=False,
    reviewUrl='http://127.0.0.1:8768/?v=v50',passageReviewUrl='http://127.0.0.1:8768/storyboard/station-concourse-motion-v02/')
save(BASE/'kling-station-concourse-v02.json',plan)
save(OUT/'review-manifest.json',dict(animaticVersion='v50',status='Native playback review draft',credits=240,cumulativeCredits=3104,
    stillShotIds=plan['stillShotIds'],transitions=plan['transitions'],
    takes=[dict(id=t['id'],motionRef=t['motionRef'],placements=t['placements'],review=reviews[t['shotId']]) for t in plan['shots']]))
save(OUT/'verification.json',dict(fullFrames=5265,passageFrames=490,fps=24,width=1920,height=1080,
    originalMasterAudio='AAC packet hashes verified equal to V49 by insertion tool',newNativeTakes=5,stillFlips=plan['stillShotIds'],
    noEditorialImageTranslation=True,review=reviews))
api='http://127.0.0.1:8768/api/notes'
with urlopen(api,timeout=10) as response:
    notes=json.load(response)
for note in notes['notes']:
    sid=note.get('sourceShotId')
    if sid in review_by_shot:
        note['resolution']='Clean native take in V50; user playback pending. '+review_by_shot[sid]['notes']
        note['text']=note['text'].replace('Revised still in V49; native motion not generated.','Clean native motion in V50; user playback review pending.')
        note['text']=note['text'].replace('Still composition draft in V46; motion remains to be generated after review.','Clean native motion in V50; user playback review pending.')
    elif sid in plan['stillShotIds']:
        note['resolution']='V50 uses the approved still for this brief flip with a right-to-left reveal wipe. Native ship footage not used.'
    else:
        continue
    note['updated_at']=datetime.now(timezone.utc).isoformat()
req=Request(api,data=json.dumps(notes,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
with urlopen(req,timeout=10) as response:
    saved=json.load(response)
assert saved['revision']==notes['revision']+1
print('V50 saved; notes revision',saved['revision'])
