"""Prepare a bounded Claude work order, without submitting paid jobs."""
import hashlib
import json
from pathlib import Path
import subprocess
import wave
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

def pcm(p, start=0, seconds=8):
    return subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(p),
        '-af', f'atrim=start={start:.12f}:duration={seconds},asetpts=PTS-STARTPTS',
        '-ac', '1', '-ar', '48000', '-f', 's16le', '-'])

old = ROOT / 'out/opening_performance_v3'
contract = json.loads((old / 'handoff.json').read_text())
reference = np.frombuffer(pcm(ROOT / 'out/opening_sync_test/guide.wav'), dtype='<i2').astype(float)
samples = Path('C:/Users/arneg/OneDrive/Documents/Bitwig Studio/Projects/RiversOnMars/samples')
matches = []
for source in samples.glob('*(Lead Vocal)*.wav'):
    data = np.frombuffer(pcm(source, 143/24 - .178348), dtype='<i2').astype(float)
    correlation = float(np.corrcoef(reference, data)[0, 1])
    matches.append((correlation, source))
correlation, source = max(matches)
assert correlation > .995, matches
origin = 488
start, end = 500, 670
raw_start = origin/24 - .178348
guide = OUT / 'guide.wav'
assert not (OUT / 'base.mp4').exists(), 'Do not overwrite an active handoff'
with wave.open(str(guide), 'wb') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(48000)
    wav.writeframes(pcm(source, raw_start))
with wave.open(str(guide)) as wav:
    assert wav.getnframes() == 384000
lock = (old / 'style_lock_v2.txt').read_bytes()
(OUT / 'style_lock_v2.txt').write_bytes(lock)
prompt = (OUT / 'performance_direction.txt').read_text(encoding='utf-8').rstrip() + '\n\n' + lock.decode('utf-8')
(OUT / 'flow_prompt.txt').write_text(prompt, encoding='utf-8')
assert (OUT / 'flow_prompt.txt').read_text(encoding='utf-8').endswith(lock.decode('utf-8'))
beats = [b for b in json.loads((ROOT / 'generated/overlay_cues.json').read_text())['beats'] if origin <= b['frame'] < origin+192]
periods = np.diff([b['sec'] for b in beats])
still = ROOT / 'codex/out/astronomer_close_sync_b.jpg'
h = {
    'schema_version': 1, 'test_id': 'pieces_performance_v1',
    'project_root': ROOT.as_posix(), 'status': 'ready_for_claude_not_submitted',
    'authorization': contract['authorization'],
    'task': 'One Flow close-up singing take, inspect, then one Kling lip-sync. No specimen generation or assembly.',
    'clock': {'timeline_fps':24, 'indexing':'zero-based end-exclusive',
        'song_origin_frame':origin, 'song_origin_seconds':origin/24,
        'requested_take_frames':192, 'requested_take_seconds':8,
        'lead_stem_placement_offset_seconds':.178348,
        'raw_stem_extract_start_seconds':raw_start,
        'guide_already_aligned':True, 'guide_upload_start_seconds':0,
        'additional_audio_offset_seconds':0},
    'cut': {'review_id':'pieces_close_v1', 'replaces_old_shot_ids':['s005','s006','s007'],
        'song_start_frame':start,'song_end_frame_exclusive':end,
        'source_in_frame_at_24fps':start-origin,'source_out_frame_exclusive_at_24fps':end-origin,
        'duration_frames':end-start,'speed':1},
    'phrases':[
        {'text':"I've got pieces.",'song_frames':[516,602], 'source_seconds':[(516-origin)/24,(602-origin)/24]},
        {'text':'Things that almost fit.','song_frames':[620,658], 'source_seconds':[(620-origin)/24,(658-origin)/24]}],
    'preceding_picture':{'source':'out/opening_specimen_v2/base.mp4',
        'song_frames':[334,500], 'source_frames':[12,178],
        'note':'Proposed one-second extension beyond approved preview end476, real existing motion, not a freeze. Inspect the late hand reach in context; not production adoption.'},
    'following_picture':{'proposed_cut_frame':670,'lyric':'Then they do not quite match.',
        'lyric_song_frames':[680,719], 'status':'future specimen continuation, not commissioned in this handoff; do not restart the previous specimen action'},
    'inputs':{'first_frame':{'file':still.relative_to(ROOT).as_posix(),'sha256':digest(still)},
        'guide':{'file':guide.relative_to(ROOT).as_posix(),'sha256':digest(guide),'sample_rate':48000,'channels':1,'samples':384000},
        'prompt':{'file':'out/pieces_performance_v1/flow_prompt.txt'},
        'lock':{'file':'out/pieces_performance_v1/style_lock_v2.txt','sha256':digest(OUT/'style_lock_v2.txt'),'scope':'Identical to accepted opening v3 performance lock'}},
    'guide_provenance':{'source':source.as_posix(),'source_sha256':digest(source),
        'verification':'Same extraction method compared against accepted opening guide at its original song origin.',
        'opening_guide_correlation':correlation,
        'candidate_correlations':{p.name:c for c,p in matches},
        'processing':'Mono 48k PCM16, exact eight-second trim; no normalization, gating, speed change, silence removal or extra offset.'},
    'output':{'base':'out/pieces_performance_v1/base.mp4','synced':'out/pieces_performance_v1/synced.mp4',
        'receipt':'out/pieces_performance_v1/RECEIPT.md','preserve_original_download':True,'do_not_trim':True,'do_not_retime':True},
    'generation':contract['generation'], 'assembly':contract['assembly'],
    'performance':{'prompt_bpm':84,'measured_local_bpm':float(60/np.mean(periods)),
        'gesture_spacing_beats':[2,4],'beat_source':'generated/overlay_cues.json',
        'beat_grid':[dict(b,source_sec=b['sec']-origin/24) for b in beats],
        'note':'Broad movement direction, not a guarantee of precise generated motion sync.'},
    'coverage_guard':'Minimum picture coverage through source182/24=7.583333s. Measure actual returned timestamps; never stretch or freeze to hide shortfall. Full requested 8s is not guaranteed by Kling.',
    'assembly_caveat':'Old production s005/s006/s007 boundaries are superseded ONLY in the proposed review. Codex must reconcile shotlist AND cues in the isolated preview. No production modifications by Claude.'
}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':h['status'],'correlation':correlation,'guide_sha256':digest(guide),'local_bpm':h['performance']['measured_local_bpm'],'cut':h['cut']},indent=2))
