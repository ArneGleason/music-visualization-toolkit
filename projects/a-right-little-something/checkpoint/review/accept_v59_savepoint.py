"""Accept V59 and archive curated current image references for Git."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

BASE=Path(__file__).resolve().parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v59'
now=datetime.now(timezone.utc).isoformat()
note='User accepted V59 as the save point before taking a break: stronger optical zoom overlaps, Blender departure pullout and enlarged cyan twinkle.'
r['reviewEdits']['v59'].update(userAccepted=True,status='Accepted save point',acceptedAt=now,acceptanceNotes=note)
selected=[s for s in r['storyboardProposals'] if s.get('batch') in ['station-concourse-v05','departure-discovery-v01']]
for s in selected:
    s['status']='User-accepted V59 save point'
    s['animaticPlacement']['userSelected']=True
    for key in ['motionSelection','startingFrameSelection']:
        if key in s: s[key].update(userSelected=True,status='Accepted in V59 save point')
seq=r['departureDiscoverySequence']
seq.update(status='V59 accepted save point; user taking a break',acceptedVersion='v59',acceptedAt=now)
seq['motionRequest']['status']='Accepted V59; all generation complete; no jobs pending'
save(BASE/'shots/shotlist.json',r)
project=read(BASE/'project.json')
project['production']['continuationNotes']=note+' Next planned work starts at frame3144 (130.958s), the second chorus/new jungle world. V57 is preserved as the softer-zoom fallback. Matching opening ship shots to the new ship reference remains future work.'
save(BASE/'project.json',project)

manifest=read(BASE/'reference-images/manifest.json')
existing={e['source']:e for e in manifest['files']}
candidates={}
for s in selected:
    image=(s.get('startingFrameSelection') or s.get('startingFrameDraft') or {}).get('image')
    if image: candidates[image]=s['id']+' / '+s['title']+'; accepted V59 visual reference'
    for seg in s.get('storyboardSegments',[]):
        if seg.get('image'): candidates[seg['image']]='Accepted optical magnification view / '+seg.get('asset',s['id'])
for t in read(BASE/'kling-departure-discovery-v01.json')['shots']:
    for key in ['firstImage','tailImage']:
        if t.get(key): candidates.setdefault(t[key],t['shotId']+' / accepted generation '+key)
ship=r['continuityReferences']['personalSphereShip']
for key in ['image','geometrySource','scaleSource']:
    candidates.setdefault(ship[key],'Personal sphere ship continuity / '+key+'; use for future opening match')
added=[]
for name,role in sorted(candidates.items()):
    source=BASE/name
    assert source.is_file(),source
    assert source.suffix.lower() in {'.png','.jpg','.jpeg','.webp'}
    if name in existing: continue
    relative=Path(name).relative_to('generated/storyboard')
    backup=BASE/'reference-images'/relative
    backup.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,backup)
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest==hashlib.sha256(backup.read_bytes()).hexdigest()
    entry=dict(source=name,backup=backup.relative_to(BASE).as_posix(),role=role,bytes=source.stat().st_size,sha256=digest)
    manifest['files'].append(entry)
    added.append(entry)
manifest.update(acceptedVersion='v59',updatedAt=now)
save(BASE/'reference-images/manifest.json',manifest)
(BASE/'reference-images/README.md').write_text('''# Curated image references

These are exact copies of useful accepted stills, not video renders or frame caches.
`manifest.json` records the original generated path, visual role, size and SHA-256.
Existing identity/opening/hologram references are retained. The V59 save point adds
the selected concourse, ship options, gantry, departure/discovery and nine zoom views,
plus the new sphere ship continuity sources for a future opening match.

Run `tools/project_checkpoint.py projects/a-right-little-something/project.json --restore`
with the repository Python environment to restore missing local metadata and image
references. Existing local files are not overwritten. Audio, generated videos,
Blender scenes, full frame sequences and final renders remain on the production
machine under ignored folders; Git does not contain a complete media backup.
''',encoding='utf-8')
for name in ['PRODUCTION-HANDOFF.md','ESCAPE-DIRECTION.md']:
    path=BASE/name
    head,rest=path.read_text(encoding='utf-8').split('\n',1)
    block='\n## October 11 — accepted V59 save point / break\n\n'+note+'\nFull edit: 5265 frames, 1080p at24fps, original master audio. No paid jobs\npending; cumulative spend3384credits. V57 softer zoom and V58 prior twinkle\nremain local fallbacks. New work resumes at frame3144 (2:10.958), the second\nchorus/new jungle world; no new generation or planning is requested during\nthe break. Matching intro ship shots to the accepted sphere design is still\nfuture work. Canonical decisions: `shots/shotlist.json`. Curated exact image\nreferences: `reference-images/manifest.json`. Small metadata, prompts and\nrebuild scripts: `checkpoint/`. Large footage, audio, frame caches, blends\nand full renders stay local and excluded from Git.\n'
    path.write_text(head+'\n'+block+rest,encoding='utf-8')
print('V59 accepted. Added',len(added),'reference images;',round(sum(e['bytes'] for e in added)/1048576,1),'MiB; largest',round(max(e['bytes'] for e in added)/1048576,2),'MiB.')
