from pathlib import Path
import json,sys
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1]
sys.path.insert(0,str(R/'out/fx_tracking_deps'))
import cv2
rows=[]
for f in (range(1,193) if '--full' in sys.argv else [1,25,50,86,138,160,192]):
    a=cv2.imread(str(O/f'probe/native_1280/{f:04d}.png'))
    b=cv2.imread(str(R/f'out/probe_voice_trial/frames/{f-1:04d}.png'))
    if a is None or b is None:continue
    diff=np.abs(a.astype(float)-b.astype(float))
    row={'source_frame':f-1,'mean_error':float(diff.mean()),'p99':float(np.percentile(diff,99))}
    bp=O/f'probe/native_1920/{f:04d}.png'
    big=cv2.imread(str(bp)) if bp.exists() else None
    if big is not None:
        down=cv2.resize(big,(1280,720),interpolation=cv2.INTER_AREA)
        row['resolution_mean_error']=float(np.abs(a.astype(float)-down.astype(float)).mean())
    rows.append(row)
(O/'probe/qa.json').write_text(json.dumps(rows,indent=2))
print(json.dumps({'checked':len(rows),'max_frame_mean_error':max(r['mean_error'] for r in rows),
                  'max_p99':max(r['p99'] for r in rows),
                  'resolution_samples':[r for r in rows if 'resolution_mean_error' in r]},indent=2))
