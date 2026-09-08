"""Prepare a Kling-only repair aligned to the current shore edit."""
import hashlib,json,subprocess,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
source=ROOT/'clips/raw/basin_edge_sync_v6.mp4'
origin=3302/24-2.84
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=next(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-map','0:v:0','-c:v','copy','-an',str(OUT/'base.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(stem),'-af',f'atrim=start={origin-.178348}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'guide.wav')],check=True)
with wave.open(str(OUT/'guide.wav')) as w: assert w.getnframes()==384000
def ref(p):return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
h={
 'schema_version':1,'test_id':'swimmer_shore_lipsync_v1','project_root':str(ROOT),'status':'ready_for_claude_not_submitted',
 'task':'One Kling-only lip-sync repair of the existing singing shore performance. Use original Flow base, NOT old Kling. Preserve current edit and swimmer effects.',
 'authorization':{'max_flow_submissions':0,'max_kling_submissions':1,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'kling':{'mode':'Lip Sync','character':'real red-haired woman kneeling in foreground, NOT any chrome swimmer','guide_start_seconds':0,'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical estimate only; verify UI. No purchases.'},
 'inputs':{'base':ref(OUT/'base.mp4'),'guide':ref(OUT/'guide.wav')},'original_source':ref(source),
 'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_seconds':origin,'song_origin_frame_equivalent':origin*24,'source_in_seconds':2.84,'song_cut_start_frame':3302,'lead_stem_placement_offset_seconds':.178348,'raw_stem_extract_start_seconds':origin-.178348,'guide_already_aligned':True,'additional_audio_offset_seconds':0,'note':'Preserve existing fractional-second in-point2.84 exactly. Do not round source clock or add half-second lead-in. Full base already supplies2.84seconds of context before visible cut.'},
 'cut':{'shot_id':'s042','song_frames':[3302,3370],'source_seconds':[2.84,2.84+68/24],'speed':1,'current_snapshot':'out/spring_into_swimmers_v1/shotlist.json'},
 'lyric_context':{'full_first_phrase_song_frames':[3229,3357],'text':'Chrome-plated bodies go swimming / in the rivers of Mars.','visible_words':'go swimming, then the start of in; other words play over swimmer coverage in current edit','go_song_frame':3303,'swimming_song_frame':3322,'in_song_frame':3357,'guard':'Do not shift go swimming to source zero. The audio file already places words correctly. The entire rivers of Mars line is NOT on the visible face; no need to extend this face shot.'},
 'guide_provenance':{'source':str(stem),'processing':'Continuous8second mono48k PCM16 slice. No normalization, gate, silence removal, stretching or extra offsets.'},
 'output':{'synced':'out/swimmer_shore_lipsync_v1/synced.mp4','receipt':'out/swimmer_shore_lipsync_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'tool_time_counts':True,'respect_rate_limits':True},
 'quality_notes':'Check active articulation throughout source2.84..5.673333, especially go/swimming at source2.881667/3.673333 and in at5.131667. No missing-word blank gaps, puppet lips or facial warping. Preserve camera, costume and swimmers. Report defects; no automatic retry.',
 'assembly_guard':'Codex verifies result/guide alignment, timestamp-conforms native30fps to24fps if needed and replaces only s042 at its existing2.84second in-point. Preserve approved spring transition and protected s043/s044 violet-pearl FX. Master/lyrics once. No assembly or new Flow by Claude.',
 'completion':'Download untouched original and byte-identical synced.mp4. Write RECEIPT.md with hashes, job ID, actual settings/credits, native fps/frame count, duration/start times and articulation observations. Add claude_result and status=claude_done_ready_for_codex_verification. No commit or owner approval claims.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2))
print('Ready for Claude; no external submission made.')
