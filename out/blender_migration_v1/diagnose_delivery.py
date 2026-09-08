import json,sys
from pathlib import Path
import numpy as np
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O.parent/'fx_tracking_deps'));import cv2
actual=json.loads((O/'full_blend_check.json').read_text())['checks'];selected=json.loads((O/'full_selection_check.json').read_text());cap=cv2.VideoCapture(str(O/'full_native_context.mp4'))
for number in [19,24,36,46]:
 s=actual[number-1];m=selected[number-1];a,z=m['song_frames'];f=(a+z)//2;cap.set(1,f);_,p=cap.read();src=cv2.VideoCapture(s['file']);src.set(1,s['source_in']+f-a);_,q=src.read();q=cv2.resize(q,(1280,720));cv2.imwrite(str(O/f'compare_{number}.jpg'),np.hstack([p,q]))
 x=q[40:500,40:1150].astype(float).reshape(-1);y=p[40:500,40:1150].astype(float).reshape(-1);coef=np.polyfit(x[::10],y[::10],1);print(number,coef,'corrected',np.abs(y-np.polyval(coef,x)).mean(),'corr',np.corrcoef(x,y)[0,1]);src.release()
