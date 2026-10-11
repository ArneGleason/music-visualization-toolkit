from pathlib import Path
import json, math
from PIL import Image, ImageDraw

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/orbit-blender-v03/hybrid'
data=json.loads((out/'trajectory.json').read_text(encoding='utf-8'))
image=Image.new('RGB',(1400,520),(12,18,31))
draw=ImageDraw.Draw(image)
draw.text((35,22),'ORBIT SPEED AND TRAIL RESPONSE / v25',fill='white')
draw.text((35,46),'Relative speeds follow distance on each eccentric loop; transfer timing is authored to fit the song.',fill=(180,200,225))
left,top,right,bottom=65,95,770,405
for value in (.6,.8,1,1.2,1.4):
    y=bottom-(value-.5)/1*(bottom-top)
    draw.line((left,y,right,y),fill=(42,52,69))
    draw.text((20,y-6),str(value),fill=(175,195,220))
draw.line([(left+t*(right-left),bottom-(v-.5)*(bottom-top)) for t,v in zip(data['passageTimes'],data['relativeSpeeds'])],fill=(105,225,255),width=3)
for frame in (25,49,73,97,121,133):
    x=left+(frame-25)/108*(right-left)
    draw.text((x-10,420),str(frame),fill=(175,195,220))
draw.text((left,448),'Source frame / 24 fps / speed rises near each closest pass',fill='white')
draw.text((left,475),'Peak / slow speed ratio: %.2fx'%(max(data['relativeSpeeds'])/min(data['relativeSpeeds'])),fill=(105,225,255))
left,top,right,bottom=880,95,1360,405
for value in (0,.25,.5,.75,1):
    y=bottom-value*(bottom-top)
    draw.line((left,y,right,y),fill=(42,52,69))
    draw.text((840,y-6),str(value),fill=(175,195,220))
def decay(age): return (.92*math.exp(-age/2)+.08*math.exp(-age/12))*max(0,1-age/48)
draw.line([(left+age/48*(right-left),bottom-decay(age)*(bottom-top)) for age in [i/4 for i in range(193)]],fill=(255,205,110),width=3)
for age in (0,6,12,24,36,48):
    x=left+age/48*(right-left)
    draw.text((x-8,420),str(age),fill=(175,195,220))
draw.text((left,448),'Trail age in frames / short bright wake, long faint tail',fill='white')
draw.text((left,475),'5 frames: %.1f%%   24 frames: %.2f%%'%(decay(5)*100,decay(24)*100),fill=(255,205,110))
image.save(out/'speed-profile.png')
print('Speed and trail profile diagram ready')
