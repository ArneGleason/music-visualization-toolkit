import json,subprocess,math,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parent.parent;o=r/'motion-graphics/OUTRO-LIGHTS-001'
shots=json.loads((o/'original-shots.json').read_text())
# Coordinates in960x540 reference space. Each anchor follows a confirmed architectural beacon, never a character.
anchors={
 'SCN-012-ESCAPE-SHOW':[(697,116,6,8),(936,57,8,9)],
 'SCN-014-BEYOND-FENCE':[(403,83,2.5,3),(508,40,2,3),(750,86,2.5,3),(850,82,2,3),(935,121,3,4)],
 'SCN-014-CEO':[(728,205,7,9),(949,113,8,10)],
 'SCN-014-PLAY':[(414,157,2.5,3),(472,183,2.5,3)],
 'SCN-014-INSPECTOR':[(708,124,7,9),(940,66,8,10)],
 'SCN-014-HARPER-KID':[(252,71,3.5,4)],
}
if (o/'finale-anchors.json').exists():anchors['SCN-015-FINALE']=json.loads((o/'finale-anchors.json').read_text())
for s in shots:
 name=s['id']
 if name not in anchors or (len(sys.argv)>1 and name not in sys.argv[1:]):continue
 source=r/s['source']
 if name=='SCN-015-FINALE':source=r/'motion-graphics/OUTRO-003/FINALE-timed-v003.mp4'
 n=s['end_frame_exclusive']-s['start_frame'];w=1920;h=1080
 reader=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
 dest=o/(name+'-beacons-v001.mp4')
 writer=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','24','-i','-','-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',str(dest)],stdin=subprocess.PIPE)
 positions=[[a[0]*2,a[1]*2] for a in anchors[name]];tracks=[];samples=[]
 for f in range(n):
  raw=reader.stdout.read(w*h*3)
  if len(raw)!=w*h*3:raise RuntimeError((name,f,'short source'))
  im=np.frombuffer(raw,np.uint8).reshape(h,w,3).copy();row=[]
  for i,(ax,ay,rx,ry,*rest) in enumerate(anchors[name]):
   x,y=positions[i]
   # Track red source in a tight local search. Final distant lamps have explicitly measured camera tracks.
   if rest:
    keys=rest[0];x=np.interp(f,[k[0] for k in keys],[k[1]*2 for k in keys]);y=np.interp(f,[k[0] for k in keys],[k[2]*2 for k in keys])
   search=max(8,int(rx*2+3));x0=max(0,int(x)-search);x1=min(w,int(x)+search+1);y0=max(0,int(y)-search);y1=min(h,int(y)+search+1)
   patch=im[y0:y1,x0:x1].astype(float);yy,xx=np.mgrid[y0:y1,x0:x1]
   redness=np.maximum(0,patch[:,:,0]-np.maximum(patch[:,:,1],patch[:,:,2])-30)
   weights=redness**2*np.exp(-((xx-x)**2+(yy-y)**2)/(2*max(4,rx*1.5)**2))
   if weights.sum()>300:
    nx=(weights*xx).sum()/weights.sum();ny=(weights*yy).sum()/weights.sum()
    x=.7*x+.3*nx;y=.7*y+.3*ny
   positions[i]=[x,y]
   radius=int(max(rx,ry)*7+8);x0=max(0,int(x)-radius);x1=min(w,int(x)+radius+1);y0=max(0,int(y)-radius);y1=min(h,int(y)+radius+1)
   patch=im[y0:y1,x0:x1].astype(float);yy,xx=np.mgrid[y0:y1,x0:x1]
   core=np.exp(-.5*(((xx-x)/(rx*2))**2+((yy-y)/(ry*2))**2))
   halo=np.exp(-.5*(((xx-x)/(rx*3.8))**2+((yy-y)/(ry*3.8))**2))
   #29frame established aviation cadence, staggered lamps, continuous master clock.
   phase=(s['start_frame']+f-7-i*4+14.5)%29-14.5;p=math.exp(-.5*(phase/3.4)**2)
   redconf=np.clip((patch[:,:,0]-np.maximum(patch[:,:,1],patch[:,:,2])-8)/55,0,1)
   mute=np.maximum(core*.91,halo*redconf*.96)*(1-p)
   bg=np.median(np.concatenate([patch[0],patch[-1],patch[:,0],patch[:,-1]]),axis=0)
   # Keep faint lamp glass and architecture in off state; no opaque circular cutout.
   result=patch*(1-mute[:,:,None])+bg*mute[:,:,None]
   boost=(np.array([130,12,3])[None,None,:]*halo[:,:,None]+np.array([85,25,10])[None,None,:]*core[:,:,None])*p*(.4 if name=='SCN-015-FINALE' else 1)
   im[y0:y1,x0:x1]=np.clip(result+boost,0,255).astype(np.uint8)
   row.append([round(x/2,2),round(y/2,2),round(p,4)])
  writer.stdin.write(im.tobytes());tracks.append(row)
  if f in [0,n//4,n//2,3*n//4,n-1]:samples.append((f,Image.fromarray(im).resize((480,270))))
 writer.stdin.close();assert writer.wait()==0;reader.stdout.close();assert reader.wait()==0
 (o/(name+'-tracks.json')).write_text(json.dumps(tracks))
 sheet=Image.new('RGB',(1440,580),(20,20,20));draw=ImageDraw.Draw(sheet)
 for j,(f,im) in enumerate(samples):x=j%3*480;y=j//3*290;sheet.paste(im,(x,y));draw.text((x+4,y+274),name+' '+str(f),fill='white')
 sheet.save(o/(name+'-review.jpg'))
 print(name,'done',n,'frames',flush=True)
