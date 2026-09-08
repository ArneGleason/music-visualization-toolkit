"""Verify returned media and expose exact assigned B2 cuts, no production edits."""
from pathlib import Path
import hashlib,json,subprocess,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_timebase import conform_clip
h=json.loads((OUT/'handoff.json').read_text())
for r in list(h['inputs'].values())+[h['claude_result']['synced'],h['claude_result']['synced_original']]:
    assert hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['sha256'],r['file']
assert hashlib.sha256((OUT/'base.mp4').read_bytes()).hexdigest()=='9a7056b689a77dd50fcc262540d04033c77bb6f271a899b131135ae6cca556f0'
source=conform_clip(ROOT,{'file':str(OUT/'synced.mp4'),'speed':1},24,prepare=True)['file']
def audio(p):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype='<f4')
a=audio(OUT/'synced.mp4');b=audio(OUT/'guide.wav'); n=min(len(a),len(b)); corr=float(np.corrcoef(a[:n],b[:n])[0,1])
assert corr>.95,corr
fg=[]
for j,(lo,hi) in enumerate([(11,42),(80,111),(141,184)]):
    fg += [f'[0:v]trim=start_frame={lo}:end_frame={hi},setpts=PTS-STARTPTS[v{j}]',f'[1:a]atrim=start={(4320+lo)/24}:end={(4320+hi)/24},asetpts=PTS-STARTPTS[a{j}]']
fg += ['[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]']
subprocess.run(['ffmpeg','-v','error','-n','-i',source,'-i',str(ROOT/'audio/song.wav'),'-filter_complex',';'.join(fg),'-map','[v]','-map','[a]','-frames:v','105','-c:v','libx264','-crf','18','-c:a','aac','-movflags','+faststart',str(OUT/'assigned_replies_review.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'assigned_replies_review.mp4'),'-f','null','-'],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,r_frame_rate','-of','json',str(OUT/'assigned_replies_review.mp4')]))
assert probe['streams'][0]['nb_read_frames']=='105'
assert probe['streams'][0]['r_frame_rate']=='24/1'
(OUT/'codex_verification.json').write_text(json.dumps({'hashes_pass':True,'guide_returned_audio_lag_zero_correlation':corr,'conformed_file':source,'review_frames':105,'review_type':'Three assigned B2 excerpts concatenated for diagnosis, not a continuous assembly. No FX yet.','source_ranges':[[11,42],[80,111],[141,184]],'status':'technical_checks_pass_owner_sync_review_pending'},indent=2))
print('Verified hashes, timestamp conform, audio alignment and105frame review',corr)
