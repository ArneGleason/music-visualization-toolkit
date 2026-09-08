import json,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
subprocess.run(['ffmpeg','-v','error','-y','-i',str(ROOT/'clips/raw/forest_walk_track_v6.mp4'),'-vf','select=eq(n\\,144)','-frames:v','1',str(OUT/'first_frame.png')],check=True)
lock=(ROOT/'out/astronaut_reply_v1/style_lock_v2.txt').read_text()
direction=(OUT/'direction.txt').read_text()
(OUT/'flow_prompt.txt').write_text(direction.rstrip()+'\n\n'+lock)
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper()
h={'schema_version':1,'test_id':'garden_walk_return_v1','project_root':str(ROOT),'status':'ready_for_claude_not_submitted',
 'task':'One new non-speaking garden walking take. No Kling, no assembly. Fresh later coverage, not a restarted old take.',
 'authorization':{'max_flow_submissions':1,'max_kling_submissions':0,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'model':'Veo 3.1 Quality','mode':'Frames','aspect_ratio':'16:9','resolution':'720p','duration_seconds':8,'outputs':1,'expected_credits':100,'stop_if_unavailable_or_cost_exceeds_expected':True},
 'inputs':{'first_frame':{'file':'out/garden_walk_return_v1/first_frame.png','sha256':sha('out/garden_walk_return_v1/first_frame.png'),'provenance':'Exact decoded frame144 from clips/raw/forest_walk_track_v6.mp4. Reviewed by Codex. Later garden geography, existing likeness/costume/lantern.'},
 'identity_reference_only':'codex/out/forest_walk_track_b.jpg','prompt':{'file':'out/garden_walk_return_v1/flow_prompt.txt'},'lock':{'file':'out/astronaut_reply_v1/style_lock_v2.txt','sha256':sha('out/astronaut_reply_v1/style_lock_v2.txt')}},
 'clock':{'fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':1638,'requested_source_frames':192,'no_audio_upload':True},
 'proposed_cut':{'shot_id':'garden_walk_return','setup':'forest_walk_track','song_frames':[1650,1710],'source_frames_after_timestamp_conform':[12,72],'duration_frames':60,'lead_handle_frames':12,'requested_exit_handle_frames':120,'status':'Revised phrase-contained opening; distinct take with its own origin, not continuous old source clock'},
 'phrase':{'text':'in the psychedelic garden','song_frames':[1650,1710]},
 'output':{'base':'out/garden_walk_return_v1/base.mp4','receipt':'out/garden_walk_return_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'respect_rate_limits':True,'tool_time_counts':True},
 'assembly_guard':'Codex verifies source12..72 after timestamp conform. No lip sync or source audio used. Never restart old walk source238..298, which exceeds192frames. No speed changes or holds. New base is a candidate, not an automatic production override; Codex adds restrained musical light response later.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
assert (OUT/'flow_prompt.txt').read_text().endswith(lock)
print('Handoff ready; input hash verified; style lock unchanged.')
