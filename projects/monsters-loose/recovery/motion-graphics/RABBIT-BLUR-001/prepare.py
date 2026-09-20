from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,math,bisect
o=Path(__file__).resolve().parent
# Hand-followed rabbit body/wing envelope; local frame0 = master2302.
keys=[(5,510,410,145,120),(9,600,465,145,115),(12,655,510,145,115),(15,725,525,140,110),(18,720,515,140,110),(21,690,535,120,120),(24,650,510,145,125),(27,605,485,130,110),(30,535,485,135,110),(33,480,455,120,115),(36,435,430,115,110),(40,360,430,95,95)]
(o/'masks').mkdir(exist_ok=True);(o/'protect').mkdir(exist_ok=True);records=[]
for f in range(76):
 j=min(len(keys)-2,max(0,bisect.bisect_right([k[0] for k in keys],f)-1));a,b=keys[j:j+2];t=max(0,min(1,(f-a[0])/(b[0]-a[0])));cx,cy,rx,ry=[a[i]+(b[i]-a[i])*t for i in range(1,5)]
 gain=max(0,min(1,(f-5)/4,(40-f)/6))*.72
 mask=Image.new('L',(1280,720));dr=ImageDraw.Draw(mask);dr.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=round(255*gain));mask=mask.filter(ImageFilter.GaussianBlur(12))
 # Generous head/ear/teeth exclusion; rabbit partly behind head stays untouched.
 protect=Image.new('L',(1280,720));ImageDraw.Draw(protect).ellipse((535,125,830,465),fill=255);protect=protect.filter(ImageFilter.GaussianBlur(5));mask=ImageChops.multiply(mask,ImageChops.invert(protect))
 mask.save(o/f'masks/mask-{f+1:04d}.png');protect.save(o/f'protect/head-{f+1:04d}.png')
 vx=(b[1]-a[1])/(b[0]-a[0]);vy=(b[2]-a[2])/(b[0]-a[0]);angle=math.atan2(-vy,vx);pixels=min(24,max(12,math.hypot(vx,vy)*1.4))
 records.append(dict(local_frame=f,master_frame=2302+f,center=[cx,cy],radius=[rx,ry],mix=gain,angle=angle,blur_pixels=pixels))
(o/'tracking.json').write_text(json.dumps(records,indent=2))
