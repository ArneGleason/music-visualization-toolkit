"""Select the reviewed tower cutaway; preserve every musical boundary."""
import json
import subprocess
from pathlib import Path
notes = Path(__file__).resolve().parent
project = notes.parents[1]
output = project / 'generated/tower-blackout-v070'
batch = json.loads((notes / 'batch.json').read_text())
entry = batch['shots'][0]
assert entry['status'] == 'reviewed'
video = output / 'S12-SH07.mp4'
media = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,duration','-of','json',str(video)]))['streams'][0]
assert media['r_frame_rate'] == '24/1'
score = json.loads((project / 'shots/shotlist.json').read_text())
shot = next(s for s in score['shots'] if s['id'] == 'S12-SH07')
start = entry['sourceInFrame']; count = int(media['nb_frames']); end = start + shot['frames']
assert start >= 24 and count-end >= 24
story = 'The main tower controls go dark. The controller tries a dead control and looks up in alarm as port control fails.'
shot.update(title='Port control goes dark', action=story, description=story, reviewOverlay=story, camera='Modest push toward the controller and main console.', acting='Sudden alarm as her controls stop responding; urgent attempted input and a startled look up.', videoSource=str(video.relative_to(project)), starterImage=entry['starter'], starterRevision='v069', status='motion_review', motionReview='shots/tower-blackout-v070/batch.json')
shot['videoEdit'] = {'sourceInFrame':start}
shot['starterCandidate']['status']='selected'
shot['motionDirection']={'prompt':entry['prompt'],'status':'generated_selected_for_review'}
shot['motionDirectionCandidate']['status']='generated_selected_for_review'
shot['videoHandles'].update(status='generated', editInSourceFrame=start, editOutSourceFrameExclusive=end, availableHeadFrames=start, availableTailFrames=count-end, availableInFrames=start, availableOutFrames=count-end, sourceFrames=count, sourceStartMasterFrame=shot['startFrame']-start, sourceEndMasterFrameExclusive=shot['startFrame']-start+count, note='v070 tower cutaway; full one-second handles retained.')
shot['motionReviewNote']=entry['reviewNote']
(project/'shots/shotlist.json').write_text(json.dumps(score,indent=2)+'\n')
entry.update(status='selected_for_review',media=media,localVideo=shot['videoSource'])
(notes/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
f=project/'shots/video-recovery.json'; recovery=json.loads(f.read_text()); record=next((s for s in recovery['shots'] if s['shotId']==shot['id']),None)
if record is None:
    record={'shotId':shot['id']}
    recovery['shots'].append(record)
record.update(displayId=shot['displayId'],editFrames=shot['frames'],localVideo=shot['videoSource'],sourceInFrame=start,resultUrls=[entry['resultUrl']],receiptFiles=['shots/tower-blackout-v070/batch.json']); f.write_text(json.dumps(recovery,indent=2)+'\n')
(output/'review.html').write_text('''<!doctype html><meta charset="utf-8"><title>Scene12 Shot7 — tower blackout</title><style>body{background:#15201c;color:#eee;font:18px system-ui;margin:28px}video{width:100%;max-width:1300px}a{color:#aadcce}</style><h1>Scene12 Shot7 — port control goes dark</h1><video controls src="S12-SH07.mp4"></video><p>Full source; animatic uses source1.0–2.458s,35frames.</p><a href="http://127.0.0.1:8767/">Full animatic</a>''')
with (output/'review.html').open('a') as f: f.write('<h2>Extended crash buildup</h2><video controls src="impact-preview.mp4"></video><p>Shake and fade toward white begin2.0s into S14-SH01.</p>')
print('Selected tower reaction; timing unchanged.')
