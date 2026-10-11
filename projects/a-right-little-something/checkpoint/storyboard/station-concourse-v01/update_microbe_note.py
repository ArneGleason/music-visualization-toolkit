"""Update only the two revised directions through the revision-checked API."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[3]
register = json.loads((BASE/'shots/shotlist.json').read_text(encoding='utf-8'))
shots = {s['id']: s for s in register['storyboardProposals']
         if s['id'] in ('concourse-004',)}
api = 'http://127.0.0.1:8768/api/notes'
with urlopen(api, timeout=10) as response:
    notes = json.load(response)
changed = 0
for note in notes['notes']:
    shot = shots.get(note.get('sourceShotId'))
    if not shot:
        continue
    note['text'] = (f"Concourse / {shot['title']}\n\nSelected direction: {shot['description']}"
        f"\n\nStaging: {shot['motionDirection']}\n\nProposed span: frames "
        f"{shot['startFrame']}-{shot['endFrameExclusive']} (end exclusive); anchor: "
        f"{shot['timingBasis']}. Canonical direction: shots/shotlist.json, {shot['id']}.")
    note['resolution'] = 'Revised ship still in V43; user review pending. Other imagery and timing retained. Review: http://127.0.0.1:8768/storyboard/station-concourse-v01/'
    note['updated_at'] = datetime.now(timezone.utc).isoformat()
    changed += 1
assert changed == 1
request = Request(api, data=json.dumps(notes,ensure_ascii=False).encode('utf-8'),
                  headers={'Content-Type':'application/json'}, method='POST')
with urlopen(request, timeout=10) as response:
    saved = json.load(response)
print('Updated first flip direction; notes revision', saved['revision'])
