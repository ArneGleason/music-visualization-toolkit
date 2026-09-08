"""One owner-requested speaker reassignment audition, without timing changes."""
import hashlib,json,subprocess,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
source=ROOT/'out/meaning_exchange_handoff_v1/astronomer/base.mp4'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='9e2931728f3357b2d7ab07d8488cc93bd7cf4d966537b6abb6c142e5ae20e72e'
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-map','0:v:0','-c:v','copy','-an',str(OUT/'base.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(stem),'-af',f'atrim=start={2774/24-.178348}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'guide.wav')],check=True)
with wave.open(str(OUT/'guide.wav')) as w:assert w.getnframes()==384000
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
h={'schema_version':1,'test_id':'meaning_astronomer_lipsync_v1','project_root':str(ROOT),'status':'ready_for_claude_not_submitted',
 'task':'ONE Kling Lip Sync on the fresh astronomer push-in. No Flow. Owner explicitly wants to audition the astronomer singing Words leave words.',
 'authorization':{'max_flow_submissions':0,'max_kling_submissions':1,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'kling':{'mode':'Lip Sync','character':'the real woman, never the empty spacesuit on its stand','guide_start_seconds':0,'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical estimate, verify actual UI. No purchases.'},
 'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':2774,'song_origin_seconds':2774/24,'lead_stem_placement_offset_seconds':.178348,'raw_stem_extract_start_seconds':2774/24-.178348,'guide_already_aligned':True,'additional_audio_offset_seconds':0},
 'inputs':{'base':ref(OUT/'base.mp4'),'guide':ref(OUT/'guide.wav')},'original_source':ref(source),
 'guide_provenance':{'source':str(stem),'processing':'Continuous8second mono48k PCM16 slice with real context. No normalization, gating, silence removal, stretching or added offsets. Context is not permission to make the listener sing earlier lines in assembly.'},
 'phrase':{'text':'Words leave words.','song_frames':[2812,2881],'source_frames_at_24fps':[38,107],'source_seconds':[38/24,107/24]},
 'cut':{'whole_plate_song_frames':[2786,2881],'whole_plate_source_frames':[12,107],'keep_original_listening_song_frames':[2786,2812],'keep_original_listening_source_frames':[12,38],'replace_synced_song_frames':[2812,2881],'replace_synced_source_frames':[38,107],'panel_push_song_frames':[2786,2826]},
 'speaker_override':'Owner-authorized editorial audition: astronomer sings Words leave words even though current lyric metadata says Them2. Do not silently move or reassign Sometimes, Not always, or Meaning leaves thread. Codex reviews and reconciles metadata on adoption.',
 'output':{'synced':'out/meaning_astronomer_lipsync_v1/synced.mp4','receipt':'out/meaning_astronomer_lipsync_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'tool_time_counts':True,'respect_rate_limits':True},
 'quality_notes':'Existing plate was generated as listening, so a clamped or puppet-like mouth is a known risk. Report articulation of all three words, especially start/end, face integrity, gaze/hand/camera preservation, and any unwanted earlier mouth movement. Do not retry or replace the Flow performance automatically.',
 'assembly_guard':'Codex verifies hashes, guide alignment and timestamp conform30to24 if needed, then keeps original listening before2812 and uses sync for2812..2881 only. Reapply live_v5 loop/marks/panel push after sync. Check source switch at2812 and ensure outgoing astronaut face is offscreen at the vocal handover. No master shift, time stretch, repeated words, FX upload, duplicate soundtrack or new full assembly by Claude.',
 'completion':'Download untouched result and byte-identical synced copy. Write receipt with hashes, native fps, frame count, dimensions, durations/start times, job ID, settings, credits and observations. Add claude_result; status=claude_done_ready_for_codex_verification. No production edits, commits or approval claims.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2))
print('Astronomer Words leave words Kling-only handoff ready; not submitted.')
