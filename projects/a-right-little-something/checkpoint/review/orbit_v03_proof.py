from pathlib import Path
import json, math, subprocess
from PIL import Image, ImageDraw

base=Path('projects/a-right-little-something').resolve()
plan=json.loads((base/'orbit-blender-v03.json').read_text())
out=base/plan['output']/'hybrid'
route=json.loads((out/'trajectory.json').read_text())
source=base/plan['source']
for frame in (25,46,80,105,145,162):
    target=out/f'plate-{frame:04}.png'
    subprocess.run(['ffmpeg','-y','-v','error','-reinit_filter','0','-i',str(source),'-vf',f'select=eq(n\\,{frame-1}),pad=1920:1080:(ow-iw)/2:(oh-ih)/2','-frames:v','1',str(target)],check=True)
    from PIL import ImageChops
    plate=Image.open(target).convert('RGB')
    layer=Image.open(out/f'look-{frame:04}.png').convert('RGB')
    ImageChops.screen(plate,layer).save(out/f'composite-look-{frame:04}.png')
points=route['points']
project=lambda p:(960+p[0]*80,540-p[1]*80)
diagram=Image.open(out/'plate-0080.png').convert('RGB')
draw=ImageDraw.Draw(diagram)
draw.line([project(p) for p in points],fill=(255,205,125),width=4)
for i in range(20,len(points)-20,45):
    a,b=project(points[i]),project(points[i+2])
    dx,dy=b[0]-a[0],b[1]-a[1]
    length=math.hypot(dx,dy)
    dx,dy=dx/length,dy/length
    draw.line([(a[0]-dx*12-dy*6,a[1]-dy*12+dx*6),a,(a[0]-dx*12+dy*6,a[1]-dy*12-dx*6)],fill=(185,245,255),width=3)
draw.rectangle((15,15,970,85),fill=(10,15,30))
draw.text((30,30),'PATH STUDY: continuous loops, curvature-matched approaches; final trails decay',fill='white')
diagram.save(out/'trajectory-study.png')
sheet=Image.new('RGB',(1280,1080),(8,12,24))
for i,frame in enumerate((25,46,80,105,145,162)):
    picture=Image.open(out/f'composite-look-{frame:04}.png').resize((640,360))
    sheet.paste(picture,((i%2)*640,(i//2)*360))
    ImageDraw.Draw(sheet).text(((i%2)*640+12,(i//2)*360+12),f'Source frame {frame}',fill='white')
sheet.save(out/'motion-proof.png')
print('Path and six composite proof frames ready')
