"""Overlap existing chorus takes by six frames, preserving musical boundaries."""
from effectcraft_session import Session, BASE
out=BASE/'generated/effectcraft-edit-v010'
out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v010.ecproj'
if target.exists():raise SystemExit('Preserve v010.')
s=Session(BASE/'generated/effectcraft-edit-v009/Let-the-Phone-Book-Sing-editable-v009.ecproj')
try:
    s.command('comp.open',{'comp':675})
    s.command('layer.timing',{'layers':[17206],'in':966/24})
    s.call('set_property',{'layer':17206,'path':'timeRemap','expression':'Math.max(0, time-966/24)'})
    s.call('add_keyframe',{'layer':17206,'path':'transform/opacity','keys':[{'time':966/24,'value':0},{'time':972/24,'value':100}],'interpolation':'linear'})
    s.command('layer.rename',{'layer':17206,'name':'Chorus 1 — coffee / six-frame overlap dissolve'})
    s.command('comp.open',{'comp':1554})
    s.call('save_project',{'path':str(target)})
finally:s.close()
