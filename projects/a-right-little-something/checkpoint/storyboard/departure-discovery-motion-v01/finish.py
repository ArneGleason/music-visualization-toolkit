"""Finalize reviewed V55 native placements and revision-checked app notes."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request,urlopen

OUT=Path(__file__).resolve().parent;BASE=OUT.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
r=read(BASE/'shots/shotlist.json');assert r['activeReviewEdit']=='v55'
plan=read(BASE/'kling-departure-discovery-v01.json')
assert len(plan['collectedShotIds'])==7 and plan['actualCredits']==280
reviews=read(OUT/'native-review.json')
shots={s['id']:s for s in r['storyboardProposals'] if s.get('batch')=='departure-discovery-v01'}
edit=r['reviewEdits']['v55']
edit.update(type='Seven native Kling takes with nine optical still views',newPaidCredits=280,cumulativeCredits=3384,departureDissolve=False,stillSegments=plan['stillSegments'])
for entry in edit['entries']:
    s=shots[entry['shot']]
    if s['id'] in reviews:
        kind='native Kling motion' if s['id']!='departure-005' else '26-frame optical still hold then 48-frame native planet reveal'
        if s['id']=='departure-002':
            kind='native Kling pullback with editorial speed ramp'
            s['motionRef']=s['motionSelection']['motionRef']
            entry['retime']=s['motionSelection']['retime']
        entry.update(kind=kind,nativePlacements=s['nativePlacements'])
        s['animaticPlacement'].update(kind=kind,nativePlacements=s['nativePlacements'])
        s['motionReview']=reviews[s['id']]
        s['status']='Reviewed native motion in V55; user playback pending'
    else:
        s['status']='Accepted nine still views at exact optical zoom cues'
        s['animaticPlacement'].update(kind='nine timed static optical views',userSelected=True)
        entry.update(kind='nine timed static optical views',userSelected=True)
        s['motionReview']={'notes':'Nine accepted optical still views preserved on exact performed in cues; no paid zoom jobs.'}
shots['departure-002']['stillPreviewNote']='Superseded by one continuous native camera pullback in V55; no dissolve.'
r['departureDiscoverySequence']['motionRequest'].update(status='Seven clean native takes assembled in V55; user playback pending',actualCredits=280,cumulativeCredits=3384)
r['departureDiscoverySequence'].update(status='V55 native motion review ready',reviewUrl='http://127.0.0.1:8768/?v=v55',motionReviewUrl='http://127.0.0.1:8768/storyboard/departure-discovery-motion-v01/',generationStatus='Seven clean native takes collected, 280 credits; no paid jobs pending')
save(BASE/'shots/shotlist.json',r)
opening=read(BASE/'generated/animatic/current-opening.json')
for item in opening['shots']:
    if item['id'] in shots: item['review']=shots[item['id']]['motionReview']
save(BASE/'generated/animatic/current-opening.json',opening)
plan.update(status='Seven clean native takes collected and assembled in V55; user playback pending',paidJobsPending=False,reviewUrl='http://127.0.0.1:8768/?v=v55')
save(BASE/'kling-departure-discovery-v01.json',plan)
save(OUT/'verification.json',dict(fullFrames=5265,passageFrames=549,fps=24,width=1920,height=1080,originalMasterAudio='AAC packets verified identical to V54',newNativeTakes=7,newCredits=280,cumulativeCredits=3384,departureDissolve=False,review=reviews))
save(OUT/'review-manifest.json',dict(animaticVersion='v55',status='Native playback review draft',takes=[dict(id=t['id'],motionRef=t['motionRef'],editMotionRef=t.get('editMotionRef'),retime=t.get('retime'),placements=t['placements'],review=reviews[t['shotId']]) for t in plan['shots']],stillSegments=plan['stillSegments']))
api='http://127.0.0.1:8768/api/notes'
with urlopen(api,timeout=10) as response: notes=json.load(response)
for note in notes['notes']:
    sid=note.get('sourceShotId')
    if sid not in shots: continue
    note['resolution']=shots[sid]['motionReview']['notes']
    note['text']=note['text'].replace('Generated stills timed in V54; user review pending. Native action not yet generated.','Clean motion assembled in V55; user playback review pending.').replace('V54 still preview, review pending.','V55 native motion preview, review pending.')
    if sid=='departure-002':
        note['text']+='\nLatest motion direction: immediate brisk camera pullback so the large Harper view passes quickly. Ship moves gently; camera supplies speed. No dissolve. '+reviews[sid]['notes']
    if sid=='departure-004': note['text']=note['text'].replace('Clean motion assembled in V55; user playback review pending.','Accepted nine optical still cuts retained in V55.')
    note['updated_at']=datetime.now(timezone.utc).isoformat()
request=Request(api,data=json.dumps(notes,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
with urlopen(request,timeout=10) as response: saved=json.load(response)
assert saved['revision']==notes['revision']+1
print('V55 metadata and notes saved; revision',saved['revision'])
