"""Replace Forrest's approved source, preserving the native edit and timing."""
import json
import subprocess
from effectcraft_session import Session, BASE, CLI

shot = next(x for x in json.loads((BASE/'shots/shotlist.json').read_text())['shots'] if x['id']=='PB-021')
start, end = shot['startFrame'], shot['endFrameExclusive']
out = BASE/'generated/effectcraft-edit-v043'
out.mkdir(parents=True, exist_ok=True)
target = out/'Let-the-Phone-Book-Sing-editable-v043.ecproj'
if target.exists():
    raise SystemExit('Preserve existing v043')
s = Session(BASE/'generated/effectcraft-edit-v042/Let-the-Phone-Book-Sing-editable-v042.ecproj')
try:
    s.command('comp.open', {'comp':675})
    item = s.command('file.import', {'paths':[str(BASE/'generated/kling-tests/forrest-pine-v002/kling-original-1080p.mp4')], 'sequence':False})['items'][0]
    s.command('layer.replaceSource', {'layer':20077, 'item':item})
    s.call('set_property', {'layer':20077, 'path':'timeRemap', 'expression':f'(time-{start}/24)+24/24'})
    s.command('layer.setSwitch', {'layers':[20077], 'switch':'audio', 'value':False})
    s.command('layer.rename', {'layer':20077, 'name':'PB-021 — Forrest Pine / corrected Clive and keypad / approved v002 / source24'})
    s.command('comp.open', {'comp':1554})
    s.call('save_project', {'path':str(target)})
    for frame in [1904,1960,2026]:
        s.call('render_frame', {'comp':1554,'time':frame/24,'path':str(out/f'check-{frame}.png'),'inline':False,'max_side':1920})
finally:
    s.close()
subprocess.run([str(CLI),'render','--project',str(target),'--gpu','--comp','1554','--start','0','--end',str(2451/24),'--out',str(out/'animatic-through-pine-price-1080p.mp4'),'--format','h264','--bitrate','10000','--audio','on'],check=True)
(out/'insertion.json').write_text(json.dumps({'layer':20077,'startFrame':start,'endFrameExclusive':end,'sourceOffsetFrames':24,'fps':24},indent=2)+'\n')
