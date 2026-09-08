"""Verify first and last decoded pictures of every shot, not just middles."""
from pathlib import Path
import json,sys,subprocess
import numpy as np
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O.parent/'fx_tracking_deps'));import cv2
actual=json.loads((O/'full_blend_check.json').read_text())['checks'];selected=json.loads((O/'full_selection_check.json').read_text());cap=cv2.VideoCapture(str(O/'full_native_context.mp4'));checks=[]
for number,(shot,meta) in enumerate(zip(actual,selected),1):
 a,z=meta['song_frames'];source=cv2.VideoCapture(shot['file'])
 for label,f in [('first',a),('last',z-1)]:
  cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,p=cap.read();assert ok
  source.set(cv2.CAP_PROP_POS_FRAMES,shot['source_in']+f-a);ok,q=source.read();assert ok,(number,label)
  q=cv2.resize(q,(1280,720));error=float(np.abs(p[40:450,40:1150].astype(float)-q[40:450,40:1150]).mean())
  seek_error=error
  if error>=8:
   # Random-access H.264 decoding can return a damaged edge frame. Confirm
   # suspicious results by decoding sequentially with a separate decoder.
   def exact(path,n):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',f'select=eq(n\\,{int(n)})','-frames:v','1','-f','image2pipe','-vcodec','png','-'])
    return cv2.imdecode(np.frombuffer(raw,np.uint8),cv2.IMREAD_COLOR)
   p=exact(O/'full_native_context.mp4',f);q=cv2.resize(exact(shot['file'],shot['source_in']+f-a),(1280,720))
   error=float(np.abs(p[40:450,40:1150].astype(float)-q[40:450,40:1150]).mean())
  checks.append({'cut':number,'edge':label,'song_frame':f,'difference':error,'random_seek_difference':seek_error,'pass':error<8})
 source.release()
cap.release();issues=[c for c in checks if not c['pass']];(O/'full_cut_edges_check.json').write_text(json.dumps({'checks':checks,'issues':issues},indent=2));assert not issues,issues
print('All 140 first/last cut pictures checked.')
