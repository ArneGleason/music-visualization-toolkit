import json,subprocess
from pathlib import Path
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');preview='animatic/MonstersUndone-v94.mp4'
tagged=r/'animatic/MonstersUndone-v94-tagged.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(r/preview),'-map','0','-c','copy','-metadata','title=Monsters Undone','-metadata','artist=Arne Gleason','-metadata','copyright=© 2026 Arne Gleason','-movflags','+faststart',str(tagged)],check=True)
tagged.replace(r/preview)
data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(r/preview)]))
v=next(s for s in data['streams'] if s['codec_type']=='video');assert int(v['nb_frames'])==5290 and v['r_frame_rate']=='24/1'
assert any(s['codec_type']=='audio' for s in data['streams'])
hashes=[]
for source in ['animatic/MonstersLoose-v93-swamp-cousin-beacons.mp4',preview]:
 hashes.append(subprocess.check_output(['ffmpeg','-v','error','-i',str(r/source),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).decode().strip())
assert hashes[0]==hashes[1]
changes={'SCN-014-BEYOND-FENCE':'motion-graphics/OUTRO-LIGHTS-002/SCN-014-BEYOND-FENCE-beacons-v002.mp4','SCN-014-CEO':'motion-graphics/OUTRO-001/CEO-timed-v001.mp4','SCN-014-INSPECTOR':'motion-graphics/OUTRO-001/INSPECTOR-timed-v001.mp4','SCN-015-FINALE':'motion-graphics/OUTRO-LIGHTS-002/SCN-015-FINALE-beacons-v002.mp4'}
p=r/'shots/shotlist.json';d=json.loads(p.read_text())
for s in d['shots']:
 if s['id'] not in changes:continue
 s['previous_v93_source']=s['source'];s['source']=changes[s['id']];s['source_in_frame']=0
 if s['id'] in ['SCN-014-CEO','SCN-014-INSPECTOR']:
  s['effects_status']='added_beacons_removed_user_requested';s.pop('beacon_record',None)
 else:s['effects_status']='tightened_beacons_for_review';s['beacon_refinement_record']='motion-graphics/OUTRO-LIGHTS-002/settings.json'
d['title']='Monsters Undone';d['working_title']='Monsters Loose';d['current_preview']=preview;d['ending_planning']['preview']=preview;d['next_scene_planning']['preview']=preview
d['end_credit']=dict(title='MONSTERS UNDONE',credit='© 2026 Arne Gleason',start_frame=5279,end_frame_exclusive=5291,duration_frames=12,position='bottom center',font='Georgia Bold title; Georgia credit')
p.write_text(json.dumps(d,indent=2)+'\n')
(r/'motion-graphics/OUTRO-LIGHTS-002/validation.json').write_text(json.dumps(dict(frame_count=5290,fps=24,audio_unchanged=True,width=v['width'],height=v['height'],credit_frames=12,credit_master_start=5279,additional_generation_credits=0),indent=2)+'\n')
p=Path('projects/monsters-loose/README.md');s=p.read_text(encoding='utf-8').replace('Current preview: **v93**','Current preview: **v94**').replace('recovery/animatic/MonstersLoose-v93-swamp-cousin-beacons.blend','recovery/animatic/MonstersUndone-v94.blend').replace('Open the current v93 Blender','Open the current v94 Blender');p.write_text('Latest v94: renamed display title Monsters Undone. Standalone MP4 with bottom lyrics, no scene markers. Final12frames5279..5290 show MONSTERS UNDONE / ©2026 Arne Gleason. Final beacon radius one-third and subdued intensity; swamp-entry radius75percent. CEO4414 and inspector4719 use original lights. No new generation credits.\n\n'+s,encoding='utf-8')
Path('projects/monsters-loose/HANDOFF.md').write_text('# Monsters Undone — current state\n\nCurrent standalone render: animatic/MonstersUndone-v94.mp4 and matching.blend,5290frames at24fps,1280x720,original song audio unchanged. Former working/project name Monsters Loose retained in paths. Top scene/planning markers removed; lyrics and countdown retained. Final12frames5279..5290 carry title MONSTERS UNDONE and ©2026 Arne Gleason, centered at bottom.\n\nLight refinement: final lamps use one-third previous radius with subdued intensity; swamp entry4242 uses75percent radius. Original baked bloom suppressed before smaller light reconstruction, preserving roof texture. CEO4414 and inspector4719 restored to original unmodified lights. Other effects retained. Reproduce effects with motion-graphics/refine-outro-lights.py and assembly animatic/build-opening-v94.py. No new generation credits this revision.\n\nFinale take003 retains resting boss, mossy cousin and stronger crane. User is reviewing polish. Earlier kid eye-roll and cutesy Harper dialogue shot remain deferred. Large media external to Git.\n',encoding='utf-8')
p=r/'animatic/frame-review-current.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(dict(video=str(r/preview),master_start=1)));tmp.replace(p)
print('v94 published:5290frames; audio identical; final12frame credit')
