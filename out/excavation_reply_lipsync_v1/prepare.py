"""Prepare verified-clock lip sync for the owner-approved ironic performance."""
import hashlib,json,subprocess,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
source=ROOT/'out/excavation_reply_v1/base.mp4'
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
def run(a):subprocess.run([str(v) for v in a],check=True)
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
run(['ffmpeg','-v','error','-y','-i',source,'-map','0:v:0','-c:v','copy','-an',OUT/'base.mp4'])
run(['ffmpeg','-v','error','-y','-i',stem,'-af',f'atrim=start={2552/24-.178348}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-c:a','pcm_s16le',OUT/'guide.wav'])
with wave.open(str(OUT/'guide.wav')) as w:assert w.getnframes()==384000 and w.getframerate()==48000
lyrics=json.loads((ROOT/'shots/lyric_motion_full.json').read_text())
phrases=[{'text':p['text'],'song_frames':[p['on'],p['off']],
 'source_seconds':[(p['on']-2552)/24,(p['off']-2552)/24],
 'words':[{'text':v['text'],'source_seconds':[(v['on']-2552)/24,(v['off']-2552)/24]} for v in p['words']]}
 for p in lyrics['phrases'] if p['on'] in [2573,2620,2637]]
d={'schema_version':1,'test_id':'excavation_reply_lipsync_v1','project_root':str(ROOT),
 'status':'ready_for_claude_not_submitted','task':'ONE Kling Lip Sync on owner-approved excavation close-up. No Flow or acting revision.',
 'authorization':{'max_flow_submissions':0,'max_kling_submissions':1,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'kling':{'mode':'Lip Sync','character':'sole woman','guide_start_seconds':0,'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical cost only; check UI and stop above10. No purchases.'},
 'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':2552,'lead_stem_placement_offset_seconds':.178348,'raw_stem_extract_start_seconds':2552/24-.178348,'guide_already_aligned':True,'additional_audio_offset_seconds':0},
 'inputs':{'base':ref(OUT/'base.mp4'),'guide':ref(OUT/'guide.wav')},'source':ref(source),
 'guide_provenance':{'source':str(stem),'processing':'Uninterrupted8second mono48k PCM16 vocal slice. No gating, silence removal, normalization or time change. Context outside visible shot is not approved face coverage.'},
 'phrases':phrases,'cut':{'song_frames':[2564,2658],'source_frames_after_timestamp_conform':[12,106],'speed':1,'guard':'Preserve approved source clock. Especially begins0.875s, question2.833333s, finishes4.416667s. No picture shifts. Later Sometimes belongs to the other speaker; do not extend this shot into it.'},
 'output':{'synced':'out/excavation_reply_lipsync_v1/synced.mp4','receipt':'out/excavation_reply_lipsync_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'respect_rate_limits':True,'tool_time_counts':True},
 'inspection':'Owner accepts broader ironic wince/grin and transition to sincerity. Do not regenerate acting. Check especially every word through the grinning interval1.4..3.1s, plus question onset/end. Report missing articulation honestly; no automatic retry.',
 'assembly_guard':'Codex verifies returned audio alignment and native timestamps, conforms to24fps without slowdown, then auditions source12..106 after unchanged excavation. Never upload review movie, FX or master mix. No close-up shop changes or full-film merge.'}
(OUT/'handoff.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
print('Excavation reply lip-sync handoff ready.')
