from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,bisect
o=Path(__file__).resolve().parent;(o/'masks').mkdir(exist_ok=True);records=[]
keys=[(0,417,268),(12,420,282),(20,424,280),(29,427,265),(36,430,254),(55,435,254)]
for f in range(56):
 j=min(len(keys)-2,max(0,bisect.bisect_right([k[0] for k in keys],f)-1));a,b=keys[j:j+2];t=(f-a[0])/(b[0]-a[0]);cx=a[1]+t*(b[1]-a[1]);cy=a[2]+t*(b[2]-a[2]);gain=max(0,min(1,(f-16)/5));records.append(dict(local_frame=f,master_frame=2036+f,mouth=[cx,cy],gain=gain))
 mask=Image.new('L',(1280,720));d=ImageDraw.Draw(mask)
 if gain>0:d.ellipse((cx+7,cy-90,cx+173,cy+90),fill=255)
 mask=mask.filter(ImageFilter.GaussianBlur(5));d=ImageDraw.Draw(mask);d.rectangle((446,0,484,719),fill=0);d.rectangle((540,0,564,719),fill=0);mask.save(o/f'masks/mask-{f+1:04d}.png')
(o/'tracking.json').write_text(json.dumps(records,indent=2))
