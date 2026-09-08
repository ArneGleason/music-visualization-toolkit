from pathlib import Path
import json,sys
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(R/'out/fx_tracking_deps'))
import cv2
rows=[]
for family,frames in [('opening',[9,16]),('pressure',[19,48]),('bloom',[43])]:
    for f in frames:
        low=cv2.imread(str(O/family/f'native_1280/{f:04d}.png'))
        high=cv2.imread(str(O/family/f'native_1920/{f:04d}.png'))
        assert low is not None and high is not None
        reduced=cv2.resize(high,(1280,720),interpolation=cv2.INTER_AREA)
        delta=np.abs(reduced.astype(float)-low.astype(float))
        rows.append({'family':family,'frame':f,'mae':float(delta.mean()),'p99':float(np.percentile(delta,99))})
(O/'batch3_peak_resolution.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
assert all(r['mae']<5 for r in rows),'Resolution discrepancy needs visual review'
