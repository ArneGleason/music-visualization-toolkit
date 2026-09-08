"""Tracked aperture reveal and restrained leaf phosphor, no new generation."""
import json,sys,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
OUT.mkdir(exist_ok=True);(OUT/'composite').mkdir(exist_ok=True)
# Paired eyes share an animal's cue, with a one-frame asymmetry. Waking=1621.
groups=[('far_amber',[(495,175),(509,175)],6,24),
 ('left_cyan',[(296,207),(345,207)],13,37),
 ('right_pink',[(935,216),(970,216)],12,44),
 ('middle_amber',[(665,307),(682,307)],6,31),
 ('middle_green',[(530,378),(544,378)],5,49),
 ('right_violet',[(817,385),(849,385)],11,53),
 ('low_green',[(636,431)],6,58),
 ('right_cyan',[(1107,403),(1184,403)],20,57),
 ('left_amber',[(154,459),(237,453)],23,51)]
eyes=[{'name':name,'p':np.array(p,dtype=float),'radius':r,'on':on+j,'side':j} for name,ps,r,on in groups for j,p in enumerate(ps)]
y,x=np.mgrid[:720,:1280].astype(np.float32)
cap=cv2.VideoCapture(str(ROOT/'out/garden_eyes_motion_v1/base.mp4'))
rng=np.random.default_rng(713);noise=rng.random((360,640)).astype(np.float32);previous=None
records=[]
def smooth(a):
 a=np.clip(a,0,1);return a*a*(3-2*a)
for frame in range(81):
 ok,base=cap.read();assert ok
 comp=cv2.imread(str(ROOT/'out/garden_eyes_airflow_v2/composite'/f'{frame:04d}.png')).astype(np.float32)
 hsv=cv2.cvtColor(base,cv2.COLOR_BGR2HSV)
 bright=(hsv[:,:,1]>65)&(hsv[:,:,2]>85)
 yy,xx=np.nonzero(bright);pixels=np.stack([xx,yy],axis=1)
 positions=np.array([e['p'] for e in eyes]);dist=((pixels[:,None,:]-positions[None,:,:])**2).sum(2)
 assigned=dist.argmin(1)
 cover=np.zeros((720,1280),np.float32);clear=np.zeros_like(cover);eye_info=[]
 for j,e in enumerate(eyes):
  gate=e['radius']+13
  pts=pixels[(assigned==j)&(dist[:,j]<gate**2)]
  if len(pts)>=3:
   center=pts.mean(0);e['p']=center
   rx=max(e['radius']*.65,(pts[:,0].max()-pts[:,0].min()+1)/2)
   ry=max(e['radius']*.65,(pts[:,1].max()-pts[:,1].min()+1)/2)
  else:center=e['p'];rx=ry=e['radius']
  # Feather extends beyond luminous eye to hide its existing bloom when shut.
  d=np.sqrt(((x-center[0])/(rx+9))**2+((y-center[1])/(ry+9))**2)
  region=1-smooth((d-.92)/.45)
  clear=np.maximum(clear,region)
  opening=float(smooth((frame-e['on'])/9))
  lid_curve=np.sqrt(np.clip(1-((x-center[0])/(rx+12))**2,0,1))
  aperture=smooth((opening*(ry+14)*lid_curve-np.abs(y-center[1]))/2.5)
  # Full opening restores the exact source, including surrounding halo.
  hide=region*(1-aperture)*(1-smooth((opening-.85)/.15))
  cover=np.maximum(cover,hide)
  eye_info.append({'name':e['name'],'side':e['side'],'center':center.tolist(),'opening':opening,'pixels':len(pts)})
 # Inpaint source eyes only, never fill arbitrary moving scene objects.
 remove=(clear>.02).astype(np.uint8)*255
 dark=cv2.inpaint(base,remove,6,cv2.INPAINT_TELEA).astype(np.float32)
 comp=comp*(1-cover[:,:,None])+dark*cover[:,:,None]
 # Lift actual leaf detail, not the black floor or luminous eyes/particles.
 b=base.astype(np.float32)/255
 lum=cv2.cvtColor(base,cv2.COLOR_BGR2GRAY).astype(np.float32)/255
 leaf=smooth((lum-.015)/.06)*(1-smooth((lum-.22)/.16))*(1-clear)
 lift=(np.power(b,.86)-b)*255*.68
 comp+=lift*leaf[:,:,None]
 # Shape-bound noisy phosphor. Low-amplitude grain follows optical flow;
 # gradients are taken from the moving plate, not the particle composite.
 gray=cv2.resize(cv2.cvtColor(base,cv2.COLOR_BGR2GRAY),(640,360))
 if previous is not None:
  flow=cv2.calcOpticalFlowFarneback(gray,previous,None,.5,3,19,3,5,1.2,0)
  gy,gx=np.mgrid[:360,:640].astype(np.float32)
  noise=cv2.remap(noise,gx+flow[:,:,0],gy+flow[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
  noise=.93*noise+.07*rng.random(noise.shape).astype(np.float32)
 previous=gray
 fine=cv2.resize(noise,(1280,720),interpolation=cv2.INTER_LINEAR)
 gradx=cv2.Sobel(lum,cv2.CV_32F,1,0,ksize=3);grady=cv2.Sobel(lum,cv2.CV_32F,0,1,ksize=3)
 edge=np.clip(np.hypot(gradx,grady)*7,0,1)*leaf
 speck=np.clip((fine-.43)*7,0,1)
 pulse=1+.35*np.exp(-((frame-55)/12)**2)
 phosphor=edge*speck*7*pulse
 phosphor+=cv2.GaussianBlur(phosphor,(0,0),1.7)*.65
 comp+=phosphor[:,:,None]*np.array([.66,1.,.76],np.float32)
 cv2.imwrite(str(OUT/'composite'/f'{frame:04d}.png'),np.clip(comp,0,255).astype(np.uint8))
 records.append({'song_frame':1569+frame,'eyes':eye_info})
(OUT/'tracking.json').write_text(json.dumps(records,indent=2))
(OUT/'recipe.json').write_text(json.dumps({'status':'owner_review_pending','song_frames':[1569,1650],
 'waking_frame':1621,'opening_groups':[(n,o) for n,p,r,o in groups],
 'method':'Source-color tracked soft aperture and inpainted closed-eye patch; no generated eyelids. Flow-advected noisy leaf contours plus shadow-detail lift.',
 'source':'out/garden_eyes_motion_v1/base.mp4','airflow':'out/garden_eyes_airflow_v2/composite',
 'unchanged':'Source timing, particles, camera, lyric choreography and font fix'},indent=2))
# Preserve shared-resolver assembly and exact time mappings from previous test.
p=ROOT/'out/garden_eyes_airflow_v2/assemble.py';s=p.read_text().replace('garden_eyes_airflow_v2','garden_waking_v3').replace('garden_eyes_airflow_motion_audition','garden_waking_motion_audition')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'assemble.py')})
