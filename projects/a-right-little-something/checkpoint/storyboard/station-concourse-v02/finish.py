"""Reconcile V46 review notes and metadata after the verified hybrid export."""
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

register=read(BASE/'shots/shotlist.json')
assert register['activeReviewEdit']=='v46'
spec=read(OUT/'review-options.json')
shots={s['id']:s for s in register['storyboardProposals'] if s.get('batch')==spec['id']}
edit=register['reviewEdits']['v46']
edit.update(type='retained native motion and revised stills',transitions=spec['transitions'],newPaidCredits=0)
for entry in edit['entries']:
    sid=entry['shot']
    if sid in spec['motionShotIds']:
        entry.update(kind='native Kling motion',userSelected=True)
        shots[sid]['animaticPlacement'].update(kind='native Kling motion',userSelected=True)
        shots[sid]['status']='User-reviewed native footage retained in V46'
    transition=next((t for t in spec['transitions'] if t['incomingShot']==sid),None)
    if transition:
        shots[sid]['transitionIn']=transition
register['concourseSequence']['scaleReview']='Smaller ship framing and human-sized entry; exact 20 percent physical reduction remains approximate because the gantry perspective changed.'
register['concourseSequence']['timingReview']='Third flip and Guess retain the existing provisional frame 2211; their compiled lyric timing is unchanged. The rejection is now an action within the extended captain shot, not a separate six-frame cut.'
register['concourseSequence']['motionRequest']['status']='V45 generated batch complete; five replacement stills in V46 await review before any new native generation'
save(BASE/'shots/shotlist.json',register)
save(OUT/'review-manifest.json',dict(boardId='ce27973e-c009-4d44-8eab-ed01be58c996',
    animaticVersion='v46',status='Five revised stills; user review pending',generationMode='built-in ImageGen',
    newKlingJobs=0,newKlingCredits=0,cumulativeKlingCredits=2864,
    items=[dict(id=s['id'],title=s['title'],image=s['startingFrameDraft']['image'],
        startFrame=s['startFrame'],endFrameExclusive=s['endFrameExclusive'],direction=s['description'])
        for s in shots.values() if s['id'] not in spec['motionShotIds']]))
save(OUT/'verification.json',dict(fullFrames=5265,passageFrames=490,fps=24,width=1920,height=1080,
    masterAudio='Original AAC packet hashes verified equal to V45 by insertion tool',
    transitions=spec['transitions'],nativeRetained=spec['motionShotIds'],
    newStillCount=5,noEditorialImageTranslation=True,reviewStatus='Composition and pacing draft; static poses do not demonstrate head-shake or walking motion'))

api='http://127.0.0.1:8768/api/notes'
with urlopen(api,timeout=10) as r:
    notes=json.load(r)
for note in notes['notes']:
    sid=note.get('sourceShotId')
    if sid=='concourse-007':
        note.update(status='addressed',resolution='Superseded in V46 by one continuous captain pitch/refusal scene, frames 2211–2294. No separate six-frame reaction cut.')
    elif sid in shots and sid not in spec['motionShotIds']:
        s=shots[sid]
        note.update(start=s['startSeconds'],end=s['endSeconds'],start_frame=s['startFrame'],
            end_frame=s['endFrameExclusive'],anchor_label=f"Concourse / frame {s['startFrame']}",
            batch=spec['id'],status='open',
            text=f"Concourse / {s['title']}\n\nRevised direction: {s['description']}\n\nSpan: frames {s['startFrame']}–{s['endFrameExclusive']} (end exclusive). Still composition draft in V46; motion remains to be generated after review.",
            resolution='Revised still and timing review: http://127.0.0.1:8768/storyboard/station-concourse-v02/')
    else:
        continue
    note['updated_at']=datetime.now(timezone.utc).isoformat()
req=Request(api,data=json.dumps(notes,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
with urlopen(req,timeout=10) as r:
    saved=json.load(r)
assert saved['revision']==notes['revision']+1
print('V46 metadata and revised notes saved; revision',saved['revision'])
