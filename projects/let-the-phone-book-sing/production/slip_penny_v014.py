"""Favor Penny's satisfied ending without moving musical cuts."""
from effectcraft_session import Session, BASE
out = BASE / 'generated/effectcraft-edit-v014'
out.mkdir(parents=True, exist_ok=True)
target = out / 'Let-the-Phone-Book-Sing-editable-v014.ecproj'
if target.exists():
    raise SystemExit('Preserve v014.')
s = Session(BASE / 'generated/effectcraft-edit-v013/Let-the-Phone-Book-Sing-editable-v013.ecproj')
try:
    s.command('comp.open', {'comp': 675})
    s.call('set_property', {'layer': 17423, 'path': 'timeRemap', 'expression': '(time-1096/24)+54/24'})
    s.command('layer.rename', {'layer': 17423, 'name': 'Penny Cash — approved v003 / source offset54 / satisfied ending'})
    s.command('comp.open', {'comp': 1554})
    s.call('save_project', {'path': str(target)})
finally:
    s.close()
