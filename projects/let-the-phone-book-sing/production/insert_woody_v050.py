"""Insert approved Woody phone surprise using native EffectCraft."""
import json
import subprocess
from effectcraft_session import Session, BASE, CLI

shots = json.loads((BASE / 'shots/shotlist.json').read_text())
shot = next(x for x in shots['shots'] if x['id'] == 'PB-022')
start, end = shot['startFrame'], shot['endFrameExclusive']
offset = 48
out = BASE / 'generated/effectcraft-edit-v050'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v050.ecproj'
if target.exists():
    raise SystemExit('Preserve existing v050')
s = Session(BASE / 'generated/effectcraft-edit-v049/Let-the-Phone-Book-Sing-editable-v049.ecproj')
try:
    s.command('comp.open', {'comp': 675})
    old = next(x for x in s.call('get_comp', {'comp': 675})['layers'] if x['id'] == 1088)
    s.command('layer.setSwitch', {'layers': [1088], 'switch': 'video', 'value': False})
    item = s.command('file.import', {'paths': [str(BASE / 'generated/kling-tests/woody-pine-v003/kling-original-1080p.mp4')], 'sequence': False})['items'][0]
    layer = s.command('layer.addItem', {'item': item, 'index': old['index']})['layer']
    s.command('layer.rename', {'layer': layer, 'name': 'PB-022 — Woody Pine / art and ringing phone / approved take / source48'})
    s.command('layer.setSwitch', {'layers': [layer], 'switch': 'audio', 'value': False})
    s.call('set_property', {'layer': layer, 'path': 'transform/scale', 'value': [1920/1916*100]*2+[100]})
    s.command('layer.enableTimeRemap', {'layers': [layer], 'value': True})
    s.call('set_property', {'layer': layer, 'path': 'timeRemap', 'expression': f'(time-{start}/24)+{offset}/24'})
    s.command('layer.timing', {'layers': [layer], 'out': (end+2)/24})
    s.command('layer.timing', {'layers': [layer], 'in': (start-2)/24})
    s.call('add_keyframe', {'layer': layer, 'path': 'transform/opacity', 'keys': [{'time': (start-3+i)/24, 'value': i*20} for i in range(6)], 'interpolation': 'linear'})
    for part, text, frame, pos, fill in [('last','PINE',2031,[1760,125],'#f7dda2'),('first','WOODY',2048,[1400,125],'#9dd8cf')]:
        lid=s.command('layer.newText',{'name':f'NAME — WOODY PINE / {part}','text':text,'font':'Arial Bold Italic','size':88,'fill':fill,'position':pos,'justify':'center'})['layer']
        s.command('layer.style.stroke',{'layers':[lid]})
        s.call('set_property',{'layer':lid,'path':'layerStyles/stroke/color','value':'#292536'})
        s.call('set_property',{'layer':lid,'path':'layerStyles/stroke/size','value':5})
        s.command('layer.timing',{'layers':[lid],'out':2083/24})
        s.command('layer.timing',{'layers':[lid],'in':frame/24})
        s.call('add_keyframe',{'layer':lid,'path':'transform/opacity','keys':[{'time':f/24,'value':v} for f,v in [(frame,0),(frame+2,100),(2075,100),(2083,0)]],'interpolation':'linear'})
    s.command('comp.open', {'comp': 1554})
    s.call('save_project', {'path': str(target)})
    for frame in [2036, 2056, 2138, 2160]:
        s.call('render_frame', {'comp': 1554, 'time': frame/24, 'path': str(out/f'check-{frame}.png'), 'inline': False, 'max_side': 1920})
finally:
    s.close()
subprocess.run([str(CLI), 'render', '--project', str(target), '--gpu', '--comp', '1554', '--start', '0', '--end', str(2451/24), '--out', str(out/'animatic-through-pine-price-1080p.mp4'), '--format', 'h264', '--bitrate', '10000', '--audio', 'on'], check=True)
(out/'insertion.json').write_text(json.dumps({'layer': layer, 'startFrame': start, 'endFrameExclusive': end, 'sourceOffsetFrames': offset, 'fps': 24}, indent=2)+'\n')
