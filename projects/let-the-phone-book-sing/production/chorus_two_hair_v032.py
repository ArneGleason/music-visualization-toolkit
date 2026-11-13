"""Gentler native matte for fine Chorus 2 hair; preserve v031 comparison."""
import json
from effectcraft_session import Session,BASE
out=BASE/'generated/effectcraft-edit-v032';out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v032.ecproj'
if target.exists():raise SystemExit('Preserve v032')
values={'screenGain':120,'clipBlack':5,'clipWhite':82,'screenShrinkGrow':0,'screenSoftness':0.4,'screenPreblur':0.25}
s=Session(BASE/'generated/effectcraft-edit-v031/Let-the-Phone-Book-Sing-editable-v031.ecproj')
try:
 s.command('comp.open',{'comp':19862})
 for name,val in values.items():s.call('set_property',{'layer':19805,'path':'effects/#1/'+name,'value':val})
 before={l['id'] for l in s.call('get_comp',{'comp':19862})['layers']}
 s.command('edit.duplicate',{'layers':[19805]})
 recovery=next(l['id'] for l in s.call('get_comp',{'comp':19862})['layers'] if l['id'] not in before)
 for k,v in {'screenGain':200,'clipBlack':25,'screenShrinkGrow':-.65,'screenSoftness':.7,'screenPreblur':.5}.items():
  s.call('set_property',{'layer':19805,'path':'effects/#1/'+k,'value':v})
 s.command('layer.precompose',{'layers':[recovery],'name':'Chorus 2 fine hair matte recovery','mode':'move','adjustDuration':False,'open':False})
 s.command('comp.open',{'comp':19862})
 outer=next(l['id'] for l in s.call('get_comp',{'comp':19862})['layers'] if l['name']=='Chorus 2 fine hair matte recovery')
 s.command('mask.new',{'layer':outer,'vertices':[[-100,-100],[2020,-100],[2020,520],[-100,520]],'closed':True})
 s.call('set_property',{'layer':outer,'path':'masks/mask/feather','value':[25,25]})
 s.call('save_project',{'path':str(target)})
 for f in [1634,1690,1820]:s.call('render_frame',{'comp':1554,'time':f/24,'path':str(out/f'check-{f}.png'),'inline':False,'max_side':1920})
finally:s.close()
(BASE/'production/chorus-two-hair-v001.json').write_text(json.dumps({'status':'pending_review','nativeProject':str(target.relative_to(BASE)),'controls':values,'notes':'Reduce matte erosion and black clipping to retain thin hair connections. Source Hedra also contains a few detached hair fragments; key tuning cannot recreate missing strands. Existing hair despill and ink outline retained.'},indent=2)+'\n')
