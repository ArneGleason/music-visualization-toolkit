"""Reuse approved native key/hair precomp for chorus; preserve previous edit."""
from effectcraft_session import Session,BASE
out=BASE/'generated/effectcraft-edit-v011';out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v011.ecproj'
if target.exists():raise SystemExit('Preserve v011.')
s=Session(BASE/'generated/effectcraft-edit-v010/Let-the-Phone-Book-Sing-editable-v010.ecproj')
try:
    cid=s.command('project.duplicate',{'items':[17020]})['items'][0]
    s.command('comp.open',{'comp':cid})
    layers=s.call('get_comp',{'comp':cid})['layers']
    plate=next(l['id'] for l in layers if l['type']=='Footage')
    item=s.command('file.import',{'paths':[str(BASE/'generated/avatar-tests/chorus-one-v001/hedra-original-1080p.mp4')],'sequence':False})['items'][0]
    s.command('layer.replaceSource',{'layer':plate,'item':item})
    s.call('set_property',{'layer':plate,'path':'timeRemap','expression':'Math.max(0, time-810/24)'})
    s.command('layer.rename',{'layer':plate,'name':'Chorus singer — native key, despill, ink outline'})
    s.command('comp.open',{'comp':675})
    lid=s.command('layer.addItem',{'item':cid,'index':30})['layer']
    s.command('layer.rename',{'layer':lid,'name':'Chorus singer — early O pickup / approved native hair cleanup'})
    s.command('layer.setSwitch',{'layers':[lid],'switch':'audio','value':False})
    s.call('set_property',{'layer':lid,'path':'transform/scale','value':[85,85,100]})
    s.call('set_property',{'layer':lid,'path':'transform/position','value':[960,621,0]})
    s.command('layer.timing',{'layers':[lid],'out':1098/24})
    s.command('layer.timing',{'layers':[lid],'in':814/24})
    s.call('add_keyframe',{'layer':lid,'path':'transform/opacity','keys':[{'time':f/24,'value':v} for f,v in [(814,0),(822,100)]],'interpolation':'linear'})
    s.command('comp.open',{'comp':1554})
    s.call('save_project',{'path':str(target)})
    print({'precomp':cid,'plate':plate,'masterLayer':lid})
finally:s.close()
