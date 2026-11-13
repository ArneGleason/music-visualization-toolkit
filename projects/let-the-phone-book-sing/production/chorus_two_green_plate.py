"""Place approved transparent narrator B on green using native EffectCraft."""
from PIL import Image
from effectcraft_session import Session, BASE
out=BASE/'generated/avatar-tests/chorus-two-v001'
out.mkdir(parents=True,exist_ok=True)
s=Session()
try:
    comp=s.command('comp.new',{'name':'Chorus 2 approved B green plate','width':1920,'height':1080,'frameRate':24,'duration':1})['comp']
    s.command('layer.newSolid',{'name':'Uniform green','color':'#00FF00','width':1920,'height':1080})
    path=BASE/'generated/scene-development/chorus-two-narrator-cutout-v002.png'
    w,h=Image.open(path).size
    item=s.command('file.import',{'paths':[str(path)],'sequence':False})['items'][0]
    layer=s.command('layer.addItem',{'item':item,'index':1})['layer']
    s.call('set_property',{'layer':layer,'path':'transform/scale','value':[1920/w*92,1080/h*92,100]})
    s.call('set_property',{'layer':layer,'path':'transform/position','value':[960,583.2,0]})
    s.call('save_project',{'path':str(out/'narrator-green.ecproj')})
    s.call('render_frame',{'comp':comp,'time':0,'path':str(out/'narrator-green.png'),'inline':False,'max_side':1920})
finally:s.close()
