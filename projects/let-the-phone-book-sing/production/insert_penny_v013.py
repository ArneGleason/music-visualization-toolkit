"""Insert approved Penny v003 at fixed musical boundaries; retain Rich stills."""
from effectcraft_session import Session, BASE

out = BASE / 'generated/effectcraft-edit-v013'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v013.ecproj'
if target.exists():
    raise SystemExit('Preserve v013.')
s = Session(BASE / 'generated/effectcraft-edit-v012/Let-the-Phone-Book-Sing-editable-v012.ecproj')
try:
    s.command('comp.open', {'comp': 675})
    s.command('layer.setSwitch', {'layers': [877, 900], 'switch': 'video', 'value': False})
    item = s.command('file.import', {'paths': [str(BASE / 'generated/kling-tests/penny-cash-v003/penny-original-1080p.mp4')], 'sequence': False})['items'][0]
    layer = s.command('layer.addItem', {'item': item, 'index': 28})['layer']
    s.command('layer.rename', {'layer': layer, 'name': 'Penny Cash — approved v003 / source offset30'})
    s.command('layer.setSwitch', {'layers': [layer], 'switch': 'audio', 'value': False})
    s.call('set_property', {'layer': layer, 'path': 'transform/scale', 'value': [1920/1916*100]*2+[100]})
    s.command('layer.enableTimeRemap', {'layers': [layer], 'value': True})
    s.call('set_property', {'layer': layer, 'path': 'timeRemap', 'expression': '(time-1096/24)+30/24'})
    s.command('layer.timing', {'layers': [layer], 'out': 1232/24})
    s.command('layer.timing', {'layers': [layer], 'in': 1094/24})
    s.call('add_keyframe', {'layer': layer, 'path': 'transform/opacity', 'keys': [{'time': f/24, 'value': v} for f,v in [(1093,0),(1094,20),(1095,40),(1096,60),(1097,80),(1098,100)]], 'interpolation': 'linear'})
    s.command('comp.open', {'comp': 1554})
    s.call('save_project', {'path': str(target)})
    print('Penny layer:', layer)
finally:
    s.close()
