"""Record the optical overlap edit and update its local review annotation."""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v57'
s=next(s for s in r['storyboardProposals'] if s['id']=='departure-004')
plan=read(BASE/'kling-departure-discovery-v01.json')
plan.update(status='Existing takes and stills assembled in V57; optical zoom overlaps added',reviewUrl='http://127.0.0.1:8768/?v=v57')
plan.setdefault('editorialRevisions',[]).append(dict(version='v57',shotId='departure-004',
    operation='one- or two-frame radial zoom overlaps',transitions=8,changedFrames=14,newCredits=0))
save(BASE/'kling-departure-discovery-v01.json',plan)
for name in ['PRODUCTION-HANDOFF.md','ESCAPE-DIRECTION.md']:
    path=BASE/name
    text=path.read_text(encoding='utf-8')
    head,rest=text.split('\n',1)
    block='\n## October 11 — V57 brief optical zoom overlaps\n\nUser requested a rapid outgoing zoom blur to connect the static magnification\nsteps. Eight transitions now expand the outgoing view toward camera with a\nradial shutter blur, fading over the next static image on its original cue.\nTwo frames per overlap; one frame into the shortest three-frame views\n(cues 3 and 8), leaving clear settled views. Fourteen picture frames affected.\nAll nine cue frames and the final planet hold/reveal are retained; lyrics\nare composited afterward and stay sharp. V56 reversed departure retained;\nuser noted its distant opening might linger but was undecided about changing it.\nFull 5265 frames, 1080p/24fps; master AAC packet hashes match V56.\nNo new generation or spend; cumulative 3384 credits. Playback review pending.\nReview: http://127.0.0.1:8768/?v=v57\nEffect manifest and build: `generated/storyboard/departure-discovery-motion-v03/`.\n'
    path.write_text(head+'\n'+block+rest,encoding='utf-8')
api='http://127.0.0.1:8768/api/notes'
with urlopen(api,timeout=10) as response: notes=json.load(response)
for note in notes['notes']:
    if note.get('sourceShotId')!='departure-004': continue
    note['resolution']=s['motionReview']['notes']
    note['text']+='\nLatest optical transition direction: '+s['motionReview']['notes']
    note['updated_at']=datetime.now(timezone.utc).isoformat()
request=Request(api,data=json.dumps(notes,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'},method='POST')
with urlopen(request,timeout=10) as response: saved=json.load(response)
assert saved['revision']==notes['revision']+1
print('V57 production notes saved; revision',saved['revision'])
