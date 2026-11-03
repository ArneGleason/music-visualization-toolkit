"""Select the reviewed tower cutaway; preserve every musical boundary."""
import json
import subprocess
from pathlib import Path
notes = Path(__file__).resolve().parent
project = notes.parents[1]
output = project / 'generated/ascent-wipe-v071'
batch = json.loads((notes / 'batch.json').read_text())
entry = batch['shots'][0]
assert entry['status'] == 'reviewed'
video = output / 'S13-SH03.mp4'
media = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,duration','-of','json',str(video)]))['streams'][0]
assert media['r_frame_rate'] == '24/1'
score = json.loads((project / 'shots/shotlist.json').read_text())
shot = next(s for s in score['shots'] if s['id'] == 'S13-SH03')
start = entry['sourceInFrame']; count = int(media['nb_frames']); end = start + shot['frames']
assert start >= 24 and count-end >= 24
story = 'The small corrected ship flies steadily above the vast desert landscape; scenery remains dominant.'
shot.update(description=story, action=story, reviewOverlay=story, camera='Gentle wide aerial follow, no push toward the ship.', videoSource=str(video.relative_to(project)),starterImage=entry['starter'],starterRevision='v071',status='motion_review',motionReview='shots/ascent-wipe-v071/batch.json')
shot['videoEdit'] = {'sourceInFrame':start}
shot['starterCandidate']['status']='selected'
shot['motionDirection']={'prompt':entry['prompt'],'status':'generated_selected_for_review'}
shot['videoHandles'].update(status='generated', editInSourceFrame=start, editOutSourceFrameExclusive=end, availableHeadFrames=start, availableTailFrames=count-end, availableInFrames=start, availableOutFrames=count-end, sourceFrames=count, sourceStartMasterFrame=shot['startFrame']-start, sourceEndMasterFrameExclusive=shot['startFrame']-start+count, note='v071 wide flight; full one-second handles retained.')
shot['motionReviewNote']=entry['reviewNote']
(project/'shots/shotlist.json').write_text(json.dumps(score,indent=2)+'\n')
entry.update(status='selected_for_review',media=media,localVideo=shot['videoSource'])
(notes/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
f=project/'shots/video-recovery.json'; recovery=json.loads(f.read_text()); record=next(s for s in recovery['shots'] if s['shotId']==shot['id']); record.update(localVideo=shot['videoSource'],sourceInFrame=start,resultUrls=[entry['resultUrl']],receiptFiles=['shots/ascent-wipe-v071/batch.json']); f.write_text(json.dumps(recovery,indent=2)+'\n')
f=output/'review.html';html=f.read_text().replace('Existing motion not regenerated yet.','Replacement motion generated and selected.');html+='<h2>S13-SH03 — corrected wide flight</h2><video controls src="S13-SH03.mp4"></video><p>Animatic uses source1.0–4.583s,86frames.</p>';f.write_text(html)
print('Selected corrected wide flight.')
