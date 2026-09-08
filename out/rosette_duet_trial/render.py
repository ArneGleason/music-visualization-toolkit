"""Two phrase-isolated rosettes with peripheral swooping approach paths."""
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'out/astronaut_reply_v1/guide.wav'),'-af','highpass=f=80,lowpass=f=1500,aresample=8000','-f','f32le','-'])
audio=np.frombuffer(raw,dtype='<f4');norm=max(np.quantile(np.abs(audio),.95),.001)
phase=np.arange(256)/256;angle=np.linspace(0,2*np.pi,768,endpoint=False)
def smooth(t):
 t=np.clip(t,0,1);return t*t*(3-2*t)
class Sprite:
 def __init__(self,start,end,side,color):
  self.start,self.end,self.side,self.color=start,end,side,np.array(color)
  self.period=40.;self.radial=np.full(256,12.);self.level=.3
  self.trail=np.zeros((720,1280),np.float32)
  self.signal=np.zeros_like(audio)
  a=round((start-899)/24*8000);b=round((end-899)/24*8000)
  self.signal[a:b]=audio[a:b] # No lookahead or cross-talk from the other phrase.
 def render(self,songframe):
  t=(songframe-self.start)/24
  if t<0:return np.zeros((720,1280,3),np.float32),None
  active=songframe<self.end
  if active:
   i=round((songframe-899)/24*8000);chunk=self.signal[i-512:i+512].astype(float);chunk-=chunk.mean()
   amplitude=float(np.sqrt(np.mean(chunk**2)))
   corr=np.correlate(chunk,chunk,'full')[len(chunk)-1:]
   candidates=np.arange(22,90);scores=corr[candidates]/(len(chunk)-candidates)
   peaks=np.flatnonzero((scores[1:-1]>scores[:-2])&(scores[1:-1]>=scores[2:]))+1
   if len(peaks) and amplitude>.002:
    self.period=.85*self.period+.15*candidates[peaks[np.argmax(scores[peaks])]]
   lo=max(1,i-int(self.period));hi=min(len(audio)-1,i+int(self.period))
   crossings=np.flatnonzero((self.signal[lo-1:hi-1]<=0)&(self.signal[lo:hi]>0))+lo
   origin=crossings[np.argmin(abs(crossings-i))] if len(crossings) else i
   folded=sum(np.interp(origin+(phase+k)*self.period,np.arange(len(audio)),self.signal) for k in [-1,0,1])/(3*norm)
   radial=12+28*np.tanh(np.abs(folded)*1.65)
   self.radial=(radial+np.roll(radial,1)+np.roll(radial,-1))/3
   self.level=.45+.75*min(1,amplitude/norm)
  # Apparent approach from distant small halo to broad foreground loop.
  approach=smooth(t/.82)
  scale=.18+3.4*approach
  sweep=t*4.1
  x=220*(1-approach)+(100+142*np.cos(sweep))*approach
  y=275+approach*(130*np.sin(sweep)-30)
  if self.side==1:x=1280-x;y=400-125*np.sin(sweep+.25)*approach
  # Peripheral paths allow frame-edge clipping, never transit across her face.
  radius=np.tile(self.radial,3)*scale
  yaw=.63+.18*np.cos(t*2.8)
  local=np.stack([np.cos(angle+t*.8)*radius,np.sin(angle+t*.8)*radius*yaw],axis=1)
  tilt=.45*np.sin(t*2.2)*(1 if self.side==0 else -1)
  rotation=np.array([[np.cos(tilt),-np.sin(tilt)],[np.sin(tilt),np.cos(tilt)]])
  xy=local@rotation.T+np.array([x,y])
  energy=np.zeros((720,1280),np.float32)
  level=self.level*smooth(t/.12)
  if not active:level*=.78 # Retains captured first-phrase shape/energy, no second-phrase driver.
  for j in range(768):
   q=(j+1)%768;distance=np.linalg.norm(xy[q]-xy[j]);dwell=1/(1+distance*.17)
   weight=(.75+.25*((j/768-t*.55)%1))*level*dwell
   cv2.line(energy,tuple(np.rint(xy[j]).astype(int)),tuple(np.rint(xy[q]).astype(int)),float(weight),max(1,round(scale*.6)),cv2.LINE_AA)
  energy=cv2.GaussianBlur(energy,(0,0),.7)
  self.trail=self.trail*.55+energy*.60
  light=self.trail*1.5+cv2.GaussianBlur(self.trail,(0,0),3)*1.8+cv2.GaussianBlur(self.trail,(0,0),11)*2.5
  # Gentle safety falloff before central performance, including diffuse bloom.
  xx=np.arange(1280)
  guard=1-smooth((xx-345)/35) if self.side==0 else smooth((xx-900)/35)
  light*=guard[None,:]
  return light[:,:,None]*self.color,{'center':[x,y],'scale':scale,'active_voice':active,'level':float(level)}
sprites=[Sprite(1030,1060,0,[1.,.80,.20]),Sprite(1060,1082,1,[.10,.50,1.])]
cap=cv2.VideoCapture(str(ROOT/'out/rosette_sprite_trial/raw.mp4'))
assert cap.get(cv2.CAP_PROP_FPS)==24
(OUT/'frames').mkdir(exist_ok=True);records=[]
for f in range(111):
 ok,frame=cap.read();assert ok
 accumulation=np.zeros_like(frame,dtype=np.float32);states=[]
 for sub in range(2):
  light=np.zeros_like(frame,dtype=np.float32)
  for sprite in sprites:
   glow,state=sprite.render(971+f+(sub+.5)/2);light+=glow
   if sub==1:states.append(state)
  accumulation+=np.clip(frame.astype(np.float32)/255+light,0,1)*.5
 cv2.imwrite(str(OUT/'frames'/f'{f:04d}.png'),np.rint(accumulation*255).astype(np.uint8))
 records.append({'song_frame':971+f,'sprites':states})
cap.release()
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(OUT/'frames/%04d.png'),'-i',str(ROOT/'audio/song.wav'),'-filter_complex',
 '[1:a]atrim=start=40.458333333333:end=45.083333333333,asetpts=PTS-STARTPTS[a]',
 '-map','0:v:0','-map','[a]','-frames:v','111','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',str(OUT/'preview.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview.mp4'),'-f','null','-'],check=True)
(OUT/'choreography.json').write_text(json.dumps({'cyan_voice_frames':[1030,1060],'amber_voice_frames':[1060,1082],
 'guide_origin':899,'method':'phrase-gated phase-folded vocal waveform, depth suggested by scaling/tilt/path; screen-space preview','frames':records},indent=2))
print('Two-rosette preview ready; separate phrase drivers, 111 frames.')
