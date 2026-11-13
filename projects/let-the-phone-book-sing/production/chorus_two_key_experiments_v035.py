"""Three native key/edge-color experiments; original v031 remains keeper."""
import json
from effectcraft_session import Session,BASE
root=BASE/'generated/chorus-two-key-experiments-v035';root.mkdir(parents=True,exist_ok=True)
soft={'screenGain':110,'clipBlack':3,'clipWhite':90,'screenShrinkGrow':0,'screenSoftness':.4,'screenPreblur':.2,'despill':0,'edgeColor':1}
variants={
 'a-cleaner':{'key':{},'effects':[('ec.key.keycleaner',{'additionalEdgeRadius':1.5,'reduceChatter':True,'alphaContrast':100,'strength':40}),('ec.key.advancedspill',{'method':0,'suppression':100})]},
 'b-soft-spill':{'key':soft,'effects':[('ec.key.keycleaner',{'additionalEdgeRadius':1,'reduceChatter':True,'alphaContrast':100,'strength':30}),('ec.key.advancedspill',{'method':1,'suppression':100,'ultraSettings/keyColor':[0,211/255,0,1],'ultraSettings/tolerance':50,'ultraSettings/desaturate':25,'ultraSettings/spillRange':60})]},
 'c-refine':{'key':soft,'effects':[('ec.matte.refinesoft',{'radius':2,'feather':.6,'contrast':5,'reduceChatter':25,'decontaminate':True,'decontamination/decontaminationAmount':70}),('ec.key.advancedspill',{'method':1,'suppression':100,'ultraSettings/keyColor':[0,211/255,0,1],'ultraSettings/desaturate':25,'ultraSettings/spillRange':60})]}}
for name,config in variants.items():
 out=root/name;out.mkdir(exist_ok=True);target=out/'experiment.ecproj'
 if target.exists():raise SystemExit('Preserve '+name)
 s=Session(BASE/'generated/effectcraft-edit-v031/Let-the-Phone-Book-Sing-editable-v031.ecproj')
 try:
  s.command('comp.open',{'comp':19862})
  for k,v in config['key'].items():s.call('set_property',{'layer':19805,'path':'effects/#1/'+k,'value':v})
  for fx,vals in config['effects']:
   p=s.call('add_effect',{'layer':19805,'effect':fx})['path']
   for k,v in vals.items():s.call('set_property',{'layer':19805,'path':p+'/'+k,'value':v})
  s.call('save_project',{'path':str(target)})
  for f in [1634,1690,1820]:s.call('render_frame',{'comp':1554,'time':f/24,'path':str(out/f'check-{f}.png'),'inline':False,'max_side':1920})
 finally:s.close()
 print(name,flush=True)
(BASE/'production/chorus-two-key-experiments-v035.json').write_text(json.dumps({'status':'pending_review','baseline':'generated/effectcraft-edit-v031/Let-the-Phone-Book-Sing-editable-v031.ecproj','variants':variants,'output':str(root.relative_to(BASE))},indent=2)+'\n')
