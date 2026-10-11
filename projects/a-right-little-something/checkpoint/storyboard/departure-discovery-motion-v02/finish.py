"""Record the user-requested reversal in local production notes."""
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v56'
s=next(s for s in r['storyboardProposals'] if s['id']=='departure-002')
frame_map=read(OUT.with_name('departure-discovery-motion-v01')/'pullback-frame-map.json')
save(OUT/'reverse-frame-map.json',[dict(editFrame=i+1,nativeSourceFrame=row['nativeSourceFrame'],priorEditFrame=row['editFrame']) for i,row in enumerate(reversed(frame_map))])
plan=read(BASE/'kling-departure-discovery-v01.json')
plan.update(status='Existing takes assembled in V56; departure reversed per user direction',reviewUrl='http://127.0.0.1:8768/?v=v56')
plan['editorialRevision']=dict(version='v56',shotId='departure-002',operation='reverse',motionRef=s['motionRef'],frames=140,newCredits=0)
save(BASE/'kling-departure-discovery-v01.json',plan)
for name in ['PRODUCTION-HANDOFF.md','ESCAPE-DIRECTION.md']:
    path=BASE/name
    text=path.read_text(encoding='utf-8')
    head,rest=text.split('\n',1)
    block='\n## October 11 — V56 departure reversed\n\nUser requested literal reversal of “To the bigger sky beyond” so the ship\ncomes out from the station. Reversed the accepted clean 140-frame picture\n at frames 2665–2805 (exclusive end); forward lyrics and original music retained.\nAll other shot selections and timings retained. Full 5265 frames, 1080p/24fps,\nmaster AAC packets verified identical to V55. No new generation or spending;\ncumulative 3384 credits. V55 retained as prior version.\nReview: http://127.0.0.1:8768/?v=v56\nClean reversal and provenance: `generated/storyboard/departure-discovery-motion-v02/`.\n'
    path.write_text(head+'\n'+block+rest,encoding='utf-8')
api='http://127.0.0.1:8768/api/notes'
with urlopen(api,timeout=10) as response: notes=json.load(response)
for note in notes['notes']:
    if note.get('sourceShotId')!='departure-002': continue
    note['resolution']=s['motionReview']['notes']
    note['text']=note['text'].split('\nLatest motion direction:')[0]+'\nLatest motion direction: '+s['motionReview']['notes']
    note['updated_at']=datetime.now(timezone.utc).isoformat()
request=Request(api,data=json.dumps(notes,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'},method='POST')
with urlopen(request,timeout=10) as response: saved=json.load(response)
assert saved['revision']==notes['revision']+1
print('V56 production notes saved; revision',saved['revision'])
