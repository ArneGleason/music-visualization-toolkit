"""Insert approved Miles flower exchange, preserving musical boundaries."""
from effectcraft_session import Session, BASE

out = BASE / 'generated/effectcraft-edit-v020'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v020.ecproj'
if target.exists():
    raise SystemExit('Preserve v020.')
s = Session(BASE / 'generated/effectcraft-edit-v019/Let-the-Phone-Book-Sing-editable-v019.ecproj')
try:
    s.command('comp.open', {'comp': 675})
    old = next(x for x in s.call('get_comp', {'comp': 675})['layers'] if x['id'] == 971)
    s.command('layer.setSwitch', {'layers': [971], 'switch': 'video', 'value': False})
    item = s.command('file.import', {'paths': [str(BASE / 'generated/kling-tests/miles-chase-v001/miles-original-1080p.mp4')], 'sequence': False})['items'][0]
    layer = s.command('layer.addItem', {'item': item, 'index': old['index']})['layer']
    s.command('layer.rename', {'layer': layer, 'name': 'Miles Chase — flower for Belle / source48 / approved take'})
    s.command('layer.setSwitch', {'layers': [layer], 'switch': 'audio', 'value': False})
    s.call('set_property', {'layer': layer, 'path': 'transform/scale', 'value': [1920/1916*100]*2+[100]})
    s.command('layer.enableTimeRemap', {'layers': [layer], 'value': True})
    s.call('set_property', {'layer': layer, 'path': 'timeRemap', 'expression': '(time-1355/24)+48/24'})
    s.command('layer.timing', {'layers': [layer], 'out': 1490/24})
    s.command('layer.timing', {'layers': [layer], 'in': 1353/24})
    s.call('add_keyframe', {'layer': layer, 'path': 'transform/opacity', 'keys': [{'time': f/24, 'value': v} for f,v in [(1352,0),(1353,20),(1354,40),(1355,60),(1356,80),(1357,100)]], 'interpolation': 'linear'})
    s.command('comp.open', {'comp': 1554})
    s.call('save_project', {'path': str(target)})
    print('Miles layer:', layer)
finally:
    s.close()
