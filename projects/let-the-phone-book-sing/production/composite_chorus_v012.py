"""Dissolve the complete chorus composite in together, preserving vocal timing."""
from effectcraft_session import Session, BASE

out = BASE / 'generated/effectcraft-edit-v012'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v012.ecproj'
if target.exists():
    raise SystemExit('Preserve v012.')
s = Session(BASE / 'generated/effectcraft-edit-v011/Let-the-Phone-Book-Sing-editable-v011.ecproj')
try:
    s.command('comp.open', {'comp': 675})
    for layer in [17371, 17179]:
        s.command('prop.toggleAnimation', {'layer': layer, 'path': 'transform/opacity', 'value': False})
        s.call('set_property', {'layer': layer, 'path': 'transform/opacity', 'value': 100})
    result = s.command('layer.precompose', {
        'layers': [17371, 17206, 17179], 'name': 'Chorus 1 — singer and Canal together',
        'mode': 'move', 'adjustDuration': False, 'open': False,
    })
    print(result)
    s.command('comp.open', {'comp': 675})
    layers = s.call('get_comp', {'comp': 675})['layers']
    scene = next(l['id'] for l in layers if l['name'] == 'Chorus 1 — singer and Canal together')
    s.command('layer.timing', {'layers': [scene], 'out': 1098/24})
    s.command('layer.timing', {'layers': [scene], 'in': 826/24})
    s.call('add_keyframe', {
        'layer': scene, 'path': 'transform/opacity',
        'keys': [{'time': f/24, 'value': v} for f, v in [(825,0),(826,20),(827,40),(828,60),(829,80),(830,100)]],
        'interpolation': 'linear',
    })
    s.command('comp.open', {'comp': 1554})
    s.call('save_project', {'path': str(target)})
    print('Scene layer:', scene)
finally:
    s.close()
