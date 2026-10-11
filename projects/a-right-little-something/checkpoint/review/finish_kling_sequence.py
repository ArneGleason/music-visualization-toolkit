"""Persist final generation ledger and keep review drafts distinct from approval."""
import json
from pathlib import Path
import urllib.request

base = Path(__file__).resolve().parents[2]
entries = []
for name in ['kling-chorus1-motion-v01.json','kling-window-coast-v01.json']:
    path = base/name
    plan = json.loads(path.read_text(encoding='utf-8'))
    for shot in plan['shots']:
        folder = base/plan['output']/shot['id']
        submission = json.loads((folder/'submission.json').read_text(encoding='utf-8'))['body']
        result = json.loads((folder/'result.json').read_text(encoding='utf-8'))['body']
        assert result['status']=='COMPLETED', (shot['id'],result['status'])
        entries.append(dict(id=shot['id'],shotId=shot['shotId'],generationId=submission['generationId'],credits=submission['creditsConsumed'],status=result['status'],output=folder.relative_to(base).as_posix()))
    plan.update(status='All submitted tasks collected; working motion selections in v20 await user review',actualCredits=sum(e['credits'] for e in entries if e['id'] in {s['id'] for s in plan['shots']}))
    plan['reviewSummary'] = f"{len(plan['shots'])} collected takes, {plan['actualCredits']} credits including comparisons. Working choices are assembled in full animatic v20; user motion review pending."
    path.write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
register = json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))
chosen = {s['id']:s['motionSelection']['id'] for s in register['storyboardProposals'] if s.get('motionSelection') and s['id'] in {'chorus1-01','chorus1-02','chorus1-03','chorus1-04','chorus1-05','space-008','space-009','space-011'}}
assert len(chosen)==8
for e in entries:
    e['workingChoice'] = chosen[e['shotId']]==e['id']
ledger = dict(credits=sum(e['credits'] for e in entries),priorRecordedKlingCredits=936,cumulativeRecordedKlingCredits=936+sum(e['credits'] for e in entries),tasks=entries,workingChoices=chosen,animaticVersion='v20',motionApproval='Pending user review',noTaskPending=True)
assert ledger['credits']==640 and len(entries)==12
(base/'generated/review/kling-sequence-oct10-manifest.json').write_text(json.dumps(ledger,indent=2)+'\n',encoding='utf-8')
project_path = base/'project.json'
project = json.loads(project_path.read_text(encoding='utf-8'))
project['production'].update(animatic='generated/animatic/A-Right-Little-Something-selected-motion-v20.mp4',continuationNotes='V20 working motion drafts cover frames 737–1549: inlet v02, keeper portrait v01, revised arms/tide coast v02, then chorus B/A/B/A/A with mission v02, intervention v01, response v02 and two orbital v01 takes. Chorus cuts in at frame 1046, 43.54s. All motion awaits user review; approved stills and comparison attempts retained. Earlier accepted opening/planet/hologram and original master preserved. 640 credits this run; no task pending.',chorus1MotionReview='http://127.0.0.1:8768/storyboard/kling-chorus1-motion-v01/',windowCoastMotionReview='http://127.0.0.1:8768/storyboard/kling-window-coast-v01/')
project_path.write_text(json.dumps(project,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
with urllib.request.urlopen('http://127.0.0.1:8768/api/notes') as r:
    doc = json.load(r)
for n in doc['notes']:
    sid = n['id'].removesuffix('-ideas-oct10')
    if sid in chosen:
        text = f"Selected still branch approved; working motion draft {chosen[sid]} in animatic v20. User motion review pending. Review: http://127.0.0.1:8768/storyboard/kling-chorus1-motion-v01/"
        n['resolution'] = (n.get('resolution','')+'\n'+text).strip()
request = urllib.request.Request('http://127.0.0.1:8768/api/notes',data=json.dumps(doc).encode(),headers={'Content-Type':'application/json'},method='POST')
with urllib.request.urlopen(request) as r:
    saved = json.load(r)
print('Final ledger:',ledger['credits'],'credits;',len(chosen),'working shots;',len(entries),'completed tasks; notes revision',saved['revision'])
