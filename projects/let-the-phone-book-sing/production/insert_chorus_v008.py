"""Add proposed chorus background to saved native edit; preserve all musical cuts."""
from effectcraft_session import Session,BASE
from PIL import Image
out=BASE/'generated/effectcraft-edit-v008';out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v008.ecproj'
if target.exists():raise SystemExit('Preserve existing v008.')
s=Session(BASE/'generated/effectcraft-edit-v007/Let-the-Phone-Book-Sing-editable-v007.ecproj')
try:
 s.command('comp.open',{'comp':675})
 for lid in (827,853):s.command('layer.setSwitch',{'layers':[lid],'switch':'video','value':False})
 s.command('layer.setSwitch',{'layers':[827],'switch':'audio','value':False})
 path=BASE/'generated/scene-development/chorus-one-canal-background-v001.png'
 item=s.command('file.import',{'paths':[str(path)],'sequence':False})['items'][0]
 lid=s.command('layer.addItem',{'item':item,'index':30})['layer']
 s.command('layer.rename',{'layer':lid,'name':'Chorus 1 — canal square background / no narrator / review'})
 w,h=Image.open(path).size;scale=max(1920/w,1080/h)*100
 s.call('set_property',{'layer':lid,'path':'transform/scale','value':[scale,scale,100]})
 s.command('layer.timing',{'layers':[lid],'in':826/24,'out':1098/24})
 s.call('add_keyframe',{'layer':lid,'path':'transform/opacity','keys':[{'time':f/24,'value':v} for f,v in [(825,0),(826,20),(827,40),(828,60),(829,80),(830,100)]],'interpolation':'linear'})
 s.command('comp.open',{'comp':1554});s.call('save_project',{'path':str(target)})
 print(target)
finally:s.close()
