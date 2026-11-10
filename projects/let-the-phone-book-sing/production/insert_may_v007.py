"""Insert approved May footage into saved v006; render with EffectCraft separately."""
from effectcraft_session import Session, BASE

out = BASE / 'generated/effectcraft-edit-v007'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v007.ecproj'
if target.exists():
    raise SystemExit('v007 already exists; preserve it.')
s = Session(BASE / 'generated/effectcraft-edit-v006/Let-the-Phone-Book-Sing-editable-v006.ecproj')
try:
    s.command('comp.open', {'comp': 675})
    for lid in (781, 804):
        s.command('layer.setSwitch', {'layers': [lid], 'switch': 'video', 'value': False})
    item = s.command('file.import', {'paths': [str(BASE / 'generated/kling-tests/may-bloom-v001/may-original-1080p.mp4')], 'sequence': False})['items'][0]
    lid = s.command('layer.addItem', {'item': item, 'index': 32})['layer']
    s.command('layer.rename', {'layer': lid, 'name': 'May Bloom — approved fan gag / source frame 24'})
    s.command('layer.setSwitch', {'layers': [lid], 'switch': 'audio', 'value': False})
    s.call('set_property', {'layer': lid, 'path': 'transform/scale', 'value': [1920/1916*100]*2+[100]})
    s.command('layer.enableTimeRemap', {'layers': [lid], 'value': True})
    s.call('set_property', {'layer': lid, 'path': 'timeRemap', 'expression': 'Math.max(0, time-695/24+1)'})
    s.command('layer.timing', {'layers': [lid], 'in': 693/24, 'out': 830/24})
    s.call('add_keyframe', {'layer': lid, 'path': 'transform/opacity', 'keys': [{'time': f/24, 'value': v} for f,v in [(692,0),(693,20),(694,40),(695,60),(696,80),(697,100)]], 'interpolation': 'linear'})
    s.command('comp.open', {'comp': 1554})
    s.call('save_project', {'path': str(target)})
    print(target)
finally:
    s.close()
