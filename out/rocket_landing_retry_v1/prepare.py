"""One controlled-landing replacement with aligned speaker guide."""
import hashlib,json,subprocess,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
lock=(ROOT/'out/astronaut_reply_v1/style_lock_v2.txt').read_bytes()
(OUT/'style_lock_v2.txt').write_bytes(lock)
(OUT/'flow_prompt.txt').write_bytes((OUT/'direction.txt').read_bytes()+b'\n\n'+lock)
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
subprocess.run(['ffmpeg','-v','error','-y','-i',str(stem),'-af',f'atrim=start={2916/24-.178348}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'guide.wav')],check=True)
with wave.open(str(OUT/'guide.wav')) as w:assert w.getnframes()==384000
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
h={'schema_version':1,'test_id':'rocket_landing_retry_v1','project_root':str(ROOT),'status':'ready_for_claude_not_submitted',
 'task':'One NEW Flow controlled landing with helmeted singing performer, then one Kling pass only if base passes the gate. Orbital descent is accepted and MUST NOT be regenerated.',
 'authorization':{'max_flow_submissions':1,'max_kling_submissions':1,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'flow':{'model':'Veo 3.1 Quality','mode':'Frames','aspect_ratio':'16:9','resolution':'720p','duration_seconds':8,'outputs':1,'expected_credits':100},'kling':{'mode':'Lip Sync','character':'sole real woman inside the clear helmet','guide_start_seconds':0,'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical estimates only. Verify actual UI, no purchases.'},
 'inputs':{'first_frame':ref(ROOT/'codex/out/rockets_landing_wide_a.jpg'),'prompt':ref(OUT/'flow_prompt.txt'),'lock':ref(OUT/'style_lock_v2.txt'),'guide':ref(OUT/'guide.wav')},
 'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':2916,'song_origin_seconds':121.5,'lead_stem_placement_offset_seconds':.178348,'raw_stem_extract_start_seconds':121.5-.178348,'guide_already_aligned':True,'additional_audio_offset_seconds':0},
 'cut':{'current_audition_song_frames':[2928,3027],'current_source_frames':[12,111],'primary_phrase_song_frames':[2928,2993],'primary_phrase_source_frames':[12,77],'lead_handle_frames':12,'requested_exit_handle_frames_after_audition':81,'speed':1},
 'coverage_guard':'Eight seconds from origin2916 ends3108, NOT3165. This tests the first landing interval and primary line only. It does not cover the entire old landing run or complete the later phrase ending3113. Do not loop, freeze, stretch, restart landing, compress later lyrics, or claim full later coverage. Subsequent cut/coverage will be planned after owner review.',
 'quality_gate_before_kling':['Inspect entire base before lip-sync spend.','Monotonic descent, engines shorten/dim and shut OFF at touchdown, no re-ignition.','Low outward dust, no mushroom-like rising cloud or explosion.','All three rockets stable and intact after landing.','Plain silver chest and clear helmet preserved; no new hardware.','Active natural singing through source0.5..3.208, face readable through visor.','If a material failure occurs, save base/receipt and stop for owner review. No automatic retry or Kling on a failed base.'],
 'output':{'base':'out/rocket_landing_retry_v1/base.mp4','synced':'out/rocket_landing_retry_v1/synced.mp4','receipt':'out/rocket_landing_retry_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'tool_time_counts':True,'respect_rate_limits':True},
 'assembly_guard':'Codex verifies source/guide clocks and timestamp conforms as needed. Existing orbital shot2881..2928 untouched. Reapply accepted local pressure-lens FX after sync, using new plate masks and existing song timing, not old baked picture. Master and lyrics once. No global flash or mastering.',
 'completion':'Save untouched originals and byte-identical base/synced. Receipt records hashes, settings, credits, IDs, dimensions, native fps/frame count/durations, touchdown and engine-cutoff times for each rocket, dust development, costume and mouth defects. Add claude_result and status=claude_done_ready_for_codex_verification, or explicit blocked quality-gate status. No assembly, commit or approval claims.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2))
print('Landing replacement handoff ready. No submissions.')
