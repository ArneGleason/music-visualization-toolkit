import json,subprocess,io
import numpy as np
from scipy.ndimage import label,center_of_mass
from PIL import Image,ImageDraw
from pathlib import Path
r=Path(__file__).resolve().parent.parent;o=r/'motion-graphics/OUTRO-LIGHTS-001';o.mkdir(exist_ok=True)
shots=[s for s in json.loads((r/'shots/shotlist.json').read_text())['shots'] if s['start_frame']>=3883]
(o/'original-shots.json').write_text(json.dumps(shots,indent=2))
for s in shots:
 sheet=Image.new('RGB',(1440,290));points=[]
 for i,f in enumerate([0,(s['end_frame_exclusive']-s['start_frame'])//2,s['end_frame_exclusive']-s['start_frame']-1]):
  raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/24),'-i',str(r/s['source']),'-frames:v','1','-vf','scale=960:540','-f','image2pipe','-vcodec','png','-threads','1','-'])
  im=Image.open(io.BytesIO(raw)).convert('RGB');a=np.array(im).astype(float);mask=(a[:,:,0]>155)&(a[:,:,0]>2.8*a[:,:,1])&(a[:,:,0]>2.8*a[:,:,2])
  lab,n=label(mask);d=ImageDraw.Draw(im);ps=[]
  for k in range(1,n+1):
   yy,xx=np.where(lab==k)
   if len(xx)<2 or len(xx)>220:continue
   x=float(xx.mean());y=float(yy.mean())
   if y>400:continue
   ps.append([round(x,1),round(y,1),len(xx)])
   d.ellipse((x-8,y-8,x+8,y+8),outline='cyan',width=2);d.text((x+8,y-9),str(len(ps)-1),fill='white')
  sheet.paste(im.resize((480,270)),(480*i,0));ImageDraw.Draw(sheet).text((480*i+4,273),s['id']+' f'+str(f),fill='white');points.append(ps)
 sheet.save(o/(s['id']+'-audit.jpg'));(o/(s['id']+'-points.json')).write_text(json.dumps(points))
 print(s['id'],[len(x) for x in points],flush=True)
