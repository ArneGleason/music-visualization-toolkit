"""Isolated frame-exact native review selection. Does not promote production."""
from pathlib import Path
import json,copy
O=Path(__file__).resolve().parent
edl=json.loads((O/'meaning_shotlist.json').read_text());register=json.loads((O/'migration_register.json').read_text());by_id={s['id']:s for s in edl['shots']}
outro={55:('tv',12),56:('afterglow_b1',67),57:('tv',97),58:('afterglow_b2',11),59:('tv_late',0),60:('room_late',0),61:('tv_late',38),62:('room_late',31),63:('tv_late',56),64:('close_cloud',0),65:('close_cloud',36),66:('return_cloud',0),67:('tv_late',78),68:('return_cloud',49),69:('night',0),70:('titles',0)}
shots=[]
for record in register['shots']:
 ident=record['id'];number=record['review_number'];a,z=record['song_frames']
 shot=copy.deepcopy(by_id.get(ident,{'id':ident,'section':'low-light-outro','type':'performance','setup':ident,'lyric':'','prompt':'','transition':{'type':'cut','dur_sec':0}}))
 shot.update(start_sec=a/24,end_sec=z/24,dur_sec=(z-a)/24,frames=z-a)
 if number in outro:
  family,offset=outro[number];shot['clip']={'file':f'out/blender_migration_v1/{family}/native_clean.mp4','in_sec':offset/24,'speed':1}
 if number==2:shot['clip']={'file':'out/blender_migration_v1/scope/native_clean.mp4','in_sec':0,'speed':1}
 if number==29:shot['clip']={'file':'out/blender_migration_v1/shop_full/native_clean.mp4','in_sec':0,'speed':1}
 shots.append(shot)
edl['shots']=shots;edl['duration_sec']=4854/24;edl['migration_status']='draft_requires_dependency_preflight';(O/'full_native_review_draft.json').write_text(json.dumps(edl,indent=2))
decisions=json.loads((O/'batch3_decisions.json').read_text())
decisions['s002']={'id':'native-scope-review','shot_id':'s002','setup':by_id['s002']['setup'],'decision':'prefer_music_fx_composite_over_untreated_video','approval':'owner_approved_treatment','delivery_status':'delivery_ready','delivery_file':'out/blender_migration_v1/scope/native_clean.mp4','timing_snapshot':{'fps':24,'song_start_frame':86,'song_end_frame_exclusive':155,'source_in_frame':0,'source_out_frame_exclusive':69}}
(O/'full_native_decisions.json').write_text(json.dumps(decisions,indent=2))
cues=json.loads((O.parents[1]/'out/swirl_tail_review_v1/overlay_cues.json').read_text())
cues.update(frames=4854,duration_sec=4854/24)
cues['shots']=[{'id':s['id'],'setup':s['setup'],'section':s['section'],'start':round(s['start_sec']*24),'end':round(s['end_sec']*24),'lyric':s.get('lyric','')} for s in shots]
(O/'full_native_cues.json').write_text(json.dumps(cues,indent=2))
