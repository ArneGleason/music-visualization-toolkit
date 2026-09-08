"""Create a fresh Flow-only geyser handoff with exact editorial clock."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
shutil.copy2(ROOT/'out/astronaut_reply_v1/style_lock_v2.txt',OUT/'style_lock_v2.txt')
lock=(OUT/'style_lock_v2.txt').read_bytes()
(OUT/'flow_prompt.txt').write_bytes((OUT/'direction.txt').read_bytes().rstrip()+b'\n\n'+lock)
assert (OUT/'flow_prompt.txt').read_bytes().endswith(lock)
def asset(name):
    p=OUT/name;return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
m={
 'schema_version':1,'test_id':'spring_geyser_flow_v1','project_root':str(ROOT),'status':'ready_for_claude_not_submitted',
 'task':'One Flow-only geyser surge/pressure-decay/falling-spray take for Whatever falls from heaven. No Kling.',
 'authorization':{'max_flow_submissions':1,'max_kling_submissions':0,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'flow':{'model':'Veo 3.1 Quality','mode':'Frames','aspect_ratio':'16:9','resolution':'720p','duration_seconds':8,'outputs':1,'expected_credits':100},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical setting/cost. Verify current UI. No purchase or silent model change.'},
 'inputs':{'first_frame':asset('first_frame.png'),'prompt':asset('flow_prompt.txt'),'lock':asset('style_lock_v2.txt')},
 'input_guard':'Use this first_frame.png as sole START frame. No END frame, no audio input. Do not use the old arched-hose still from springs_splash_review_v1. Prompt verbatim including lock.',
 'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':3752,'song_origin_seconds':3752/24,'additional_audio_offset_seconds':0,'note':'Editorial source clock, no lip sync. Mid-eruption at source0, not eruption starting from a calm pool.'},
 'cut':{'shot_id':'spring_falls_heaven','song_frames':[3752,3830],'source_frames_at_24fps':[0,78],'duration_seconds':3.25,'lead_handle_frames':0,'exit_handle_frames_if_192_delivered':114,'speed':1},
 'lyric_targets':[{'word':'Whatever','song_frame':3752,'source_seconds':0},{'word':'falls','song_frame':3761,'source_seconds':9/24},{'word':'from','song_frame':3791,'source_seconds':39/24},{'word':'heaven','song_frame':3807,'source_seconds':55/24}],
 'timing_guard':'Targets guide the action, not guaranteed frame-accurate generated events. Do not retime/trim to force a match. Report actual pressure-decay and splash times for Codex review. Useful fall/splash must be in first3.25s, not only at8s.',
 'quality_gate':['Confirm tall vertical water exits top of frame, not small arched hose. Keep low framing and visible ground vent.','Inspect source0,0.5,1,2,3.25s and tail: pressure drops but previously airborne spray continues to fall and splash.','Liquid detail, stable geography, no smoke/explosion, no disappearing water or rigid water arch.','Save result even if imperfect; minor timing deviations are review notes, not authorization to retry. Report gross failures separately.'],
 'output':{'base':'out/spring_geyser_flow_v1/base.mp4','receipt':'out/spring_geyser_flow_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'tool_time_counts':True,'respect_rate_limits':True},
 'assembly_guard':'Codex handles conforming, editorial review and audio. Provisional preview snapshot out/springs_splash_review_v1/shotlist.json: replace only static spring3752..3830. Keep underwater footage on3830..3897 and preserve all prior accepted FX including Bends your mind and opening aerial. Do not change assembly, lyrics, master, registers or prior media.',
 'completion':'Download original untouched and save byte-identical base.mp4. Write RECEIPT.md with media ID, actual settings/credits, paths, SHA256, native fps/frame count/dimensions/duration, progress and visual QA including action timings. Add claude_result and flip status to claude_done_ready_for_codex_verification, or explicit blocked status. No retry, commit, purchase or owner-acceptance claim.'
}
(OUT/'handoff.json').write_text(json.dumps(m,indent=2))
print('Ready for Claude, not submitted.')
