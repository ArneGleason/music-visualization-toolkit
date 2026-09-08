"""Prepare one wide-only lip-sync job with the original source clock."""
import hashlib,json,subprocess,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
source=ROOT/'out/shop_performance_v1/wide/base.mp4'
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
def run(a):subprocess.run([str(v) for v in a],check=True)
run(['ffmpeg','-v','error','-y','-i',source,'-map','0:v:0','-c:v','copy','-an',OUT/'base.mp4'])
run(['ffmpeg','-v','error','-y','-i',stem,'-af',f'atrim=start={2387/24-.178348}:duration=8,asetpts=PTS-STARTPTS',
 '-ac','1','-ar','48000','-c:a','pcm_s16le',OUT/'guide.wav'])
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
with wave.open(str(OUT/'guide.wav')) as w:assert w.getnframes()==384000 and w.getframerate()==48000
lyrics=json.loads((ROOT/'shots/lyric_motion_full.json').read_text())
phrases=[]
for p in lyrics['phrases']:
 if p['on'] in [2399,2411]:
  phrases.append({'text':p['text'],'song_frames':[p['on'],p['off']],
    'source_seconds':[(p['on']-2387)/24,(p['off']-2387)/24]})
d={'schema_version':1,'test_id':'shop_wide_lipsync_v1','project_root':str(ROOT),
 'status':'ready_for_claude_not_submitted','task':'ONE Kling Lip Sync on WIDE shop performance only. Never touch the approved close-up. NO Flow.',
 'authorization':{'max_flow_submissions':0,'max_kling_submissions':1,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'kling':{'mode':'Lip Sync','character':'sole real woman, NOT reflection or alien souvenir','guide_start_seconds':0,'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical expectation, verify actual UI; no purchases.'},
 'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':2387,
 'lead_stem_placement_offset_seconds':.178348,'raw_stem_extract_start_seconds':2387/24-.178348,
 'guide_already_aligned':True,'additional_audio_offset_seconds':0},
 'inputs':{'base':ref(OUT/'base.mp4'),'guide':ref(OUT/'guide.wav')},
 'source':ref(source),'guide_provenance':{'source':str(stem),'processing':'Uninterrupted8second mono48k PCM16 slice, no normalization, gating, silence removal or time change; context outside wide usage is not approved face coverage.'},
 'phrases':phrases,'cut':{'wide_song_frames':[2399,2431],'wide_source_frames':[12,44],
 'target_phrase_song_frames':[2399,2437],'target_phrase_source_frames':[12,50],
 'source_switch_frame':2431,'close_source_origin_frame':2425,
 'guard':'Last6frames of better are on existing close source6..12 during transition. Preserve current approved edit. Do not move cut or retime either take. Close NEVER sent to Kling.'},
 'output':{'synced':'out/shop_wide_lipsync_v1/synced.mp4','receipt':'out/shop_wide_lipsync_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'respect_rate_limits':True,'tool_time_counts':True},
 'assembly_guard':'Codex verifies return and reapplies approved shop_push_signal_v4 alien-head FX and snap transition. Never upload FX composite. No close-up changes. Extra returned guide words do not authorize extending wide coverage.',
 'inspection':'Inspect source0.5..2.083333 for No and Dont make it better; avoid affecting reflection, souvenir or facial identity. Quiet reaction base may yield weak mouth articulation: report honestly, no automatic retry.'}
(OUT/'handoff.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print('Wide-only lip-sync handoff ready.')
