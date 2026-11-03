"""Select reviewed flight replacements without changing musical timing."""
import json, subprocess
from pathlib import Path
notes=Path(__file__).resolve().parent; p=notes.parents[1]; output=p/'generated/ending-refinements-v068'
batch=json.loads((notes/'batch.json').read_text()); score=json.loads((p/'shots/shotlist.json').read_text()); recovery=json.loads((p/'shots/video-recovery.json').read_text())
for entry in batch['shots']:
 assert entry['status']=='reviewed'
 shot=next(s for s in score['shots'] if s['id']==entry['id']); video=output/(entry['id']+'.mp4')
 m=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,duration','-of','json',str(video)]))['streams'][0]
 assert m['r_frame_rate']=='24/1'; count=int(m['nb_frames']); start=entry['sourceInFrame']; end=start+shot['frames']; assert start>=24 and count-end>=24
 shot.update(videoSource=str(video.relative_to(p)),starterImage=entry['starter'],videoEdit={'sourceInFrame':start},status='motion_review',motionReview='shots/ending-refinements-v068/batch.json',motionReviewNote=entry['reviewNote'])
 if entry['id']=='S13-SH02':shot['starterRevision']='v068'
 shot['motionDirection']={'prompt':entry['prompt'],'status':'generated_selected_for_review'}
 shot['action']=('The ship lifts and accelerates out of the salvage recess, with ground dust, hull vibration and exhaust strain; all remaining parts stay attached.' if entry['id']=='S13-SH01' else 'The ship climbs above the settlement, briefly shuddering with an exhaust puff before continuing; all remaining parts stay attached.')
 shot['description']=shot['reviewOverlay']=shot['action']
 shot['videoHandles'].update(status='generated',editInSourceFrame=start,editOutSourceFrameExclusive=end,availableHeadFrames=start,availableTailFrames=count-end,availableInFrames=start,availableOutFrames=count-end,sourceFrames=count,sourceStartMasterFrame=shot['startFrame']-start,sourceEndMasterFrameExclusive=shot['startFrame']-start+count,note='v068 attached-hull retake, full24frame handles retained.')
 record=next(r for r in recovery['shots'] if r['shotId']==shot['id']);record.update(localVideo=shot['videoSource'],sourceInFrame=start,resultUrls=[entry['resultUrl']],receiptFiles=['shots/ending-refinements-v068/batch.json'])
 entry.update(status='selected_for_review',localVideo=shot['videoSource'],media=m)
(p/'shots/shotlist.json').write_text(json.dumps(score,indent=2)+'\n');(p/'shots/video-recovery.json').write_text(json.dumps(recovery,indent=2)+'\n');(notes/'batch.json').write_text(json.dumps(batch,indent=2)+'\n')
f=output/'review.html';html=f.read_text()
for entry in batch['shots']:html+=f'<section><h2>{entry["id"]} — revised flight</h2><video controls src="{entry["id"]}.mp4"></video><p>{entry["reviewNote"]}</p></section>'
f.write_text(html)
print('Selected both flight retakes.')
