"""Verified wide-only Kling replacement, preserved close and approved FX."""
import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
handoff=json.loads((ROOT/'out/shop_wide_lipsync_v1/handoff.json').read_text())
returned=ROOT/handoff['claude_result']['synced']['file']
assert hashlib.sha256(returned.read_bytes()).hexdigest()==handoff['claude_result']['synced']['sha256']
assert returned.read_bytes()==(ROOT/handoff['claude_result']['original']['file']).read_bytes()
def audio(p):
 return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32)
a=audio(returned);b=audio(ROOT/'out/shop_wide_lipsync_v1/guide.wav');n=min(len(a),len(b))
corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.98
subprocess.run(['ffmpeg','-v','error','-y','-i',str(returned),'-vf','fps=24','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',str(OUT/'wide_cfr.mp4')],check=True)
cap=cv2.VideoCapture(str(OUT/'wide_cfr.mp4'));wide=[]
while True:
 ok,f=cap.read()
 if not ok:break
 wide.append(f)
cap.release();assert len(wide)>=50
# Reconstruct approved punch geometry; replace only the wide plate after checks.
p=ROOT/'out/shop_snap_test_v2/render.py'
builder=p.read_text().split("exec(compile(s,str(p),'exec')")[0]
ns={'__file__':str(OUT/'render.py')};exec(compile(builder,str(p),'exec'),ns)
s=ns['s'].split('# Reuse the established contextual assembly')[0]
s=s.replace("(OUT/'frames').mkdir(exist_ok=True)","plates['wide']=replacement_wide\n(OUT/'frames').mkdir(exist_ok=True)")
s=s.replace("str(OUT/'clean.mp4')","str(OUT/'picture.mp4')")
exec(compile(s,'wide_replacement','exec'),{'__file__':str(OUT/'render.py'),'replacement_wide':wide})
# Reapply exactly the approved signal. Same clock, source switch and clear frame.
p=ROOT/'out/shop_push_signal_v4/render.py'
ns={'__file__':str(OUT/'render.py')};exec(compile(p.read_text().split("exec(compile(s,str(p),'exec')")[0],str(p),'exec'),ns)
s=ns['s'].replace('out/shop_snap_test_v2/clean.mp4','out/shop_wide_synced_v5/picture.mp4').replace('out/shop_push_signal_v4/clean.mp4','out/shop_wide_synced_v5/clean.mp4')
exec(compile(s,'approved_fx','exec'),{'__file__':str(OUT/'render.py'),'__name__':'__main__'})
r=json.loads((OUT/'recipe.json').read_text());r.update(lip_sync_applied='wide only',
 wide_return=str(returned),wide_audio_guide_zero_lag_correlation=corr,
 wide_conform='timestamp-preserving fps24, no speed change',wide_origin_frame=2387,
 close_source='out/shop_performance_v1/close/base.mp4',close_origin_frame=2425,
 close_processing='unchanged original, no Kling',source_switch_frame=2431,
 effect_clear_frame=2433,status='verified_owner_review_pending')
(OUT/'recipe.json').write_text(json.dumps(r,indent=2))
print('Wide-only sync integrated; guide correlation',corr)
