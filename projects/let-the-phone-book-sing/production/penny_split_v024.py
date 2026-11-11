"""Revise only Rich with the comic-panic take; preserve approved Penny."""
import json
import subprocess
from effectcraft_session import Session, BASE

out = BASE / 'generated/effectcraft-edit-v024'
target = out / 'Let-the-Phone-Book-Sing-editable-v024.ecproj'
if target.exists():
    raise SystemExit('Preserve v024')
plates = [
    ('rich', 19384, 19546, 1, 24),
]
for name, *_ in plates:
    if not (BASE / f'generated/kling-tests/penny-chase-{name}-v002/{name}-original-1080p.mp4').exists():
        raise SystemExit(f'Missing {name} video')
out.mkdir(parents=True, exist_ok=True)
s = Session(BASE / 'generated/effectcraft-edit-v023/Let-the-Phone-Book-Sing-editable-v023.ecproj')
records = {}
try:
    for name, comp, old, index, offset in plates:
        src = BASE / f'generated/kling-tests/penny-chase-{name}-v002/{name}-original-1080p.mp4'
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'json', str(src)]))['streams'][0]
        s.command('comp.open', {'comp': comp})
        s.command('layer.setSwitch', {'layers': [old], 'switch': 'video', 'value': False})
        item = s.command('file.import', {'paths': [str(src)], 'sequence': False})['items'][0]
        layer = s.command('layer.addItem', {'item': item, 'index': index})['layer']
        s.command('layer.rename', {'layer': layer, 'name': f'{name.title()} — phone performance / source{offset}'})
        s.command('layer.setSwitch', {'layers': [layer], 'switch': 'audio', 'value': False})
        scale = max(1920/probe['width'], 1080/probe['height'])*100
        s.call('set_property', {'layer': layer, 'path': 'transform/scale', 'value': [scale, scale, 100]})
        keys = []
        for n in range(25):
            u = n/24
            ease = u*u*(3-2*u)
            x = 960-460*ease if name == 'penny' else 960+646+500*(1-ease)
            keys.append({'time': (1500+n)/24, 'value': [x, 540, 0]})
        s.call('add_keyframe', {'layer': layer, 'path': 'transform/position', 'keys': keys, 'interpolation': 'linear'})
        s.command('layer.enableTimeRemap', {'layers': [layer], 'value': True})
        s.call('set_property', {'layer': layer, 'path': 'timeRemap', 'expression': f'(time-1488/24)+{offset}/24'})
        s.command('layer.timing', {'layers': [layer], 'out': 1652/24})
        s.command('layer.timing', {'layers': [layer], 'in': 1486/24})
        records[name] = {'layer': layer, 'sourceOffsetFrames': offset, 'source': str(src.relative_to(BASE))}
    s.command('comp.open', {'comp': 675})
    s.command('layer.rename', {'layer': 19493, 'name': 'Penny Chase — phone pitch / animated diagonal split'})
    s.command('comp.open', {'comp': 1554})
    s.call('save_project', {'path': str(target)})
finally:
    s.close()
(BASE/'production/penny-split-v003.json').write_text(json.dumps({'status': 'initial_video_composite_review', 'nativeProject': str(target.relative_to(BASE)), 'masterFrames': [1488,1650], 'revealFrames': [1500,1524], 'plates': records}, indent=2)+'\n')
