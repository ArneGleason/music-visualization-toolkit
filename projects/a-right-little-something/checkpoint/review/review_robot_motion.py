from pathlib import Path
import sys
from PIL import Image,ImageDraw

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,probe,run,save

base=Path('projects/a-right-little-something').resolve()
plan=load(base/'kling-lab-robot-cutaway-v01.json')
take=plan['shots'][0]
task=base/plan['output']/take['id']
source=next(task.glob('*-clean.mp4'))
info=probe(source)
count=int(info['nb_frames'])
assert count>=122 and info['height']==1080 and info['r_frame_rate']=='24/1'
out=base/'generated/storyboard/lab-robot-motion-v01'
out.mkdir(parents=True,exist_ok=True)
frames=[1,25,50,75,100,count]
select='+'.join(f'eq(n\\,{n-1})' for n in frames)
run(['-i',str(source),'-vf',f'select={select},scale=640:360','-fps_mode','passthrough',str(out/'source-%02d.png')])
sheet=Image.new('RGB',(1920,784),'#111111')
draw=ImageDraw.Draw(sheet)
for i,n in enumerate(frames):
    x,y=(i%3)*640,(i//3)*392
    sheet.paste(Image.open(out/f'source-{i+1:02d}.png').convert('RGB'),(x,y))
    draw.text((x+8,y+365),f'Native source {n}',fill='white')
sheet.save(out/'source-proof.png')
body=load(task/'submission.json')['body']
save(out/'source.json',dict(id=take['id'],shotId=take['shotId'],motionRef=source.relative_to(base).as_posix(),
    sourceFrames=count,nativeWidth=info['width'],fps=24,credits=body['creditsConsumed'],generationId=body['generationId']))
print('Native robot source ready for visual review:',count,'frames')
