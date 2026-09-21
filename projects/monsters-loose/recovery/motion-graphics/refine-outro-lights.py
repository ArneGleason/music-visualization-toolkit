import json,subprocess,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parent.parent;old=r/'motion-graphics/OUTRO-LIGHTS-001';o=r/'motion-graphics/OUTRO-LIGHTS-002';o.mkdir(exist_ok=True)
shots=json.loads((old/'original-shots.json').read_text())
specs={'SCN-014-BEYOND-FENCE':(.75,[(2.5,3),(2,3),(2.5,3),(2,3),(3,4)]),'SCN-015-FINALE':(1/3,[(2.8,3.1)]*7)}
for s in shots:
 name=s['id']
 if name not in specs:continue
 scale,radii=specs[name];tracks=json.loads((old/(name+'-tracks.json')).read_text())
 src=r/s['source'] if name!='SCN-015-FINALE' else r/'motion-graphics/OUTRO-003/FINALE-timed-v003.mp4'
 n=s['end_frame_exclusive']-s['start_frame'];w,h=1920,1080
 reader=subprocess.Popen(['ffmpeg','-v','error','-i',str(src),'-vf','scale=1920:1080','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 dest=o/(name+'-beacons-v002.mp4')
 writer=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-an','-c:v','libx264','-crf','17','-preset','fast',str(dest)],stdin=subprocess.PIPE)
 samples=[]
 for f in range(n):
  raw=reader.stdout.read(w*h*3);assert len(raw)==w*h*3;im=np.frombuffer(raw,np.uint8).reshape(h,w,3).copy()
  for i,(cx,cy,pulse) in enumerate(tracks[f]):
   x,y=cx*2,cy*2;rx,ry=radii[i];radius=int(max(rx,ry)*10+10)
   x0=max(0,int(x)-radius);x1=min(w,int(x)+radius+1);y0=max(0,int(y)-radius);y1=min(h,int(y)+radius+1)
   a=im[y0:y1,x0:x1].astype(float);yy,xx=np.mgrid[y0:y1,x0:x1]
   oldcore=np.exp(-.5*(((xx-x)/(rx*2))**2+((yy-y)/(ry*2))**2))
   wide=np.exp(-.5*(((xx-x)/(rx*5.8))**2+((yy-y)/(ry*5.8))**2))
   redconf=np.clip((a[:,:,0]-np.maximum(a[:,:,1],a[:,:,2])-5)/45,0,1)
   bg=np.median(np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]),axis=0)
   # Suppress the original baked red bloom at its OLD radius, then recreate a smaller lamp.
   # Shrinking only an additive overlay would leave the old oversized glow underneath.
   # Subtract the red illumination while retaining the original roof/sky texture.
   # A flat background replacement creates visible grey patches around distant towers.
   excess=np.maximum(0,a[:,:,0]-np.maximum(a[:,:,1],a[:,:,2]))
   illumination=excess*wide**.45/0.77
   base=np.maximum(0,a-illumination[:,:,None]*np.array([1,.23,.17]))
   base*=1-(oldcore*.7)[:,:,None]
   core=np.exp(-.5*(((xx-x)/(rx*2*scale))**2+((yy-y)/(ry*2*scale))**2))
   halo=np.exp(-.5*(((xx-x)/(rx*3.3*scale))**2+((yy-y)/(ry*3.3*scale))**2))
   hot=np.exp(-.5*(((xx-x)/(rx*.65*scale))**2+((yy-y)/(ry*.65*scale))**2))
   power=.70 if name=='SCN-015-FINALE' else .9
   glow=(np.array([220,23,9])*core[:,:,None]+np.array([60,3,1])*halo[:,:,None]+np.array([90,42,24])*hot[:,:,None])*(.025+.975*pulse)*power
   im[y0:y1,x0:x1]=np.clip(base+glow,0,255).astype(np.uint8)
  writer.stdin.write(im.tobytes())
  if f in [0,n//4,n//2,3*n//4,n-1]:samples.append((f,Image.fromarray(im).resize((480,270))))
 writer.stdin.close();assert writer.wait()==0;reader.stdout.close();assert reader.wait()==0
 sheet=Image.new('RGB',(1440,580),(20,20,20));d=ImageDraw.Draw(sheet)
 for i,(f,im) in enumerate(samples):x=i%3*480;y=i//3*290;sheet.paste(im,(x,y));d.text((x+3,y+273),name+' frame'+str(f),fill='white')
 sheet.save(o/(name+'-review.jpg'))
 print(name,'radius scale',scale,'frames',n,flush=True)
(o/'settings.json').write_text(json.dumps(dict(finale_radius_scale=1/3,finale_intensity=.70,swamp_entry_radius_scale=.75,swamp_entry_intensity=.9,method='Suppress original baked bloom at previous radius before adding tighter core and halo; retain tracked29frame blink cadence.'),indent=2)+'\n')
