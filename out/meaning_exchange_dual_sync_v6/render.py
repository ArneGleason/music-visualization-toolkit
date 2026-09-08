"""Astronomer sings Words leave words; preserve the original listening lead."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
folder=ROOT/'out/meaning_astronomer_lipsync_v1'
h=json.loads((folder/'handoff.json').read_text())
for key in ['original','synced']:
    r=h['claude_result'][key]
    assert hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['sha256'].lower()
def run(a):subprocess.run([str(x) for x in a],cwd=ROOT,check=True)
def samples(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a,b=samples(folder/'synced.mp4'),samples(folder/'guide.wav');n=min(len(a),len(b))
astronomer_corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert astronomer_corr>.98
run(['ffmpeg','-v','error','-i',folder/'synced.mp4','-f','null','-'])
run(['ffmpeg','-v','error','-y','-i',folder/'synced.mp4','-vf','fps=24','-an','-c:v','libx264','-crf','16',OUT/'astronomer_24.mp4'])
run(['ffmpeg','-v','error','-y','-i',ROOT/'out/meaning_exchange_handoff_v1/astronomer/base.mp4','-i',OUT/'astronomer_24.mp4',
    '-filter_complex','[0:v]trim=end_frame=38,setpts=N/(24*TB)[a];[1:v]trim=start_frame=38,setpts=N/(24*TB)[b];[a][b]concat=n=2:v=1:a=0[v]',
    '-map','[v]','-an','-c:v','libx264','-crf','16',OUT/'astronomer_combined.mp4'])
recipe=(ROOT/'out/meaning_exchange_live_v5/render.py').read_text().replace('meaning_exchange_live_v5','meaning_exchange_dual_sync_v6')
old="listener_cap=cv2.VideoCapture(str(ROOT/'out/meaning_exchange_handoff_v1/astronomer/base.mp4'))"
assert old in recipe
recipe=recipe.replace(old,"listener_cap=cv2.VideoCapture(str(ROOT/'out/meaning_exchange_dual_sync_v6/astronomer_combined.mp4'))")
exec(compile(recipe,str(OUT/'expanded_live.py'),'exec'),{'__name__':'__main__','__file__':str(OUT/'expanded_live.py')})
v=json.loads((OUT/'verification.json').read_text())
v.update(astronomer_sync_hash=h['claude_result']['synced']['sha256'],astronomer_guide_correlation_zero_lag=astronomer_corr,
    original_listening=[2786,2812],new_astronomer_sync=[2812,2881],status='owner audition pending; no production adoption')
(OUT/'verification.json').write_text(json.dumps(v,indent=2))
print('Astronomer sync integrated for audition:',astronomer_corr,flush=True)
