import subprocess,json
from pathlib import Path
import numpy as np
o=Path(__file__).resolve().parent;r=o.parent.parent
src=r/'video-tests/KLING-SIGN-002/KLING-SIGN-002-lipsync-24fps.mp4'
w,h=1916,1080
reader=subprocess.Popen(['ffmpeg','-v','error','-i',str(src),'-vf','scale=1916:1080,setsar=1,tpad=stop_mode=clone:stop_duration=0.05','-frames:v','144','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
writer=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1916x1080','-r','24','-i','-','-an','-c:v','libx264','-crf','17','-preset','fast',str(o/'Harper-take2-eye-v001.mp4')],stdin=subprocess.PIPE)
for f in range(144):
 data=reader.stdout.read(w*h*3)
 if len(data)!=w*h*3:raise RuntimeError('Incomplete source frame')
 im=np.frombuffer(data,dtype=np.uint8).reshape(h,w,3).copy()
 if f>=100:
  u=min(1,(f-100)/14);u=u*u*(3-2*u)
  cx=1595-5*(f-100)/44;cy=312+2*np.sin((f-100)/25)
  x0,y0=1530,260;patch=im[y0:y0+110,x0:x0+130].astype(float)/255
  yy,xx=np.mgrid[y0:y0+110,x0:x0+130];dx=xx-cx;dy=yy-cy
  # Almond opening, restrained red bloom. Original illuminated wires occlude the light.
  height=.35+5.3*u;limit=height*np.maximum(0,1-(dx/15)**2)**.65
  almond=np.clip((limit-np.abs(dy))*2,0,1)*(np.abs(dx)<15)
  slit=np.exp(-(dx/1.3)**4);core=almond*(1-.87*slit)*u
  glow=np.exp(-((dx/23)**2+(dy/15)**2)*1.6)*.28*u
  lum=patch.max(axis=2);occlusion=1-np.clip((lum-.13)/.15,0,1)
  light=(core*.95+glow)*occlusion
  col=np.stack([light,core*.085*occlusion,core*.035*occlusion],axis=2)
  patch=1-(1-patch)*(1-np.clip(col,0,1));im[y0:y0+110,x0:x0+130]=np.clip(patch*255,0,255).astype(np.uint8)
 writer.stdin.write(im.tobytes())
reader.stdout.close();reader.wait();writer.stdin.close()
if writer.wait():raise RuntimeError('Encoder failed')
# Existing first shot and Arctic title are retained verbatim in timing/content.
vf="[0:v]trim=start_frame=0:end_frame=92,setpts=PTS-STARTPTS[a];[1:v][2:v]overlay=0:0:shortest=1,trim=start_frame=92:end_frame=144,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]"
subprocess.run(['ffmpeg','-y','-v','error','-i',str(o/'Harper-arctic-cutaway-v001.mp4'),'-i',str(o/'Harper-take2-eye-v001.mp4'),'-framerate','24','-i',str(r/'motion-graphics/HARPER-SPEECH-001/frames-v004-fade/bubble-%04d.png'),'-filter_complex',vf,'-map','[v]','-map','0:a','-c:v','libx264','-crf','17','-preset','fast','-c:a','copy','-movflags','+faststart',str(o/'Harper-arctic-cutaway-v002.mp4')],check=True)
