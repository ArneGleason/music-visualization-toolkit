"""Full-frame diagnostics, native dependency checks live in audit_bends.py."""
from pathlib import Path
import sys,json,numpy as np
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'bends'
sys.path.insert(0,str(R/'out/fx_tracking_deps')); import cv2
cap=cv2.VideoCapture(str(R/'out/bends_mind_fx_v2/clean.mp4')); rows=[]
for f in range(1,138):
    ok,reference=cap.read(); assert ok
    native=cv2.imread(str(D/f'native_1280/{f:04d}.png')); assert native is not None
    difference=np.abs(native.astype(float)-reference.astype(float))
    rows.append({'frame':f,'mae':float(difference.mean()),'p99':float(np.quantile(difference,.99))})
cap.release(); hi=[]
for f in [1,35,70,100,120,137]:
    a=cv2.imread(str(D/f'native_1280/{f:04d}.png')); b=cv2.imread(str(D/f'native_1920/{f:04d}.png')); assert b is not None
    delta=np.abs(a.astype(float)-cv2.resize(b,(1280,720),interpolation=cv2.INTER_AREA).astype(float))
    hi.append({'frame':f,'mae':float(delta.mean()),'p99':float(np.quantile(delta,.99))})
result={'reference_is_encoded':True,'comparison_is_diagnostic_not_owner_approval':True,'all_137_frames':rows,'resolution_samples':hi,'max_mean':max(v['mae'] for v in rows),'max_resolution_mean':max(v['mae'] for v in hi)}
(D/'qa.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ['all_137_frames']},indent=2))

