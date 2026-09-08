"""Prepare one Kling test from the approved base, preserving source time."""
import hashlib
import json
import subprocess
import wave
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
assert not (OUT/'handoff.json').exists(), 'Never reset submitted work.'
source = ROOT/'out/outro_A1_v3/base.mp4'
assert hashlib.sha256(source.read_bytes()).hexdigest() == '99124a5780cd629cb086e9d362db2e1d78bb5afa2a9d89ca41fc09a428c13767'
local = json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stems = list(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
assert len(stems) == 1
stem = stems[0]
start = 4165/24 - .178348
subprocess.run(['ffmpeg','-v','error','-n','-i',str(source),'-map','0:v:0','-c:v','copy','-an',str(OUT/'base.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(stem),'-af',f'atrim=start={start}:duration=8,asetpts=PTS-STARTPTS','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'guide.wav')],check=True)
with wave.open(str(OUT/'guide.wav')) as w:
    assert (w.getnframes(),w.getframerate(),w.getnchannels()) == (384000,48000,1)
    guide = np.frombuffer(w.readframes(w.getnframes()),dtype='<i2')
def raw(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-f','hash','-hash','sha256','-'])
assert raw(source) == raw(OUT/'base.mp4'), 'Decoded picture changed during audio removal.'
def ref(p):
    return {'file':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
h = {
 'schema_version':1,'test_id':'outro_A1_kling_v1','project_root':ROOT.as_posix(),
 'status':'ready_for_claude_not_submitted',
 'task':'ONE Kling Lip Sync using approved A1 v3 original performance. NO Flow or retry.',
 'authorization':{'max_flow_submissions':0,'max_kling_submissions':1,'automatic_retries':False,'production_edit_changes':False},
 'generation':{'kling':{'mode':'Lip Sync','character':'sole real woman','guide_start_seconds':0,'guide_duration_seconds':8,'sound_from_video':False,'expected_credits':10},'stop_if_unavailable_or_cost_exceeds_expected':True,'cost_note':'Historical estimate. Check actual UI, no purchases or upgrades.'},
 'clock':{'timeline_fps':24,'indexing':'zero-based end-exclusive','song_origin_frame':4165,'song_end_frame_exclusive':4357,'lead_stem_placement_offset_seconds':.178348,'raw_stem_extract_start_seconds':start,'guide_already_aligned':True,'additional_audio_offset_seconds':0},
 'inputs':{'base':ref(OUT/'base.mp4'),'guide':ref(OUT/'guide.wav')},'original_source':ref(source),
 'guide_provenance':{'source':str(stem),'processing':'Continuous8second mono48k PCM16 slice. No gating, normalization, silence removal, concatenation or time stretching. Known project stem placement offset applied once during extraction. Not a speaker-separated stem.', 'samples':384000,'includes_other_speaker_context':True},
 'visible_cuts':[{'song_frames':[4177,4232],'source_frames_at_24fps':[12,67],'text':'You still there?'},{'song_frames':[4262,4331],'source_frames_at_24fps':[97,166],'text':'Never mind / La-la-la, low light'}],
 'assembly_guard':'Keep source time running while offscreen. Other-speaker reply is context only, never select A1 during that reply. No retiming to generated scratch speech. Review question onset/tail and low light tail for missed syllables; retain original listening frames where necessary after review. No guaranteed sync quality. TV FX later, not uploaded now. Final master once.',
 'output':{'synced':'out/outro_A1_kling_v1/synced.mp4','receipt':'out/outro_A1_kling_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
 'polling':{'first_check_seconds':30,'default_interval_seconds':20,'at_90_percent_seconds':10,'no_progressive_backoff':True,'tool_time_counts':True,'respect_rate_limits':True},
 'completion':'Download full untouched original plus byte-identical synced.mp4. Record hashes, settings, credits, job ID, native fps/count/duration/dimensions and observations in RECEIPT.md; add claude_result and flip status to claude_done_ready_for_codex_verification. Return imperfect results, no automatic retry, no assembly or commit.'
}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
verification={'picture_decode_hash_equal':True,'guide_samples':len(guide),'guide_seconds':len(guide)/48000,'raw_stem_start_seconds':start,'song_start_seconds':4165/24,'applied_offset_seconds':.178348,'guide_peak':float(np.max(np.abs(guide.astype(float)))/32768),'limits':'Construction and source-clock checks only; phoneme-level perceptual success must be reviewed after Kling. Previous gated guide not reused.'}
(OUT/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
print(json.dumps(verification))
