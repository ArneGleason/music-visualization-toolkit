"""Replace Liberty's approved source, preserving the native edit and timing."""
import json
import subprocess
from effectcraft_session import Session, BASE, CLI

shots = json.loads((BASE/'shots/shotlist.json').read_text())['shots']
start = next(x['startFrame'] for x in shots if x['id']=='PB-005')
end = next(x['endFrameExclusive'] for x in shots if x['id']=='PB-006')
out = BASE/'generated/effectcraft-edit-v052'
out.mkdir(parents=True, exist_ok=True)
target = out/'Let-the-Phone-Book-Sing-editable-v052.ecproj'
if target.exists():
    raise SystemExit('Preserve existing v052')
s = Session(BASE/'generated/effectcraft-edit-v051/Let-the-Phone-Book-Sing-editable-v051.ecproj')
try:
    s.command('comp.open', {'comp':675})
    item = s.command('file.import', {'paths':[str(BASE/'generated/kling-tests/liberty-duck-v001/kling-original-1080p.mp4')], 'sequence':False})['items'][0]
    s.command('layer.replaceSource', {'layer':727, 'item':item})
    s.call('set_property', {'layer':727, 'path':'timeRemap', 'expression':f'(time-{start}/24)+24/24'})
    s.command('layer.setSwitch', {'layers':[727], 'switch':'audio', 'value':False})
    s.command('layer.rename', {'layer':727, 'name':'PB-005–006 — Liberty Bell / duck reversal / approved v001 / source24'})
    for lid, x in [(20385,310),(20328,645)]:
        s.call('set_property', {'layer':lid,'path':'transform/position','value':[x,125,0]})
    s.command('comp.open', {'comp':1554})
    s.call('save_project', {'path':str(target)})
    for frame in [440,451,530,568,574]:
        s.call('render_frame', {'comp':1554,'time':frame/24,'path':str(out/f'check-{frame}.png'),'inline':False,'max_side':1920})
finally:
    s.close()
subprocess.run([str(CLI),'render','--project',str(target),'--gpu','--comp','1554','--start','0','--end',str(2451/24),'--out',str(out/'animatic-through-pine-price-1080p.mp4'),'--format','h264','--bitrate','10000','--audio','on'],check=True)
(out/'insertion.json').write_text(json.dumps({'layer':727,'startFrame':start,'endFrameExclusive':end,'sourceOffsetFrames':24,'fps':24},indent=2)+'\n')
