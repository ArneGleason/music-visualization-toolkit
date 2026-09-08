from pathlib import Path
import sys,json
import numpy as np
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O.parent/'fx_tracking_deps'));import cv2
actual=json.loads((O/'full_blend_check.json').read_text())['checks'];selected=json.loads((O/'full_selection_check.json').read_text());bounds=[0,856,1650,2484];results=[]
for k in range(3):
 cap=cv2.VideoCapture(str(O/f'full_parts/part{k}.mp4'))
 for number,(shot,meta) in enumerate(zip(actual,selected),1):
  a,z=meta['song_frames'];f=(a+z)//2
  if not bounds[k]<=f<bounds[k+1]:continue
  cap.set(1,f-bounds[k]);ok,p=cap.read();assert ok
  src=cv2.VideoCapture(shot['file']);src.set(1,shot['source_in']+f-a);ok,q=src.read();assert ok;src.release();q=cv2.resize(q,(1280,720));d=float(np.abs(p[40:500,40:1150].astype(float)-q[40:500,40:1150]).mean());results.append({'cut':number,'difference':d})
 cap.release()
(O/'first_parts_check.json').write_text(json.dumps(results,indent=2));print('Maximum difference',max(r['difference'] for r in results));assert max(r['difference'] for r in results)<8
