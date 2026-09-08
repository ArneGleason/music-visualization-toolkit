"""Package the reviewed discovery starting image for one Flow generation."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
lock=ROOT/'out/astronaut_reply_v1/style_lock_v2.txt'
prompt=(OUT/'direction.txt').read_text(encoding='utf-8')+'\n\n'+lock.read_text(encoding='utf-8')
(OUT/'flow_prompt.txt').write_text(prompt,encoding='utf-8')
d={'schema_version':1,'test_id':'archaeology_discovery_v1','project_root':str(ROOT),
 'status':'ready_for_claude_not_submitted',
 'task':'ONE careful archaeological discovery take; familiar clear amber spiral specimen stays embedded. NO Kling.',
 'authorization':{'max_flow_submissions':1,'max_kling_submissions':0,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'model':'Veo 3.1 Quality','mode':'Frames','aspect_ratio':'16:9','resolution':'720p','duration_seconds':8,'outputs':1,'expected_credits':100,'stop_if_unavailable_or_cost_exceeds_expected':True},
 'inputs':{'first_frame':ref(OUT/'first_frame.png'),'prompt':ref(OUT/'flow_prompt.txt'),'lock':ref(lock)},
 'continuity_reference':ref(ROOT/'codex/out/astronaut_inspect_medium_a.jpg'),
 'reference_note':'New starting frame created with built-in image model from accepted specimen and excavation setting references; intended matching prop, not a claim of pixel-identical reconstruction. Do not use old conical excavation prop.',
 'clock':{'fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':2472,'requested_source_frames':192,'no_audio_upload':True},
 'proposed_cut':{'setup':'excavation_site','song_frames':[2484,2564],'source_frames_after_timestamp_conform':[12,92],'duration_frames':80,'lead_handle_frames':12,'requested_exit_handle_frames':100,'status':'candidate only'},
 'output':{'base':'out/archaeology_discovery_v1/base.mp4','receipt':'out/archaeology_discovery_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'respect_rate_limits':True,'tool_time_counts':True},
 'assembly_guard':'No production replacement until review. Existing specimen-handling and shop keepers remain unchanged. Never retime or loop returned action to hide incorrect choreography. Musical amber activation is deferred to Codex after picture review.'}
(OUT/'handoff.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print('Discovery handoff ready.')
