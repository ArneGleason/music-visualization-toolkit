from pathlib import Path
import sys
from PIL import Image,ImageDraw

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,probe,run,save

base=Path('projects/a-right-little-something').resolve()
plan=load(base/'kling-lab-silver-motion-v01.json')
out=base/'generated/storyboard/lab-silver-motion-v01'
out.mkdir(parents=True,exist_ok=True)
frames=[1,25,50,75,100,145]
sheet=Image.new('RGB',(2160,5*240),'#111111')
draw=ImageDraw.Draw(sheet)
records=[]
for row,shot in enumerate(plan['shots']):
    task=base/plan['output']/shot['id']
    source=next(task.glob('*-clean.mp4'),None)
    if source is None:
        continue
    info=probe(source)
    assert (int(info['nb_frames']),info['height'],info['r_frame_rate'])==(145,1080,'24/1')
    select='+'.join(f'eq(n\\,{n-1})' for n in frames)
    run(['-i',str(source),'-vf',f'select={select},scale=360:203','-fps_mode','passthrough',str(task/'qa-%02d.png')])
    for col,n in enumerate(frames):
        sheet.paste(Image.open(task/f'qa-{col+1:02d}.png').convert('RGB'),(col*360,row*240))
        draw.text((col*360+8,row*240+208),shot['shotId']+f' · source{n}',fill='white')
    body=load(task/'submission.json')['body']
    records.append(dict(id=shot['id'],shotId=shot['shotId'],motionRef=source.relative_to(base).as_posix(),
        sourceFrames=145,nativeWidth=info['width'],fps=24,credits=body['creditsConsumed'],generationId=body['generationId']))
sheet.save(out/'source-proof.png')
save(out/'sources.json',records)
print(len(records),'silver native sources collected; visual continuity/motion review is next.')
