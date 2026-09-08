"""Same untrimmed garden plate, newly aligned guide for the approved bloom cut."""
import copy
import hashlib
import json
import subprocess
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
ORIGIN = 1720
OFFSET = .178348

def run(args):
    subprocess.run([str(x) for x in args], cwd=ROOT, check=True)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

old = json.loads((ROOT/'out/garden_begin_lipsync_v1/handoff.json').read_text())
source = ROOT/'clips/raw/forest_awakening_frontal_v6.mp4'
stem = Path(old['guide_provenance']['source'])
start = ORIGIN/24-OFFSET
run(['ffmpeg','-v','error','-y','-i',source,'-map','0:v:0','-c:v','copy',
     '-an','-movflags','+faststart',OUT/'base.mp4'])
run(['ffmpeg','-v','error','-y','-i',stem,'-af',
     f'atrim=start={start:.12f}:duration=8,asetpts=PTS-STARTPTS',
     '-ac','1','-ar','48000','-c:a','pcm_s16le',OUT/'guide.wav'])
with wave.open(str(OUT/'guide.wav'),'rb') as f:
    assert (f.getnframes(),f.getframerate(),f.getnchannels(),f.getsampwidth()) == (384000,48000,1,2)

def frame_hashes(path):
    data = subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
                                   '-map','0:v:0','-f','framemd5','-']).decode()
    return [line for line in data.splitlines() if not line.startswith('#')]

assert frame_hashes(source) == frame_hashes(OUT/'base.mp4')
h = copy.deepcopy(old)
h.pop('claude_result', None)
h['test_id'] = 'garden_bloom_lipsync_v2'
h['status'] = 'ready_for_claude_not_submitted'
h['task'] = 'ONE fresh Kling Lip Sync on original unsynced garden plate, with NEW guide aligned to later pollen-bloom selection. NO Flow. Never re-sync the old Kling output.'
h['clock'].update(song_origin_frame=ORIGIN,song_origin_seconds=ORIGIN/24,
                  raw_stem_extract_start_seconds=start)
h['cut'].update(shot_id='garden_bloom_lipsync_test',song_end_frame_exclusive=1854,
                source_in_frame_at_24fps=66,source_out_frame_exclusive_at_24fps=134,
                duration_frames=68,
                picture_change='EXACT approved bloom placement: original source66..134 -> song1786..1854. Source108 on begin1828. Full plate is unchanged; only guide origin changes. No shift to picture, no padding/retime.')
for phrase in h['phrases']:
    phrase['source_seconds'] = [(f-ORIGIN)/24 for f in phrase['song_frames']]
    for word in phrase['words']:
        word['source_seconds'] = [(f-ORIGIN)/24 for f in word['song_frames']]
h['inputs']['base'].update(file='out/garden_bloom_lipsync_v2/base.mp4',
                          sha256=sha(OUT/'base.mp4'),source_sha256=sha(source))
h['inputs']['guide'].update(file='out/garden_bloom_lipsync_v2/guide.wav',
                           sha256=sha(OUT/'guide.wav'))
h['guide_provenance']['processing'] = 'NEW uninterrupted8second mono48k PCM16 vocal slice for origin1720. Placement correction applied once. No gating, normalization, silence removal, gain or timing changes. Context outside visible cut is not approved face coverage.'
h['output'].update(synced='out/garden_bloom_lipsync_v2/synced.mp4',
                   receipt='out/garden_bloom_lipsync_v2/RECEIPT.md')
h['inspection'] = 'Inspect original-source2.75..5.583333 seconds. Words2.75..5.041667, then13frame settling tail. Small quiet face was weak in prior test: inspect every word honestly, including sustained begin, plus mouth closure after phrase. Verify pollen development remains unchanged. No auto retry or Flow.'
h['assembly_guard'] = 'Source0 maps to song1720, NOT1774. Timestamp-conform30fps if needed. Use synced source66..134 at24fps, speed1, for song1786..1854. Minimum returned coverage134/24seconds. Reapply light FX at song timing. Codex will relocate green guide above head after return; never upload baked FX/lyrics/master or old synced.mp4.'
h['owner_direction'] = {'bloom_placement':'Approved later pollen burst selection; preserve exactly.',
                       'green_guide':'Move dance above her head, clear of pollen and bottom lyrics. Codex task only, not Kling input.',
                       'sequence':'Prepare handoff first; separate green-guide revision and later same-clock integration.',
                       'prior_test':'Keep garden_begin_lipsync_v1 untouched; this is a newly authorized single test, not automatic retry.'}
(OUT/'handoff.json').write_text(json.dumps(h,indent=2)+'\n')
print('Ready: unchanged192-frame clean plate, NEW384000-sample guide. Source108 = song1828; visible66..134.')
