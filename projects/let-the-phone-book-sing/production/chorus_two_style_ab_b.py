"""Native EffectCraft still preview of narrator over shared Chorus 2 starter."""
from PIL import Image
from effectcraft_session import Session, BASE
out=BASE/'generated/scene-development'
s=Session()
try:
    comp=s.command('comp.new',{'name':'Chorus 2 narrator placement review','width':1920,'height':1080,'frameRate':24,'duration':1})['comp']
    for name in ['chorus-two-shared-starter-v003.png','chorus-two-narrator-cutout-v002.png']:
        path=out/name
        width,height=Image.open(path).size
        item=s.command('file.import',{'paths':[str(path)],'sequence':False})['items'][0]
        layer=s.command('layer.addItem',{'item':item,'index':1})['layer']
        factor = .92 if 'cutout' in name else 1
        s.call('set_property',{'layer':layer,'path':'transform/scale','value':[1920/width*100*factor,1080/height*100*factor,100]})
        s.call('set_property',{'layer':layer,'path':'transform/position','value':[960,1080-540*factor,0]})
    s.call('save_project',{'path':str(out/'chorus-two-style-ab-b.ecproj')})
    s.call('render_frame',{'comp':comp,'time':0,'path':str(out/'chorus-two-style-ab-b.png'),'inline':False,'max_side':1920})
finally:s.close()
