"""Insert approved Pearl delivery reversal using native EffectCraft."""
import json
import subprocess
from effectcraft_session import Session, BASE, CLI

shots = json.loads((BASE / 'shots/shotlist.json').read_text())
shot = next(x for x in shots['shots'] if x['id'] == 'PB-024')
start, end = shot['startFrame'], shot['endFrameExclusive']
offset = 24
out = BASE / 'generated/effectcraft-edit-v053'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v053.ecproj'
if target.exists():
    raise SystemExit('Preserve existing v053')
s = Session(BASE / 'generated/effectcraft-edit-v052/Let-the-Phone-Book-Sing-editable-v052.ecproj')
try:
    s.command('comp.open', {'comp': 675})
    old = next(x for x in s.call('get_comp', {'comp': 675})['layers'] if x['id'] == 1134)
    s.command('layer.setSwitch', {'layers': [1134], 'switch': 'video', 'value': False})
    item = s.command('file.import', {'paths': [str(BASE / 'generated/kling-tests/pearl-price-v002/kling-original-1080p.mp4')], 'sequence': False})['items'][0]
    layer = s.command('layer.addItem', {'item': item, 'index': old['index']})['layer']
    s.command('layer.rename', {'layer': layer, 'name': 'PB-024 — Pearl Price / portrait delivery reversal / approved v002 / source24'})
    s.command('layer.setSwitch', {'layers': [layer], 'switch': 'audio', 'value': False})
    s.call('set_property', {'layer': layer, 'path': 'transform/scale', 'value': [1920/1916*100]*2+[100]})
    s.command('layer.enableTimeRemap', {'layers': [layer], 'value': True})
    s.call('set_property', {'layer': layer, 'path': 'timeRemap', 'expression': f'(time-{start}/24)+{offset}/24'})
    s.command('layer.timing', {'layers': [layer], 'out': (end+2)/24})
    s.command('layer.timing', {'layers': [layer], 'in': (start-2)/24})
    s.call('add_keyframe', {'layer': layer, 'path': 'transform/opacity', 'keys': [{'time': (start-3+i)/24, 'value': i*20} for i in range(6)], 'interpolation': 'linear'})
    for part, text, frame, pos, fill in [('last','PRICE',2297,[600,125],'#f7dda2'),('first','PEARL',2314,[280,125],'#9dd8cf')]:
        lid=s.command('layer.newText',{'name':f'NAME — PEARL PRICE / {part}','text':text,'font':'Arial Bold Italic','size':88,'fill':fill,'position':pos,'justify':'center'})['layer']
        s.command('layer.style.stroke',{'layers':[lid]})
        s.call('set_property',{'layer':lid,'path':'layerStyles/stroke/color','value':'#292536'})
        s.call('set_property',{'layer':lid,'path':'layerStyles/stroke/size','value':5})
        s.command('layer.timing',{'layers':[lid],'out':2349/24})
        s.command('layer.timing',{'layers':[lid],'in':frame/24})
        s.call('add_keyframe',{'layer':lid,'path':'transform/opacity','keys':[{'time':f/24,'value':v} for f,v in [(frame,0),(frame+2,100),(2341,100),(2349,0)]],'interpolation':'linear'})
    s.command('comp.open', {'comp': 1554})
    s.call('save_project', {'path': str(target)})
    for frame in [2320, 2420, 2460, 2600, 2720]:
        s.call('render_frame', {'comp': 1554, 'time': frame/24, 'path': str(out/f'check-{frame}.png'), 'inline': False, 'max_side': 1920})
finally:
    s.close()
subprocess.run([str(CLI), 'render', '--project', str(target), '--gpu', '--comp', '1554', '--start', '0', '--end', str(2843/24), '--out', str(out/'animatic-through-hope-wait-1080p.mp4'), '--format', 'h264', '--bitrate', '10000', '--audio', 'on'], check=True)
(out/'insertion.json').write_text(json.dumps({'layer': layer, 'startFrame': start, 'endFrameExclusive': end, 'sourceOffsetFrames': offset, 'fps': 24}, indent=2)+'\n')
