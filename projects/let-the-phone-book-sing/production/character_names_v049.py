"""Two native character-name trials, surname first in sound, first-last in print."""
import json
import subprocess
from effectcraft_session import Session,BASE,CLI
OUT=BASE/'generated/effectcraft-edit-v049';OUT.mkdir(parents=True,exist_ok=True)
TARGET=OUT/'Let-the-Phone-Book-Sing-editable-v049.ecproj'
if TARGET.exists():raise SystemExit('Preserve existing v049')
# Attacks from the existing compiled lyric timing; never alter shot boundaries.
NAMES=[
 dict(first='APRIL',last='BLOOM',firstFrame=582,lastFrame=571,firstPosition=[1250,915],lastPosition=[1650,915],corner='lower right'),
 dict(first='MAY',last='BLOOM',firstFrame=712,lastFrame=695,firstPosition=[170,125],lastPosition=[510,125],corner='upper left'),
 dict(first='PENNY',last='CASH',firstFrame=1113,lastFrame=1096,firstPosition=[1390,125],lastPosition=[1750,125],corner='upper right'),
 dict(first='RICH',last='CASH',firstFrame=1246,lastFrame=1230,firstPosition=[180,900],lastPosition=[500,900],corner='lower left'),
 dict(first='MILES',last='CHASE',firstFrame=1363,lastFrame=1355,firstPosition=[1250,915],lastPosition=[1660,915],corner='lower right'),
 dict(first='PENNY',last='CHASE',firstFrame=1505,lastFrame=1488,firstPosition=[230,125],lastPosition=[640,125],corner='upper left'),
 dict(first='FORREST',last='PINE',firstFrame=1915,lastFrame=1898,firstPosition=[280,915],lastPosition=[665,915],corner='lower left'),
]
for name in NAMES:
 name.update(fadeStart=name['firstFrame']+27,end=name['firstFrame']+35)

s=Session(BASE/'generated/effectcraft-edit-v048/Let-the-Phone-Book-Sing-editable-v048.ecproj')
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
 for frame in [590,720,1121,1254,1371,1513,1923]:s.call('render_frame',{'comp':1554,'time':frame/24,'path':str(OUT/f'check-{frame}.png'),'inline':False,'max_side':1920})
finally:s.close()
for filename,start,end in [('animatic-through-pine-price-1080p.mp4',0,2451/24)]:
 subprocess.run([str(CLI),'render','--project',str(TARGET),'--gpu','--comp','1554','--start',str(start),'--end',str(end),'--out',str(OUT/filename),'--format','h264','--bitrate','10000','--audio','on'],check=True)
(BASE/'production/character-names-v003.json').write_text(json.dumps({'status':'pending_user_review','names':NAMES,'nativeProject':str(TARGET.relative_to(BASE)),'font':'Arial Bold Italic','size':88,'style':'Echo palette with dark ink stroke; surname appears in its final position, first name fills reserved space at left. Brief hold and eight-frame fade. Existing echoes untouched.','timingSource':'generated/timeline.compiled.json, line-005/006/011/012/013/014/019 word startFrame'},indent=2)+'\n')
