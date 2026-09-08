"""Verify Kling timestamps and audition approved acting with corrected mouth."""
import copy,hashlib,json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)
h=json.loads((ROOT/'out/excavation_reply_lipsync_v1/handoff.json').read_text())
source=ROOT/h['output']['synced'];digest=hashlib.sha256(source.read_bytes()).hexdigest()
assert digest==h['claude_result']['synced']['sha256']
assert source.read_bytes()==(ROOT/h['claude_result']['original']['file']).read_bytes()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,duration,width,height,start_time','-of','json',str(source)]))['streams'][0]
assert probe['r_frame_rate']=='30/1' and int(probe['nb_frames'])==239
def audio(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32)
a=audio(source);b=audio(ROOT/'out/excavation_reply_lipsync_v1/guide.wav');n=min(len(a),len(b))
corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.98
run(['ffmpeg','-v','error','-y','-i',source,'-vf','fps=24','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'conformed.mp4'])
# Preserve established assembly and source in-point; only plate selection changes.
p=ROOT/'out/excavation_reply_review_v1/render.py'
s=p.read_text();s=s[s.index('edl=json.loads'):]
s=s.replace("h['output']['base']","'out/excavation_reply_synced_v2/conformed.mp4'")
exec(compile(s,str(p),'exec'),globals())
record=json.loads((OUT/'verification.json').read_text())
record.update(status='verified_synced_candidate_owner_review_pending',lip_sync_applied=True,
 guide_zero_lag_correlation=corr,conform='Native30fps timestamp-resampled24fps; no slowdown or extra offset',
 concerns=['Can has restrained articulation','early mouth movement remains during nine-frame pre-phrase bridge'],
 source_original=h['output']['synced'])
(OUT/'verification.json').write_text(json.dumps(record,indent=2))
print('Synced reply ready; guide correlation:',corr)
