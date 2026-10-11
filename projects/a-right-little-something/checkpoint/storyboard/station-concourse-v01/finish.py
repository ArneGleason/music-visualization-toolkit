"""Save V40 review metadata and reconcile wardrobe notes after rendering."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
manifest_path = OUT/'manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest.update(fullAnimaticChanged=True, animaticVersion='v40',
    fullAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v40.mp4',
    status='Composition and wardrobe drafts; user review pending',
    timingCaveat='Third flip and Guess share provisional frame 2211; keep playback review before locking motion cuts.',
    wardrobe='Warm-gray pod-issued survival coverall, changed into offscreen in transit; same suit throughout the station sequence.')
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
canonical = json.loads((BASE/'shots/shotlist.json').read_text(encoding='utf-8'))
shots = [s for s in canonical['storyboardProposals'] if s.get('batch')=='station-concourse-v01']
checks = []
for shot in shots:
    image = BASE/shot['startingFrameDraft']['image']
    checks.append({'id':shot['id'],'image':shot['startingFrameDraft']['image'],
                   'sha256':hashlib.sha256(image.read_bytes()).hexdigest(),
                   'prompt':shot['imagePrompt'],'startFrame':shot['startFrame'],
                   'endFrameExclusive':shot['endFrameExclusive']})
(OUT/'review-manifest.json').write_text(json.dumps({'boardId':'ce27973e-c009-4d44-8eab-ed01be58c996',
    'tool':'built-in ImageGen','status':'User review pending','items':checks},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
api = 'http://127.0.0.1:8768/api/notes'
with urlopen(api, timeout=10) as response:
    notes=json.load(response)
for note in notes['notes']:
    if note.get('batch')!='station-concourse-v01':
        continue
    note['resolution']='Still draft in full animatic V40; user review pending. Wardrobe: pod-issued warm-gray survival coverall, changed into offscreen during transit. Review: http://127.0.0.1:8768/storyboard/station-concourse-v01/'
    note['updated_at']=datetime.now(timezone.utc).isoformat()
    if note['id']=='concourse-handoff-direction-oct11':
        note['text']=note['text'].replace('Resolve the silver-to-gray wardrobe bridge during blocking before creating the new imagery.', 'The current still draft uses a warm-gray pod-issued survival coverall found during transit. Retain it through station discovery; a later change into the opening short-sleeve outfit remains to be staged.')
request=Request(api,data=json.dumps(notes,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
with urlopen(request,timeout=10) as response:
    saved=json.load(response)
print('V40 metadata saved; notes revision',saved['revision'])
