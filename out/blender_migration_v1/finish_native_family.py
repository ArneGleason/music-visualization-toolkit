"""Decode, resolution-check and encode complete native renders only."""
import sys,json,hashlib,subprocess
from pathlib import Path
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
family=sys.argv[1];count=int(sys.argv[2]);D=O/family
frames=[D/'native_1280'/f'{f:04d}.png' for f in range(1,count+1)]
assert all(p.exists() for p in frames),'Incomplete frame sequence'
resolution=[];tiles=[]
for i,p in enumerate(frames,1):
 image=cv2.imread(str(p));assert image is not None and image.shape==(720,1280,3),p
 hi=D/'native_1920'/p.name
 if hi.exists():
  big=cv2.imread(str(hi));assert big.shape==(1080,1920,3)
  resolution.append({'frame':i,'mean_difference_after_downsample':float(np.abs(image.astype(float)-cv2.resize(big,(1280,720),interpolation=cv2.INTER_AREA)).mean())})
 if i in set(np.linspace(1,count,8).astype(int)):
  thumb=cv2.resize(image,(384,216));cv2.putText(thumb,str(i),(10,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1);tiles.append(thumb)
cv2.imwrite(str(D/'contact.jpg'),np.vstack([np.hstack(tiles[:4]),np.hstack(tiles[4:])]))
assert resolution,'Missing 1080 checks'
movie=D/'native_clean.mp4';subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(D/'native_1280/%04d.png'),'-frames:v',str(count),'-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',str(movie)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
(D/'qa.json').write_text(json.dumps({'status':'technical_checks_complete_visual_review_required','frames':count,'fps':24,'resolution':resolution,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'production_promoted':False},indent=2))
