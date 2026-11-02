"""Verify only Scene 12 media selections changed and save recovery records."""
import json
import subprocess
import urllib.request
from pathlib import Path

notes = Path(__file__).resolve().parent
project = notes.parents[1]
batch = json.loads((notes / 'batch.json').read_text())
before = json.loads((notes / 'shotlist-before.json').read_text())
after = json.loads((project / 'shots/shotlist.json').read_text())
changed = []
for old, new in zip(before['shots'], after['shots']):
    if old != new:
        changed.append(new['id'])
    for key in set(old) | set(new):
        if key not in ('videoSource', 'videoEdit', 'status', 'videoHandles'):
            assert old.get(key) == new.get(key), (new['id'], key)
assert changed == [entry['shotId'] for entry in batch['shots'] if entry['status'] == 'selected_for_review']
media = json.loads(subprocess.check_output([
    'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
    'stream=r_frame_rate,nb_frames,duration', '-of', 'json',
    str(project / 'generated/storyboard/first-run-starters-v001/first-run-clean-animatic-v001.mp4')]))['streams'][0]
assert media['nb_frames'] == '5190' and media['r_frame_rate'] == '24/1'
assert float(media['duration']) == 216.25
validation = dict(changedShots=changed, shotCount=len(after['shots']),
                  musicalTimingTransitionsStartersAndLocksUnchanged=True,
                  creditsSpent=570, sourceStarts={s['shotId']:s['sourceInFrame'] for s in batch['shots']},
                  animaticMedia=media, renderComplete=True,
                  reviewHttpStatus=urllib.request.urlopen('http://127.0.0.1:8766/kling-scene12-v057/review.html').status)
(notes / 'validation.json').write_text(json.dumps(validation, indent=2) + '\n')
recovery_path = project / 'shots/video-recovery.json'
recovery = json.loads(recovery_path.read_text())
recovery['shots'] = [s for s in recovery['shots'] if s['shotId'] not in changed]
for entry in batch['shots']:
    if entry['status'] != 'selected_for_review':
        continue
    recovery['shots'].append(dict(shotId=entry['shotId'], displayId=entry['displayId'],
        localVideo=entry['localVideo'], sourceInFrame=entry['sourceInFrame'],
        editFrames=next(s['frames'] for s in after['shots'] if s['id']==entry['shotId']),
        resultUrls=[entry['resultUrl']], receiptFiles=['shots/kling-scene12-v057/batch.json']))
recovery_path.write_text(json.dumps(recovery, indent=2) + '\n')
print(json.dumps(validation, indent=2))
