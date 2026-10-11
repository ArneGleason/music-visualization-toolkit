"""Record the assembled V51 still preview and refresh local review directions."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request,urlopen

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def save(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

register=read(BASE/'shots/shotlist.json')
assert register['activeReviewEdit']=='v51'
timing=read(OUT/'timing-check.json')
shots={s['id']:s for s in register['storyboardProposals'] if s.get('batch')=='departure-discovery-v01'}
edit=register['reviewEdits']['v51']
edit.update(type='Generated held-still timing preview',newKlingCredits=0,stillCount=17,
    zoomCues=timing['zoomCues'],planetRevealFrame=2946,
    pullbackPreview='Two held exterior keyframes with a 12-frame dissolve; eventual continuous camera pullback remains to be animated.')
for entry in edit['entries']:
    shot=shots[entry['shot']]
    entry.update(kind='timed storyboard stills',storyboardSegments=shot['storyboardSegments'])
    shot['animaticPlacement']['kind']='timed storyboard stills'
    note='Generated still timing preview in V51; native action not generated. '
    if shot['id']=='departure-002':
        note+=shot['stillPreviewNote']
    elif shot['id']=='departure-004':
        note+='Nine distinct optical views timed to the nine performed in cues; each cut increases magnification.'
    elif shot['id']=='departure-005':
        note+='Hold the final zoom view until big at2946, then full new-planet reveal through frame2993.'
    else:
        note+=shot['description']
    shot['motionReview']={'notes':note}
register['departureDiscoverySequence'].update(status='V51 still timing preview ready; user review pending',
    generationStatus='17 built-in ImageGen stills assembled; no Kling jobs or spending',
    reviewUrl='http://127.0.0.1:8768/?v=v51',
    stillReviewUrl='http://127.0.0.1:8768/storyboard/departure-discovery-v01/board/index.html')
save(BASE/'shots/shotlist.json',register)
opening=read(BASE/'generated/animatic/current-opening.json')
for entry in opening['shots']:
    if entry['id'] in shots:
        entry['review']=shots[entry['id']]['motionReview']
save(BASE/'generated/animatic/current-opening.json',opening)
save(OUT/'verification.json',dict(version='v51',fullFrames=5265,passageFrames=549,fps=24,
    dimensions=[1920,1080],audio='Original master AAC packet hashes verified equal to V50 by insertion tool',
    uniqueStills=17,zoomCues=timing['zoomCues'],planetRevealFrame=2946,
    noKlingSubmission=True,confirmedCumulativeKlingCredits=3104))
with urlopen('http://127.0.0.1:8768/api/notes',timeout=10) as response:
    notes=json.load(response)
for note in notes['notes']:
    sid=note.get('sourceShotId')
    if sid in shots:
        note['text']=note['text'].replace('Selected text plan; stills and motion not generated.',
            'Generated stills timed in V51; user review pending. Native action not yet generated.')
        note['resolution']=shots[sid]['motionReview']['notes']
        note['updated_at']=datetime.now(timezone.utc).isoformat()
request=Request('http://127.0.0.1:8768/api/notes',data=json.dumps(notes,ensure_ascii=False).encode('utf-8'),
    headers={'Content-Type':'application/json'},method='POST')
with urlopen(request,timeout=10) as response:
    saved=json.load(response)
assert saved['revision']==notes['revision']+1
print('V51 review metadata saved; notes revision',saved['revision'])
