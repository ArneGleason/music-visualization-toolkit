"""Save truthful V49 review status and update the two ending markers."""
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
assert r['activeReviewEdit']=='v49'
spec=read(OUT/'review-options.json')
shots={s['id']:s for s in r['storyboardProposals'] if s.get('batch')==spec['id']}
new_ids=['concourse-010','concourse-012','concourse-013']
edit=r['reviewEdits']['v49']
edit.update(type='approved prior shots with approved stills reblocked as walk-consider-walk',transitions=spec['transitions'],newPaidCredits=0)
for entry in edit['entries']:
    sid=entry['shot'];s=shots[sid]
    if sid in shots:
        entry['userSelected']=True
        s['animaticPlacement']['userSelected']=True
        s['status']='User-approved prior shot retained in V49'
        for key in ('startingFrameDraft','startingFrameSelection'):
            if key in s:
                s[key]['userSelected']=True
    if sid in spec['motionShotIds']:
        entry['kind']='native Kling motion'
        s['animaticPlacement']['kind']='native Kling motion'
r['concourseSequence']['motionRequest']['status']='Prior generation complete; approved market stills plus revised approach/decision ending await next motion pass. No new generation submitted.'
r['concourseSequence']['handoff']='At frame2595 Harper has considered the ship and resumed her approach. She is still outside, walking toward the entrance. Boarding and cabin transition remain unstaged.'
r['concourseSequence']['gantryMotionPlan']=read(OUT/'motion-plan.json')
save(BASE/'shots/shotlist.json',r)
save(OUT/'review-manifest.json',dict(boardId='ce27973e-c009-4d44-8eab-ed01be58c996',animaticVersion='v49',
    status='Approved stills; revised three-part timing for review',generationMode='Reuse approved stills; no new image generation',newKlingCredits=0,motionPlan=read(OUT/'motion-plan.json'),
    items=[dict(id=sid,image=shots[sid]['startingFrameDraft']['image'],startFrame=shots[sid]['startFrame'],
        endFrameExclusive=shots[sid]['endFrameExclusive'],direction=shots[sid]['description']) for sid in new_ids]))
save(OUT/'verification.json',dict(fullFrames=5265,passageFrames=490,fps=24,width=1920,height=1080,
    originalMasterAudio='AAC packet hashes verified equal to V48 by insertion tool',newStillCount=0,
    endingFrames=[2425,2507,2539,2595],noInteriorReveal=True,earlierShotsRetained=True))

api='http://127.0.0.1:8768/api/notes'
with urlopen(api,timeout=10) as response:
    notes=json.load(response)
now=datetime.now(timezone.utc).isoformat()
existing={n.get('sourceShotId'):n for n in notes['notes'] if n.get('sourceShotId')}
for sid in new_ids:
    s=shots[sid]
    if sid not in existing:
        note=dict(id=s['sourceNoteId'],sourceRecording=None,kind='idea',created_at=now,sourceShotId=sid)
        notes['notes'].append(note)
    else:
        note=existing[sid]
    note.update(start=s['startSeconds'],end=s['endSeconds'],start_frame=s['startFrame'],end_frame=s['endFrameExclusive'],
        anchor_label=f"Concourse / frame {s['startFrame']}",batch=spec['id'],status='open',updated_at=now,
        text=f"Concourse / {s['title']}\n\n{s['description']}\n\nFrames {s['startFrame']}–{s['endFrameExclusive']} (end exclusive). Revised still in V49; native motion not generated.",
        resolution='Revised ending for review: http://127.0.0.1:8768/storyboard/station-concourse-v05/')
for note in notes['notes']:
    if note.get('sourceShotId')=='concourse-011':
        note.update(status='addressed',resolution='Superseded: the original gantry now appears before and after the consideration close-up; see concourse-010,012,013.',updated_at=now)
    if note['id']=='concourse-handoff-direction-oct11':
        note.update(text='Concourse / Handoff to All, all calling\n\nHarper has considered the ship, then resumed walking toward its entrance. She remains outside through the end; no cabin is shown through the port. Boarding and the transition into the established opening cabin remain to be staged. Retain the warm-gray pod-issued survival suit; any later wardrobe change remains to be staged.',updated_at=now)
req=Request(api,data=json.dumps(notes,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
with urlopen(req,timeout=10) as response:
    saved=json.load(response)
assert saved['revision']==notes['revision']+1
print('V49 ending markers saved; notes revision',saved['revision'])
