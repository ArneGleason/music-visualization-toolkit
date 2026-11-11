"""Insert approved Rich with one-second source tail; preserve musical cuts."""
from effectcraft_session import Session, BASE
out = BASE / 'generated/effectcraft-edit-v015'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v015.ecproj'
if target.exists():
    raise SystemExit('Preserve v015.')
s = Session(BASE / 'generated/effectcraft-edit-v014/Let-the-Phone-Book-Sing-editable-v014.ecproj')
try:
    s.command('comp.open', {'comp': 675})
    s.command('layer.setSwitch', {'layers': [924, 947], 'switch': 'video', 'value': False})
    item = s.command('file.import', {'paths': [str(BASE / 'generated/kling-tests/rich-cash-v001/rich-original-1080p.mp4')], 'sequence': False})['items'][0]
    layer = s.command('layer.addItem', {'item': item, 'index': 26})['layer']
    s.command('layer.rename', {'layer': layer, 'name': 'Rich Cash — approved Siamese take / source92 / one-second tail'})
    s.command('layer.setSwitch', {'layers': [layer], 'switch': 'audio', 'value': False})
    s.call('set_property', {'layer': layer, 'path': 'transform/scale', 'value': [1920/1916*100]*2+[100]})
    s.command('layer.enableTimeRemap', {'layers': [layer], 'value': True})
    s.call('set_property', {'layer': layer, 'path': 'timeRemap', 'expression': '(time-1230/24)+92/24'})
    s.command('layer.timing', {'layers': [layer], 'out': 1357/24})
    s.command('layer.timing', {'layers': [layer], 'in': 1228/24})
    s.call('add_keyframe', {'layer': layer, 'path': 'transform/opacity', 'keys': [{'time': f/24, 'value': v} for f,v in [(1227,0),(1228,20),(1229,40),(1230,60),(1231,80),(1232,100)]], 'interpolation': 'linear'})
    s.command('comp.open', {'comp': 1554})
    s.call('save_project', {'path': str(target)})
    print('Rich layer:', layer)
finally:
    s.close()
