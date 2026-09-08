"""Prepare a clean existing take and a single-clock uninterrupted vocal guide."""
import json,hashlib,subprocess,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
OUT.mkdir(exist_ok=True)
def run(a):subprocess.run([str(v) for v in a],cwd=ROOT,check=True)
source=ROOT/'clips/raw/forest_awakening_frontal_v6.mp4'
local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stems=list(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'));assert len(stems)==1
stem=stems[0];origin=1774;offset=.178348;start=origin/24-offset
run(['ffmpeg','-v','error','-y','-i',source,'-map','0:v:0','-c:v','copy','-an','-movflags','+faststart',OUT/'base.mp4'])
run(['ffmpeg','-v','error','-y','-i',stem,'-af',f'atrim=start={start:.12f}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-c:a','pcm_s16le',OUT/'guide.wav'])
with wave.open(str(OUT/'guide.wav'),'rb') as f:
 assert (f.getnframes(),f.getframerate(),f.getnchannels(),f.getsampwidth())==(384000,48000,1,2)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def framehash(p):
 data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-f','framemd5','-'])
 return [line for line in data.decode().splitlines() if not line.startswith('#')]
assert framehash(source)==framehash(OUT/'base.mp4'),'Remux changed video frames'
h={'schema_version':1,'test_id':'garden_begin_lipsync_v1','project_root':str(ROOT),'status':'ready_for_claude_not_submitted',
 'task':'One Kling Lip Sync on the existing clean garden awakening take. NO Flow generation. Codex reapplies accepted FX after verification.',
 'authorization':{'max_flow_submissions':0,'max_kling_submissions':1,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'kling':{'mode':'Lip Sync','character':'Character 1 (sole woman)','guide_start_seconds':0,'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'10 credits is historical expectation, not live quote. Check actual UI first.'},
 'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':origin,'song_origin_seconds':origin/24,'requested_take_seconds':8,'requested_take_frames':192,'lead_stem_placement_offset_seconds':offset,'raw_stem_extract_start_seconds':start,'guide_already_aligned':True,'guide_upload_start_seconds':0,'additional_audio_offset_seconds':0},
 'cut':{'shot_id':'garden_begin_lipsync_test','setup':'forest_awakening_frontal','song_start_frame':1786,'song_end_frame_exclusive':1841,'source_in_frame_at_24fps':12,'source_out_frame_exclusive_at_24fps':67,'duration_frames':55,'speed':1,'picture_change':'Previous FX used original source0..55. This sync test uses original12..67 to supply12 genuine lead frames. No freeze or retiming; Codex must rebuild FX against this new picture interval.'},
 'phrases':[{'text':'for the song to begin.','song_frames':[1786,1841],'source_seconds':[.5,67/24],'words':[{'text':w,'song_frames':[a,b],'source_seconds':[(a-origin)/24,(b-origin)/24]} for w,a,b in [('for',1786,1797),('the',1797,1807),('song',1807,1819),('to',1819,1828),('begin',1828,1841)]]}],
 'inputs':{'base':{'file':'out/garden_begin_lipsync_v1/base.mp4','sha256':sha(OUT/'base.mp4'),'source':'clips/raw/forest_awakening_frontal_v6.mp4','source_sha256':sha(source),'video_frames_identical_to_source':True,'audio_removed':True,'width':1280,'height':720,'fps':24,'frames':192},'guide':{'file':'out/garden_begin_lipsync_v1/guide.wav','sha256':sha(OUT/'guide.wav'),'sample_rate':48000,'channels':1,'samples':384000}},
 'guide_provenance':{'source':str(stem),'source_sha256':sha(stem),'processing':'Uninterrupted8second mono48k PCM16 extraction; no gate, gain change, normalization, silence removal or extra offset. Includes preceding vocal tail and following context outside visible cut. Do not treat following dialogue as approved coverage.'},
 'output':{'synced':'out/garden_begin_lipsync_v1/synced.mp4','receipt':'out/garden_begin_lipsync_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'respect_rate_limits':True,'tool_time_counts':True},
 'inspection':'Check visible source0.5..2.7916667 seconds word by word. Quiet closed-mouth base and small face are known risks: report omitted words, puppet mouth, identity shifts, mouth movement after vocal and any framing/set change. Do not regenerate or retry without owner approval.',
 'assembly_guard':'Codex timestamp-conforms any30fps return, never frame-for-frame reinterpretation. Reapply garden_begin_guide_v2 light/green-guide recipe at song1786..1841 against synced source12..67. Never upload processed FX, captions or master soundtrack. Preserve existing approved effects and source as fallback. Minimum source coverage67/24seconds; actual returned coverage must be measured.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
print('Prepared192-frame clean video and384000-sample guide. All video frames unchanged by audio removal.')
