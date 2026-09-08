"""Diagnostics only; never supplies FX imagery to Blender."""
from pathlib import Path
import sys,json
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1]
sys.path.insert(0,str(R/'out/fx_tracking_deps'))
import cv2
rows=[]
for f in [1,25,49,77]:
    native=cv2.imread(str(O/f'aerial/native_1280/{f:04d}.png'))
    ref=cv2.imread(str(O/f'aerial/reference/{f:04d}.png'))
    big=cv2.imread(str(O/f'aerial/native_1920/{f:04d}.png'))
    diff=np.abs(native.astype(float)-ref.astype(float))
    row={'frame':f,'reference_mae_8bit':float(diff.mean()),'reference_p99':float(np.percentile(diff,99))}
    if big is not None:
        down=cv2.resize(big,(1280,720),interpolation=cv2.INTER_AREA)
        row['resolution_mae_8bit']=float(np.abs(native.astype(float)-down.astype(float)).mean())
    rows.append(row)
print(json.dumps(rows,indent=2))
(O/'aerial/qa.json').write_text(json.dumps(rows,indent=2))
