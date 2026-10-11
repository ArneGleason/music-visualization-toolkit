"""Register Blender departure motion and retain the accepted V57 fallback."""
import copy
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request,urlopen

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v58'
shots={s['id']:s for s in r['storyboardProposals'] if s.get('batch')=='departure-discovery-v01'}
departure=read(OUT/'departure-manifest.json')
ref=(OUT/'departure-pullout-twinkle.mp4').relative_to(BASE).as_posix()
notes='V58: Blender pullout starts 18% closer at 1:51.0 (frame2665), eases to original full frame at 1:53.417 (frame2723). Brief cyan station twinkle peaks at localframe6 and fades by17. Existing reversed source timing stays unchanged; remainder uses original frames. V57 retained as accepted fallback.'
s=shots['departure-002']
selection=copy.deepcopy(s['motionSelection'])
selection.update(id='departure-blender-pullout-v58',motionRef=ref,status='Blender motion-graphics revision; playback review pending',reviewNotes=notes,
    compositor=departure,sourceEditStartFrame=1)
s.setdefault('motionTests',[]).append(selection)
s.update(motionSelection=selection,motionRef=ref,motionReview=dict(usable=True,notes=notes),
    editorialDirection=notes,status='Blender pullout and cyan twinkle in V58; playback review pending')
s['stillPreviewNote']=notes
for placement in s['nativePlacements']: placement.update(motionRef=ref,sourceEditStartFrame=1)
s['animaticPlacement'].update(kind='reversed native motion with Blender pullout and station twinkle',motionRef=ref,
    nativePlacements=s['nativePlacements'],compositor=departure)
edit=r['reviewEdits']['v58']
for entry in edit['entries']:
    if entry['shot']=='departure-002': entry.update(s['animaticPlacement'])
edit.update(type='Stronger optical blur plus Blender departure pullout and twinkle',departureComposite=departure,
    fallbackVersion='v57',fallbackVideo=r['reviewEdits']['v57']['video'])
r['reviewEdits']['v57'].update(userAccepted=True,keepAsFallback=True,
    acceptanceNotes='User says zoom blur helps a ton and much better; explicitly keep this version before trying stronger effects.')
r['departureDiscoverySequence'].update(status='V58 stronger blur and Blender departure preview ready',fallbackVersion='v57')
save(BASE/'shots/shotlist.json',r)
opening=read(BASE/'generated/animatic/current-opening.json')
for item in opening['shots']:
    if item['id'] in shots: item['review']=shots[item['id']]['motionReview']
save(BASE/'generated/animatic/current-opening.json',opening)
verification=read(OUT/'verification.json')
verification.update(departureComposite=departure,fallbackVersion='v57',fallbackPreserved=True)
save(OUT/'verification.json',verification)
plan=read(BASE/'kling-departure-discovery-v01.json')
plan.update(status='Existing media assembled in V58 with stronger zoom overlaps and Blender departure effects',reviewUrl='http://127.0.0.1:8768/?v=v58')
plan.setdefault('editorialRevisions',[]).append(dict(version='v58',shots=['departure-002','departure-004'],
    operation='Stronger radial zoom overlaps; Blender 18 percent pullout plus cyan twinkle',fallbackVersion='v57',newCredits=0))
save(BASE/'kling-departure-discovery-v01.json',plan)
for name in ['PRODUCTION-HANDOFF.md','ESCAPE-DIRECTION.md']:
    path=BASE/name
    head,rest=path.read_text(encoding='utf-8').split('\n',1)
    block='\n## October 11 — V58 stronger zoom and Blender departure effects\n\nUser accepted V57 blur and explicitly requested keeping it as a fallback.\nV58 uses longer radial trails and greater opacity at the same eight optical\ntransitions, still one or two frames each; no timing changes.\nDeparture now has an editable Blender compositor pullout: 1.18x at frame2665\n(1:51.0), smoothly reaching 1.0x at frame2723 (1:53.417). Cyan station twinkle\nat source pixel960,514 peaks at localframe6 and fades by17. Source video speed\nis unchanged. Blender renders local1–59;60–140 reuse the original picture.\nFull-frame return differs by less than0.17 average code values per RGB channel.\nFull5265frames,1080p24fps; original master AAC packets verified. No new spend;\ncumulative3384credits. V57 full video and passage remain intact.\nComparison and editable blend: http://127.0.0.1:8768/storyboard/departure-discovery-motion-v04/\nCurrent review: http://127.0.0.1:8768/?v=v58\nFrame stepping verified: focus the timeline, then Shift+Left/Right; no app change.\n'
    path.write_text(head+'\n'+block+rest,encoding='utf-8')
api='http://127.0.0.1:8768/api/notes'
with urlopen(api,timeout=10) as response: doc=json.load(response)
for note in doc['notes']:
    sid=note.get('sourceShotId')
    if sid not in ['departure-002','departure-004']: continue
    note['resolution']=shots[sid]['motionReview']['notes']
    marker='\nLatest motion direction:' if sid=='departure-002' else '\nLatest optical transition direction:'
    note['text']=note['text'].split(marker)[0]+marker+' '+shots[sid]['motionReview']['notes']
    note['updated_at']=datetime.now(timezone.utc).isoformat()
request=Request(api,data=json.dumps(doc,ensure_ascii=False).encode(),headers={'Content-Type':'application/json'},method='POST')
with urlopen(request,timeout=10) as response: saved=json.load(response)
assert saved['revision']==doc['revision']+1
(OUT/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Departure effects — V58 and V57</title>
<style>body{background:#10282e;color:#efdfc0;font:16px/1.5 system-ui;max-width:1100px;margin:24px auto;padding:0 20px}video{width:100%}a{color:#9bd9e9}section{margin:32px 0}</style>
<h1>Departure effects — compare the versions</h1>
<p><a href="/">Current full animatic</a> · <a href="departure-pullout-twinkle.blend" download>Editable Blender pullout and twinkle</a></p>
<section><h2>V58 · Stronger zoom trails + station pullout and cyan twinkle</h2><video controls preload="metadata" src="timed-still-board.mp4"></video><p>One- or two-frame overlaps, longer trails and greater opacity. Departure starts 18% closer and reaches the full frame by 1:53.4.</p></section>
<section><h2>V57 · Accepted softer version, preserved</h2><video controls preload="metadata" src="../departure-discovery-motion-v03/timed-still-board.mp4"></video><p><a href="/A-Right-Little-Something-selected-motion-v57.mp4#t=111">Original full V57 movie</a></p></section>''',encoding='utf-8')
print('V58 metadata and comparison ready. V57 preserved. Notes revision',saved['revision'])
