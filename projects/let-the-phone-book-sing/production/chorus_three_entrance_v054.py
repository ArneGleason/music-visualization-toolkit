"""Advance Chorus3 picture entrance to the downbeat during opening ad-lib."""
import json
import subprocess
from effectcraft_session import Session, BASE, CLI
OUT=BASE/'generated/effectcraft-edit-v054'
OUT.mkdir(parents=True,exist_ok=True)
TARGET=OUT/'Let-the-Phone-Book-Sing-editable-v054.ecproj'
if TARGET.exists(): raise SystemExit('Preserve existing v054')
CUT=2415
s=Session(BASE/'generated/effectcraft-edit-v053/Let-the-Phone-Book-Sing-editable-v053.ecproj')
try:
 s.command('comp.open',{'comp':675})
 s.command('layer.timing',{'layers':[21524],'out':(CUT+2)/24})
 s.command('layer.timing',{'layers':[1157],'in':(CUT-2)/24})
 s.call('set_property',{'layer':1157,'path':'transform/opacity','expression':f'clamp((time*24-{CUT-3})/5,0,1)*100'})
 s.command('comp.open',{'comp':1554})
 s.call('save_project',{'path':str(TARGET)})
 for frame in [2413,2415,2417]:
  s.call('render_frame',{'comp':1554,'time':frame/24,'path':str(OUT/f'check-{frame}.png'),'inline':False,'max_side':1920})
finally:s.close()
subprocess.run([str(CLI),'render','--project',str(TARGET),'--gpu','--comp','1554','--start','0','--end',str(2843/24),'--out',str(OUT/'animatic-through-hope-wait-1080p.mp4'),'--format','h264','--bitrate','10000','--audio','on'],check=True)
