"""Refine the native opening key; preserve v001 for comparison."""
from effectcraft_session import Session,BASE
out=BASE/'generated/effectcraft-edit-v002';out.mkdir(exist_ok=True)
s=Session(BASE/'generated/effectcraft-edit-v001/Let-the-Phone-Book-Sing-editable-v001.ecproj')
s.command('comp.open',{'comp':1})
for path,v in [('tolerance',15),('softness',5)]:s.call('set_property',{'layer':240,'path':'effects/#1/'+path,'value':v})
s.command('comp.open',{'comp':1554})
s.call('save_project',{'path':str(out/'Let-the-Phone-Book-Sing-editable-v002.ecproj')})
s.close()
# Save As preserves existing relative media links here: sibling folders at the same depth.
