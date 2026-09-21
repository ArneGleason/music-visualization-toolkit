from pathlib import Path
import json,subprocess
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913')
preview='animatic/MonstersLoose-v92-outro-performances.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(r/preview)]))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
assert int(video['nb_frames'])==5290 and video['r_frame_rate']=='24/1'
assert any(s['codec_type']=='audio' for s in probe['streams'])
selections=json.loads((r/'motion-graphics/OUTRO-001/selections.json').read_text())['selections']
plan=json.loads((r/'shots/SCN-014-015-production-plan.json').read_text())
credits=0
for take in plan['shots']:
 p=r/'video-tests'/('KLING-SCENE14-'+take['name']+'-001')/'submission.json'
 data=json.loads(p.read_text());assert data['ok'];credits+=data['body']['creditsConsumed']
p=r/'shots/shotlist.json';d=json.loads(p.read_text())
for s in d['shots']:
 for take in selections:
  if s['id']==take['id']:
   s.update(take,media_type='video',status='generated_for_review',effects_record='motion-graphics/OUTRO-001/selections.json')
   s['starting_image']=next(x['starting_image'] for x in plan['shots'] if x['id']==s['id'])
d['scope']='Full song through frame5290; generated footage assembled throughout, earlier deferred polish retained.'
d['current_preview']=preview;d['ending_planning'].update(preview=preview,status='complete_outro_generated_for_review',credits_consumed=80+credits,outro_credits_consumed=credits)
d['next_scene_planning']['preview']=preview
p.write_text(json.dumps(d,indent=2)+'\n')
(r/'motion-graphics/OUTRO-001/validation.json').write_text(json.dumps(dict(master_frames=5290,fps=24,audio_present=True,unchanged_through_frame=4413,outro_start=4414,finale_start=4951,outro_new_credits=credits,all_nine_selected_clips_exact_length=True),indent=2)+'\n')
p=Path('projects/monsters-loose/README.md');s=p.read_text(encoding='utf-8').replace('Current preview: **v91**','Current preview: **v92**').replace('recovery/animatic/MonstersLoose-v91-swamp-meeting.blend','recovery/animatic/MonstersLoose-v92-outro-performances.blend').replace('Open the current v91 Blender','Open the current v92 Blender')
p.write_text('Latest v92: nine generated reprise/outro performances4414..5290; full song fleshed out. Human/monster gesture pairs, researchers, playful creatures, inspector, Harper/kid, continuous swamp finale4951..5290.408new Kling credits. Default12frame lead-in; precise selected source frames recorded in OUTRO-001/selections.json. Review from4398. Earlier approved footage retained.\n\n'+s,encoding='utf-8')
Path('projects/monsters-loose/HANDOFF.md').write_text('# Current working state\n\nCurrent preview v92, MonstersLoose-v92-outro-performances.mp4 and .blend. All song coverage through5290 is now generated; latest nine shots4414..5290 await user review. Swamp meeting4242..4413 approved. Outro generation408credits, with twelve-frame lead-ins and source selections in motion-graphics/OUTRO-001/selections.json. Final continuous swamp shot4951..5290 uses15second take with12frame lead-in and8frame minimum tail. No forced end image. Earlier kid eye-roll and cutesy Harper YES WAY remain deferred.\n\nReproduction: video-tests/prepare-outro.py records plan and request prompts (do not rerun to resubmit); native starting-frame prompts are shots/SCN-014-*-prompt.txt and SCN-015-FINALE-v001-prompt.txt. motion-graphics/outro-select.py selects takes; animatic/build-opening-v92.py assembles Blender. Do not regenerate or pay for retries without a reason from review. Master audio and all frames through4413 unchanged. Review at4398, final tableau at4951.\n')
p=r/'animatic/frame-review-current.json';t=p.with_suffix('.tmp');t.write_text(json.dumps(dict(video=str(r/preview),master_start=1)));t.replace(p)
print('Published v92:',credits,'new credits;5290frames')
