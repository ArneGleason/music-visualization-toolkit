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

def zoom_blur(im,amount,cx,cy):
 base=Image.fromarray(np.uint8(np.clip(im,0,255)));acc=np.zeros_like(im)
 samples=14
 for i in range(samples):
  t=i/(samples-1);z=1+amount*t
  sample=base.transform((W,H),Image.Transform.AFFINE,(1/z,0,cx*(1-1/z),0,1/z,cy*(1-1/z)),resample=Image.Resampling.BILINEAR)
  acc+=np.asarray(sample,dtype=np.float32)
 acc/=samples
 # Radial streaking follows image detail, keeping the face readable.
 radius=np.sqrt(((X-cx)/430)**2+((Y-cy)/360)**2)
 weight=.84*smooth(.12,.65,radius)
 return im*(1-weight[:,:,None])+acc*weight[:,:,None]

rng=np.random.default_rng(31)
events=[(28,640,100),(43,940,285),(56,1060,390),(67,400,390),(76,1030,560)]
particles=[]
for start,x,y in events:
 for j in range(22):particles.append((start+int(rng.integers(0,5)),x+rng.uniform(-45,45),y+rng.uniform(-18,18),rng.uniform(-5,5),rng.uniform(-4,.5),rng.uniform(40,85),rng.uniform(.30,.48)))
for name in (sys.argv[1:] or ['grow-a','grow-b']):
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
   weight=np.exp(-ell*ell*1.8);scale=1+.43*gain
   im=warp(im,-(X-cx)*(1-1/scale)*weight,-(Y-cy)*(1-1/scale)*weight)
   # Broad anchored push reinforces expansion without a hard moving matte.
   z=1+.11*gain;im=warp(im,(X-640)*(1/z-1),(Y-340)*(1/z-1))
   speed=float(smooth(3,24,f));im=zoom_blur(im,.16*speed,cx,cy-65)
  if name=='grow-b':
   dx=np.zeros((H,W),np.float32);dy=dx.copy()
   for start,cx,cy in events:
    age=f-start
    if age>=0:
     kick=math.exp(-age/7)*math.sin(age*2.3+1);mask=np.exp(-(((X-cx)/200)**4+((Y-cy)/170)**4));dx+=17*kick*mask;dy+=10*kick*mask
   # Brief whole-shot jolt joins stronger local steel recoil.
   pulse=sum(math.exp(-(f-e[0])/5)*math.sin((f-e[0])*2.1) for e in events if f>=e[0])
   im=warp(im,dx+3.5*pulse,dy+2*pulse)
   for start,cx,cy,vx,vy,r,alpha in particles:
    age=f-start
    if 0<=age<34:
     xx=cx+vx*age;yy=cy+vy*age+.105*age*age;rad=r*(.6+age*.075)
     a=np.exp(-(((X-xx)/rad)**2+((Y-yy)/(rad*.7))**2)*2)*alpha*min(1,(age+1)/3)*max(0,1-age/34)
     im=im*(1-a[:,:,None])+np.array([171,145,105],np.float32)*a[:,:,None]
   # Carry growth-speed blur through the cut, decaying before roof collapse.
   if f<27:im=zoom_blur(im,.16*(1-f/27),655,280)
   # Fine debris from beam-joint impacts, in gravity arcs.
   for start,cx,cy in events:
    age=f-start
    if 0<=age<24:
     for j in range(16):
      xx=int(cx+(j-7.5)*1.9*age);yy=int(cy-(j%3+1)*1.1*age+.35*age*age)
      if 2<xx<W-3 and 2<yy<H-5:im[yy:yy+7,xx:xx+3]=[166,147,113]
  if name=='smoke-b' and f>=27:
   q=float(smooth(29,50,f));sigma=18*(1-q)
   blurred=np.array(Image.fromarray(frame).filter(ImageFilter.GaussianBlur(sigma)),dtype=np.float32)
   cloud=np.array(Image.fromarray(frames[30]).filter(ImageFilter.GaussianBlur(9)),dtype=np.float32)
   cx,cy=890,330;mask=np.exp(-(((X-cx)/330)**4+((Y-cy)/400)**4))*smooth(470,650,X)
   hold=.78*(1-q)*float(smooth(27,32,f));mix=blurred*(1-hold)+cloud*hold
   im=im*(1-mask[:,:,None])+mix*mask[:,:,None]
  enc.stdin.write(np.uint8(np.clip(im,0,255)).tobytes())
 enc.stdin.close();assert enc.wait()==0;print(name,'complete',flush=True)
(O/'settings.json').write_text(json.dumps({'growth':'43percent soft expansion,11percent anchored push,16percent radial zoom blur','blur_carry_exterior_frames':27,'collapse':'17px horizontal/10px vertical localized recoil plus3.5px jolt;110 larger dust puffs and80 debris fragments','sources':'original approved takes; same36/91frames; roar and Cyclops untouched'},indent=2))
