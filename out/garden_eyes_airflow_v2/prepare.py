"""Measure broad plate motion, not a full 3D camera solve."""
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
cap=cv2.VideoCapture(str(ROOT/'out/garden_eyes_motion_v1/base.mp4'))
frames=[]
for i in range(81):
 ok,f=cap.read();assert ok
 frames.append(f)
clahe=cv2.createCLAHE(3,(8,8))
grays=[clahe.apply(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)) for f in frames]
mask=np.full((720,1280),255,np.uint8)
for f in frames[::10]:
 h=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
 bright=((h[:,:,1]>55)&(h[:,:,2]>90)).astype(np.uint8)*255
 mask[cv2.dilate(bright,np.ones((41,41),np.uint8))>0]=0
mask[600:]=0
points=cv2.goodFeaturesToTrack(grays[0],1200,.008,9,mask=mask)
records=[];masks=[]
for i,(f,g) in enumerate(zip(frames,grays)):
 q,status,err=cv2.calcOpticalFlowPyrLK(grays[0],g,points,None,winSize=(41,41),maxLevel=4)
 back,st,_=cv2.calcOpticalFlowPyrLK(g,grays[0],q,None,winSize=(41,41),maxLevel=4)
 valid=(status[:,0]>0)&(st[:,0]>0)&(np.linalg.norm(back-points,axis=2)[:,0]<1.5)
 a,b=points[valid,0],q[valid,0]
 mat,inliers=cv2.estimateAffinePartial2D(a,b,method=cv2.RANSAC,ransacReprojThreshold=2.5)
 assert mat is not None
 records.append({'frame':i,'scale':float(np.hypot(mat[0,0],mat[1,0])),
 'center':(mat@np.array([640,360,1])).tolist(),'inliers':int(inliers.sum()),'tracked':len(a)})
 h=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
 eyes=((h[:,:,1]>65)&(h[:,:,2]>85)).astype(np.uint8)
 distance=cv2.distanceTransform(1-eyes,cv2.DIST_L2,3)
 masks.append(np.clip((distance-6)/20,0,1).astype(np.float32))
np.save(OUT/'eye_clearance.npy',np.asarray(masks))
# Smooth fit avoids interpreting local creature movement as camera jitter.
x=np.arange(81);scale=np.polyval(np.polyfit(x,[r['scale'] for r in records],2),x)
scale/=scale[0]
centers=np.array([r['center'] for r in records]); centers=np.stack([np.polyval(np.polyfit(x,centers[:,j],2),x) for j in range(2)],axis=1)
centers-=centers[0]-[640,360]
data={'method':'Background-feature robust similarity, quadratic smoothing. Approximate depth, not a calibrated 3D solve.',
 'raw':records,'scale':scale.tolist(),'center':centers.tolist()}
(OUT/'camera.json').write_text(json.dumps(data,indent=2))
print('scale endpoints',scale[[0,-1]],'center',centers[-1], 'inliers',min(r['inliers'] for r in records))
