"""Two native character-name trials, surname first in sound, first-last in print."""
import json
import subprocess
from effectcraft_session import Session,BASE,CLI
OUT=BASE/'generated/effectcraft-edit-v047';OUT.mkdir(parents=True,exist_ok=True)
TARGET=OUT/'Let-the-Phone-Book-Sing-editable-v047.ecproj'
if TARGET.exists():raise SystemExit('Preserve existing v047')
# Attacks from the existing compiled lyric timing; never alter shot boundaries.
NAMES=[dict(first='BELLE',last='BELL',firstFrame=305,lastFrame=296,firstPosition=[210,915],lastPosition=[465,915],fadeStart=332,end=340,corner='lower left'),
       dict(first='LIBERTY',last='BELL',firstFrame=446,lastFrame=437,firstPosition=[1370,125],lastPosition=[1745,125],fadeStart=473,end=481,corner='upper right')]
s=Session(BASE/'generated/effectcraft-edit-v046/Let-the-Phone-Book-Sing-editable-v046.ecproj')
try:
 s.command('comp.open',{'comp':675})
 for name in NAMES:
  name['layers']=[]
  for part in ['last','first']:
   f=name[part+'Frame'];position=name[part+'Position']
   lid=s.command('layer.newText',{'name':f"NAME — {name['first']} {name['last']} / {part}",'text':name[part],'font':'Arial Bold Italic','size':88,'fill':'#9dd8cf' if part=='first' else '#f7dda2','position':position,'justify':'center'})['layer'];name['layers'].append(lid)
   s.command('layer.style.stroke',{'layers':[lid]})
   s.call('set_property',{'layer':lid,'path':'layerStyles/stroke/color','value':'#292536'})
   s.call('set_property',{'layer':lid,'path':'layerStyles/stroke/size','value':5})
   s.command('layer.timing',{'layers':[lid],'out':name['end']/24})
   s.command('layer.timing',{'layers':[lid],'in':f/24})
   s.call('add_keyframe',{'layer':lid,'path':'transform/opacity','keys':[{'time':a/24,'value':v} for a,v in [(f,0),(f+2,100),(name['fadeStart'],100),(name['end'],0)]],'interpolation':'linear'})
 s.command('comp.open',{'comp':1554});s.call('save_project',{'path':str(TARGET)})
 for frame in [300,312,442,453]:s.call('render_frame',{'comp':1554,'time':frame/24,'path':str(OUT/f'check-{frame}.png'),'inline':False,'max_side':1920})
finally:s.close()
for filename,start,end in [('character-names-review.mp4',290/24,565/24),('animatic-through-pine-price-1080p.mp4',0,2451/24)]:
 subprocess.run([str(CLI),'render','--project',str(TARGET),'--gpu','--comp','1554','--start',str(start),'--end',str(end),'--out',str(OUT/filename),'--format','h264','--bitrate','10000','--audio','on'],check=True)
(BASE/'production/character-names-v001.json').write_text(json.dumps({'status':'pending_user_review','names':NAMES,'nativeProject':str(TARGET.relative_to(BASE)),'font':'Arial Bold Italic','size':88,'style':'Echo palette with dark ink stroke; surname appears in its final position, first name fills reserved space at left. Brief hold and eight-frame fade. Existing echoes untouched.','timingSource':'generated/timeline.compiled.json, line-003 and line-004 word startFrame'},indent=2)+'\n')
