"""Join approved wheel and coffee continuation in the native chorus edit."""
from effectcraft_session import Session, BASE
out = BASE/'generated/effectcraft-edit-v009'
out.mkdir(parents=True, exist_ok=True)
target = out/'Let-the-Phone-Book-Sing-editable-v009.ecproj'
if target.exists():
    raise SystemExit('Preserve existing v009.')
s = Session(BASE/'generated/effectcraft-edit-v008/Let-the-Phone-Book-Sing-editable-v008.ecproj')
try:
    s.command('comp.open', {'comp':675})
    s.command('layer.setSwitch', {'layers':[17155], 'switch':'video', 'value':False})
    for name, start, end in [('wheel',828,972), ('coffee',972,1098)]:
        item = s.command('file.import', {'paths':[str(BASE/f'generated/kling-tests/chorus-one-v001/{name}-original-1080p.mp4')], 'sequence':False})['items'][0]
        lid = s.command('layer.addItem', {'item':item,'index':30})['layer']
        s.command('layer.rename', {'layer':lid,'name':f'Chorus 1 — {name} / direct continuous join'})
        s.command('layer.setSwitch', {'layers':[lid],'switch':'audio','value':False})
        s.call('set_property', {'layer':lid,'path':'transform/scale','value':[1920/1916*100]*2+[100]})
        s.command('layer.enableTimeRemap', {'layers':[lid],'value':True})
        s.call('set_property', {'layer':lid,'path':'timeRemap','expression':f'Math.max(0, time-{start}/24)'})
        s.command('layer.timing', {'layers':[lid],'out':end/24})
        s.command('layer.timing', {'layers':[lid],'in':(start-2 if name=='wheel' else start)/24})
        if name=='wheel':
            s.call('add_keyframe', {'layer':lid,'path':'transform/opacity','keys':[{'time':f/24,'value':v} for f,v in [(825,0),(826,20),(827,40),(828,60),(829,80),(830,100)]],'interpolation':'linear'})
    print([(l['name'],l['in'],l['out']) for l in s.call('get_comp',{'comp':675})['layers'] if 'direct continuous join' in l['name']])
    s.command('comp.open', {'comp':1554})
    s.call('save_project', {'path':str(target)})
finally:
    s.close()
