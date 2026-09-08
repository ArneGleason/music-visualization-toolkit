"""Package one matching reaction performance, before any lip-sync submission."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
lock=ROOT/'out/astronaut_reply_v1/style_lock_v2.txt'
(OUT/'flow_prompt.txt').write_text((OUT/'direction.txt').read_text(encoding='utf-8')+'\n\n'+lock.read_text(encoding='utf-8'),encoding='utf-8')
d={'schema_version':1,'test_id':'excavation_reply_v1','project_root':str(ROOT),'status':'ready_for_claude_not_submitted',
 'task':'ONE matching kneeling close-up: quoted ironic judgment becomes sincere question. Performance review BEFORE lip sync.',
 'authorization':{'max_flow_submissions':1,'max_kling_submissions':0,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'model':'Veo 3.1 Quality','mode':'Frames','aspect_ratio':'16:9','resolution':'720p','duration_seconds':8,'outputs':1,'expected_credits':100,'stop_if_unavailable_or_cost_exceeds_expected':True},
 'inputs':{'first_frame':ref(OUT/'first_frame.png'),'prompt':ref(OUT/'flow_prompt.txt'),'lock':ref(lock)},
 'clock':{'fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':2552,'requested_source_frames':192,'no_audio_upload':True},
 'proposed_cut':{'song_frames':[2564,2658],'source_frames_after_timestamp_conform':[12,106],'lead_handle_frames':12,'requested_exit_handle_frames':86,'status':'candidate, not production merge','bridge':'nine frames2564..2573 allow eye-lift before Especially; previous excavation remains2484..2564'},
 'phrases':[{'text':'Especially stupid.','song_frames':[2573,2620],'source_frames':[21,68]},
 {'text':'Can you hear','song_frames':[2620,2637],'source_frames':[68,85]},
 {'text':'what I meant?','song_frames':[2637,2658],'source_frames':[85,106]}],
 'acting_subtext':'She quotes an old judgment against her interests, then asks sincerely to be understood. Not insulting self or fossil. Background duh is not an extra sung line; precise timing unverified.',
 'output':{'base':'out/excavation_reply_v1/base.mp4','receipt':'out/excavation_reply_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'respect_rate_limits':True,'tool_time_counts':True},
 'assembly_guard':'No lip-sync service until performance review. No modification of accepted shop or prior specimen footage. Preserve full phrase timing; no silent loops, freezes or stretching. Next Sometimes starts2658 and is another speaker.'}
(OUT/'handoff.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print('Reaction handoff ready.')
