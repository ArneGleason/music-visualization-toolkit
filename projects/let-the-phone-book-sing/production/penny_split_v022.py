"""Native still-plate blocking test before generating the two phone performances."""
import json
from PIL import Image
from effectcraft_session import Session, BASE

out=BASE/'generated/effectcraft-edit-v022'
out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v022.ecproj'
if target.exists(): raise SystemExit('Preserve v022')
s=Session(BASE/'generated/effectcraft-edit-v021/Let-the-Phone-Book-Sing-editable-v021.ecproj')
start=1488; end=1650
def prop(l,p,v): s.call('set_property',dict(layer=l,path=p,value=v))
def keys(l,p,values): s.call('add_keyframe',dict(layer=l,path=p,keys=[dict(time=f/24,value=v) for f,v in values],interpolation='linear'))
def comp(name): return s.command('comp.new',dict(name=name,width=1920,height=1080,frameRate=24,duration=4340/24))['comp']
def plate(path,name):
    item=s.command('file.import',dict(paths=[str(BASE/path)],sequence=False))['items'][0]
    lid=s.command('layer.addItem',dict(item=item,index=1))['layer']
    s.command('layer.rename',dict(layer=lid,name=name))
    w,h=Image.open(BASE/path).size
    prop(lid,'transform/scale',[max(1920/w,1080/h)*100]*2+[100])
    return lid
def path(vertices): return {'t':'Path','v':{'vertices':vertices,'in_tangents':[[0,0]]*4,'out_tangents':[[0,0]]*4,'closed':True}}
try:
    richcomp=comp('Penny Chase / Rich phone plate — independent slide')
    rich=plate('generated/scene-development/rich-cash-phone-start-v002.png','Rich — closer approved still')
    splitcomp=comp('Penny Chase / diagonal phone reveal — STILL TEST')
    penny=plate('generated/scene-development/penny-chase-phone-start-v001.png','Penny — centered opening, slide left')
    rlayer=s.command('layer.addItem',dict(item=richcomp,index=1))['layer']
    s.command('mask.new',dict(layer=rlayer,vertices=[[1920,0],[2200,0],[2200,1080],[1920,1080]],closed=True))
    line=s.command('layer.newSolid',dict(name='Diagonal ink divider',color='#292536',width=1920,height=1080))['layer']
    s.command('mask.new',dict(layer=line,vertices=[[1920,0],[1927,0],[1927,1080],[1920,1080]],closed=True))
    pp=[];rp=[];mp=[];lp=[]
    for n in range(25):
        u=n/24; ease=u*u*(3-2*u); f=start+12+n
        top=1920-820*ease; bottom=1920-1100*ease
        pp.append((f,[960-460*ease,540,0]))
        rp.append((f,[960+646+500*(1-ease),540,0]))
        mp.append((f,path([[top,0],[2200,0],[2200,1080],[bottom,1080]])))
        lp.append((f,path([[top-3.5,0],[top+3.5,0],[bottom+3.5,1080],[bottom-3.5,1080]])))
    keys(penny,'transform/position',pp)
    s.command('comp.open',{'comp':richcomp});keys(rich,'transform/position',rp)
    s.command('comp.open',{'comp':splitcomp})
    keys(rlayer,'masks/mask/path',mp);keys(line,'masks/mask/path',lp)
    s.command('comp.open',{'comp':675})
    old=next(x for x in s.call('get_comp',{'comp':675})['layers'] if x['id']==995)
    s.command('layer.setSwitch',dict(layers=[995],switch='video',value=False))
    main=s.command('layer.addItem',dict(item=splitcomp,index=old['index']))['layer']
    s.command('layer.rename',dict(layer=main,name='Penny Chase — STILL TEST / diagonal phone reveal'))
    s.command('layer.timing',dict(layers=[main],out=(end+2)/24))
    s.command('layer.timing',{'layers':[main],'in':(start-2)/24})
    keys(main,'transform/opacity',[(start-3,0),(start-2,20),(start-1,40),(start,60),(start+1,80),(start+2,100)])
    s.command('comp.open',{'comp':1554});s.call('save_project',{'path':str(target)})
finally:s.close()
(BASE/'production/penny-split-v001.json').write_text(json.dumps(dict(status='still_blocking_review_no_video_generated',nativeProject=str(target.relative_to(BASE)),masterFrames=[start,end],revealFrames=[start+12,start+36],revealSecondsRelative=[.5,1.5],easing='smoothstep sampled every frame',splitTopX=1100,splitBottomX=820,pennyShiftX=-460,richShiftX=646,comps={'split':splitcomp,'rich':richcomp},masterLayer=main,concept='Penny alone then slides left as Rich slides in behind diagonal wipe. Cat incidental outside principal crop. Stills only; no generated acting yet.'),indent=2)+'\n')
