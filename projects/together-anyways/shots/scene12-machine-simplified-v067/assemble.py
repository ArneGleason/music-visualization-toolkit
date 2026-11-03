"""Select the reviewed machine push-in; preserve every musical boundary."""
import json
import subprocess
from pathlib import Path
notes = Path(__file__).resolve().parent
project = notes.parents[1]
output = project / 'generated/kling-machine-v067'
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
story = 'The heavy tracked vehicle creeps forward as a low camera push makes its raised front attachment loom larger.'
shot.update(action=story, description=story, reviewOverlay=story, camera='Short low-angle push toward the vehicle, keeping the cab and front attachment readable.', acting='Operator watches the route; chassis rocks slightly and amber beacons rotate.', videoSource=str(video.relative_to(project)), status='motion_review', motionReview='shots/scene12-machine-simplified-v067/batch.json')
shot['videoEdit'] = {'sourceInFrame':start}
shot['motionDirection']={'prompt':entry['prompt'],'status':'generated_selected_for_review'}
shot['videoHandles'].update(status='generated', editInSourceFrame=start, editOutSourceFrameExclusive=end, availableHeadFrames=start, availableTailFrames=count-end, availableInFrames=start, availableOutFrames=count-end, sourceFrames=count, sourceStartMasterFrame=shot['startFrame']-start, sourceEndMasterFrameExclusive=shot['startFrame']-start+count, note='v067 machine push-in; full one-second handles retained.')
shot['motionReviewNote']=entry['reviewNote']
(project/'shots/shotlist.json').write_text(json.dumps(score,indent=2)+'\n')
entry.update(status='selected_for_review',media=media,localVideo=shot['videoSource'])
(notes/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
f=project/'shots/video-recovery.json'; recovery=json.loads(f.read_text()); record=next(s for s in recovery['shots'] if s['shotId']==shot['id']); record.update(localVideo=shot['videoSource'],sourceInFrame=start,resultUrls=[entry['resultUrl']],receiptFiles=['shots/scene12-machine-simplified-v067/batch.json']); f.write_text(json.dumps(recovery,indent=2)+'\n')
(output/'review.html').write_text('''<!doctype html><meta charset="utf-8"><title>Scene12 Shot7 — machine approach</title><style>body{background:#15201c;color:#eee;font:18px system-ui;margin:28px}video{width:100%;max-width:1300px}a{color:#aadcce}</style><h1>Scene12 Shot7 — machine approach</h1><video controls src="S12-SH07.mp4"></video><p>Full source; animatic uses source1.0–2.458s,35frames.</p><a href="http://127.0.0.1:8767/">Full animatic</a>''')
print('Selected machine push-in; timing unchanged.')
