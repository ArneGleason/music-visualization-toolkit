"""Build explicit two-take handoff and deterministic continuity crop."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
still=ROOT/'codex/out/counterfeit_parade_b.jpg'
lock=ROOT/'out/astronaut_reply_v1/style_lock_v2.txt'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(still),'-vf','crop=800:450:624:64,scale=1280:720:flags=lanczos','-frames:v','1',str(OUT/'close_reference.png')],check=True)
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
takes=[]
for name,start,end,first in [('wide',2399,2437,still),('close',2437,2484,OUT/'close_reference.png')]:
    prompt=OUT/f'{name}_prompt.txt'
    prompt.write_text((OUT/f'{name}_direction.txt').read_text(encoding='utf-8')+'\n\n'+lock.read_text(encoding='utf-8'),encoding='utf-8')
    takes.append({'id':name,'status':'ready_for_claude_not_submitted','first_frame':ref(first),'prompt':ref(prompt),
                  'song_frames':[start,end],'song_origin_frame':start-12,'source_frames_after_timestamp_conform':[12,12+end-start],
                  'lead_handle_frames':12,'requested_exit_handle_frames':192-12-(end-start),
                  'base':f'out/shop_performance_v1/{name}/base.mp4'})
manifest={'schema_version':1,'test_id':'shop_performance_v1','status':'ready_for_claude_not_submitted',
 'project_root':str(ROOT),'task':'Two Flow performance candidates only. NO Kling or other lip sync. Owner reviews base performances first.',
 'authorization':{'max_flow_submissions':2,'max_per_take':1,'max_kling_submissions':0,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'model':'Veo 3.1 Quality','mode':'Frames','aspect_ratio':'16:9','resolution':'720p','duration_seconds':8,'outputs_per_take':1,'expected_credits_per_take':100,'max_total_credits':200,'stop_if_settings_unavailable_or_price_exceeds_cap':True},
 'lock':ref(lock),'takes':takes,'clock':{'fps':24,'indexing':'zero-based end-exclusive','audio_upload':False,'generated_audio':'disposable, never assembly soundtrack'},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'tool_time_counts':True,'respect_rate_limits':True},
 'output':{'receipt':'out/shop_performance_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'assembly_guard':'Candidate timings only. Codex builds a short local push transition ending before2437, subject to continuity review. Do not generate the camera transition. No lip sync now. Native frame rates are conformed by timestamps later, never interpreted frame-for-frame. Preserve full originals, record actual gesture timing; do not silently move cut boundaries or claim rendered handles are reviewed usable handles.',
 'close_reference_provenance':{'source':ref(still),'crop_xywh':[624,64,800,450],'output_size':[1280,720],'method':'deterministic crop and Lanczos enlargement; no invented pixels or new generation','limitation':'enlarged reference, not proof of final close-up detail'},
 'next_phase':'Owner approves performance and transition first; Codex prepares a separate exact guide for any later lip sync.'}
(OUT/'handoff.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Handoff prepared.')
