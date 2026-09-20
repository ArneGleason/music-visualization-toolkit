from pathlib import Path
import subprocess,json,math,sys
import numpy as np
from PIL import Image,ImageFilter
from scipy.ndimage import map_coordinates,gaussian_filter
O=Path(__file__).resolve().parent;R=O.parents[1];W,H=1280,720
Y,X=np.mgrid[:H,:W].astype(np.float32)
def smooth(a,b,x):
 t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
def warp(im,dx,dy):
 coords=[np.clip(Y+dy,0,H-1),np.clip(X+dx,0,W-1)]
 return np.stack([map_coordinates(im[:,:,c],coords,order=1,mode='nearest') for c in range(3)],axis=2)
def read(p):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf','scale=1280:720','-f','rawvideo','-pix_fmt','rgb24','-']);return np.frombuffer(raw,np.uint8).reshape(-1,H,W,3)
def track(keys,f):
 return tuple(np.interp(f,[k[0] for k in keys],[k[c] for k in keys]) for c in (1,2))
rng=np.random.default_rng(31)
events=[(28,640,100),(43,940,285),(56,1060,390),(67,400,390),(76,1030,560)]
particles=[]
for start,x,y in events:
 for j in range(12):particles.append((start+int(rng.integers(0,5)),x+rng.uniform(-45,45),y+rng.uniform(-18,18),rng.uniform(-3,3),rng.uniform(-2.8,.5),rng.uniform(22,48),rng.uniform(.20,.32)))
for name in (sys.argv[1:] or ['shrink-b','grow-a','grow-b','smoke-b']):
 folder='SCENE11-SMOKE-002' if name=='smoke-b' else 'SCENE11-TRANSFORMS-001';src=R/f'motion-graphics/{folder}/{name}-timed-v001.mp4';frames=read(src)
 out=O/f'{name}-polished-v001.mp4';enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',str(out)],stdin=subprocess.PIPE)
 for f,frame in enumerate(frames):
  im=frame.astype(np.float32)
  if name=='shrink-b' and f>=67:
   cx,cy=track([(67,935,496),(73,967,490),(80,970,488),(89,968,486)],f);dx=X-cx;dy=(Y-cy)/.68;rad=np.hypot(dx,dy)
   mask=smooth(3,20,dx)*(1-smooth(170,245,dx))*np.exp(-((Y-cy)/76)**4)
   amount=np.zeros((H,W),np.float32)
   for start in range(67,90,5):
    age=f-start
    if 0<=age<24:
     band=(rad-(12+age*11))/10;amount+=19*np.exp(-.5*band*band)*np.cos(band*1.8)*(1-age/30)
   amount*=mask*min(1,(f-66)/3);im=warp(im,amount*dx/np.maximum(rad,1),amount*dy/np.maximum(rad,1)*.68)
  if name=='grow-a':
   cx,cy=track([(0,580,440),(12,620,405),(24,540,365),(35,570,355)],f)
   gain=smooth(0,23,f);ell=((X-cx)/250)**2+((Y-cy)/280)**2
   weight=np.exp(-ell*ell*1.8);scale=1+.32*gain
   im=warp(im,-(X-cx)*(1-1/scale)*weight,-(Y-cy)*(1-1/scale)*weight)
   # Broad anchored push reinforces expansion without a hard moving matte.
   z=1+.065*gain;im=warp(im,(X-640)*(1/z-1),(Y-340)*(1/z-1))
  if name=='grow-b':
   dx=np.zeros((H,W),np.float32);dy=dx.copy()
   for start,cx,cy in events:
    age=f-start
    if age>=0:
     kick=math.exp(-age/5)*math.sin(age*2.3+1);mask=np.exp(-(((X-cx)/200)**4+((Y-cy)/170)**4));dx+=4.8*kick*mask;dy+=3*kick*mask
   im=warp(im,dx,dy)
   for start,cx,cy,vx,vy,r,alpha in particles:
    age=f-start
    if 0<=age<34:
     xx=cx+vx*age;yy=cy+vy*age+.105*age*age;rad=r*(.6+age*.075)
     a=np.exp(-(((X-xx)/rad)**2+((Y-yy)/(rad*.7))**2)*2)*alpha*min(1,(age+1)/3)*max(0,1-age/34)
     im=im*(1-a[:,:,None])+np.array([171,145,105],np.float32)*a[:,:,None]
   # Fine debris from beam-joint impacts, in gravity arcs.
   for start,cx,cy in events:
    age=f-start
    if 0<=age<24:
     for j in range(6):
      xx=int(cx+(j-2.5)*2.8*age);yy=int(cy-(j%3+1)*1.1*age+.35*age*age)
      if 2<xx<W-3 and 2<yy<H-5:im[yy:yy+4,xx:xx+2]=[128,111,80]
  if name=='smoke-b' and f>=27:
   q=float(smooth(29,50,f));sigma=18*(1-q)
   blurred=np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(sigma)),dtype=np.float32)
   cloud=np.array(Image.fromarray(frames[30]).filter(ImageFilter.GaussianBlur(9)),dtype=np.float32)
   cx,cy=890,330;mask=np.exp(-(((X-cx)/330)**4+((Y-cy)/400)**4))*smooth(470,650,X)
   hold=.78*(1-q)*float(smooth(27,32,f));mix=blurred*(1-hold)+cloud*hold
   im=im*(1-mask[:,:,None])+mix*mask[:,:,None]
  enc.stdin.write(np.uint8(np.clip(im,0,255)).tobytes())
 enc.stdin.close();assert enc.wait()==0;print(name,'complete',flush=True)
(O/'settings.json').write_text(json.dumps({'roar_master_start':3492,'roar_full_strength':3494,'roar_amplitude_px':19,'growth':'soft local32percent expansion +6.5percent anchored push','collapse_events_local':events,'cyclops_reveal_local':[27,50],'sources':'v80 selected footage; durations unchanged'},indent=2))
