"""Same landing audition with returned Kling and rebuilt pressure-lens FX."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
folder=ROOT/'out/rocket_landing_retry_v1'
h=json.loads((folder/'handoff.json').read_text())
for key in ['synced','synced_original']:
    r=h['claude_result'][key]
    assert hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['sha256'].lower()
def samples(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a,b=samples(folder/'synced.mp4'),samples(folder/'guide.wav');n=min(len(a),len(b))
sync_corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert sync_corr>.98
subprocess.run(['ffmpeg','-v','error','-y','-i',str(folder/'synced.mp4'),'-vf','fps=24','-an','-c:v','libx264','-crf','16',str(OUT/'conformed.mp4')],check=True)
code=(ROOT/'out/message_into_rockets_v2/render.py').read_text().replace('message_into_rockets_v2','message_into_rockets_v3')
code=code.replace("assert hashlib.sha256(base.read_bytes()).hexdigest()=='653071bad0731275f5f21a681c544e8bbff742d52ae1f145ab2b29b49c468d81'",'# Returned original hashes checked before conform.')
code=code.replace('out/rocket_landing_retry_v1/base.mp4','out/message_into_rockets_v3/conformed.mp4')
code=code.replace("'kling_done':False","'kling_done':True").replace('no Kling yet.','with Kling.')
exec(compile(code,str(OUT/'expanded.py'),'exec'),{'__name__':'__main__','__file__':str(OUT/'expanded.py')})
v=json.loads((OUT/'verification.json').read_text());v.update(guide_correlation_zero_lag=sync_corr,original_synced_sha256=h['claude_result']['synced']['sha256'],status='owner review pending')
(OUT/'verification.json').write_text(json.dumps(v,indent=2))
print('Verified returned guide alignment:',sync_corr,flush=True)
