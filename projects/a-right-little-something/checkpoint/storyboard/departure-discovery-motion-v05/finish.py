"""Save the brighter-twinkle revision in project notes."""
from datetime import datetime,timezone
import json
from pathlib import Path
from urllib.request import Request,urlopen

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v59'
s=next(s for s in r['storyboardProposals'] if s['id']=='departure-002')
plan=read(BASE/'kling-departure-discovery-v01.json')
plan.update(status='V59 brighter station twinkle; accepted V58 stronger zoom and pullout retained',reviewUrl='http://127.0.0.1:8768/?v=v59')
plan.setdefault('editorialRevisions',[]).append(dict(version='v59',shotId='departure-002',operation='Blender twinkle 2x spatial size and 2.5x linear light intensity',newCredits=0))
save(BASE/'kling-departure-discovery-v01.json',plan)
for name in ['PRODUCTION-HANDOFF.md','ESCAPE-DIRECTION.md']:
    path=BASE/name
    head,rest=path.read_text(encoding='utf-8').split('\n',1)
    block='\n## October 11 — V59 more visible cyan twinkle\n\nUser accepts V58 stronger zoom and Blender pullout; requests a more noticeable\ntwinkle. Doubled its spatial size and multiplied linear light by2.5 in Blender.\nSame cyan, anchor and pulse timing (peak local6, gone by17). Only pulse picture\nframes differ; accepted pullout and optical overlaps retained. Full5265frames,\n24fps1080p, original master AAC packets verified identical to V58. No new spend.\nV57 and V58 remain available. Review: http://127.0.0.1:8768/?v=v59\nEditable scene and verification: `generated/storyboard/departure-discovery-motion-v05/`.\n'
    path.write_text(head+'\n'+block+rest,encoding='utf-8')
api='http://127.0.0.1:8768/api/notes'
with urlopen(api,timeout=10) as response: doc=json.load(response)
for note in doc['notes']:
    if note.get('sourceShotId')!='departure-002': continue
    note['resolution']=s['motionReview']['notes']
    marker='\nLatest motion direction:'
    note['text']=note['text'].split(marker)[0]+marker+' '+s['motionReview']['notes']
    note['updated_at']=datetime.now(timezone.utc).isoformat()
request=Request(api,data=json.dumps(doc,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'},method='POST')
with urlopen(request,timeout=10) as response: saved=json.load(response)
assert saved['revision']==doc['revision']+1
print('V59 notes saved; revision',saved['revision'])
