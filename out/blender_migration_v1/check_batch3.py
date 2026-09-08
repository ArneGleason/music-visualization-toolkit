"""Read-only pixel checks. This never generates effects."""
from pathlib import Path
import sys,json
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(R/'out/fx_tracking_deps'))
import cv2
refs={'birds':'out/garden_birds_fx_v2/frames','guide':'out/garden_walk_guide_v1/frames','bloom':'out/garden_bloom_synced_v5/frames','pressure':'out/message_into_rockets_v3/fx/frames','swim043':'out/swimmer_cutaway_v2/fx/s043/violet','swim044':'out/swimmer_fx_full/s044/violet','swim047':'out/swimmer_fx_full/s047/violet'}
refs['tunnel']='out/tunnel_arrival_o01/frames'
results=[]
for family,ref in refs.items():
    rows=[]
    for path in sorted((O/family/'native_1280').glob('*.png')):
        f=int(path.stem);a=cv2.imread(str(path));b=cv2.imread(str(R/ref/f'{f-1:04d}.png'))
        if b is None:continue
        delta=np.abs(a.astype(float)-b.astype(float))
        row={'frame':f,'mae':float(delta.mean()),'p99':float(np.percentile(delta,99))}
        hi=O/family/f'native_1920/{f:04d}.png'
        if hi.exists():row['resolution_mae']=float(np.abs(cv2.resize(cv2.imread(str(hi)),(1280,720),interpolation=cv2.INTER_AREA).astype(float)-a.astype(float)).mean())
        rows.append(row)
    if rows:
        (O/family/'qa.json').write_text(json.dumps(rows,indent=2))
        results.append({'family':family,'frames_checked':len(rows),'max_frame_mae':max(r['mae'] for r in rows),'max_p99':max(r['p99'] for r in rows),'resolution_samples':sum('resolution_mae' in r for r in rows)})
(O/'batch3_qa.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
