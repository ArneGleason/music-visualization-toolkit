"""Bold numeral echoes follow the apple's foreground flight and club's leftward throw."""
import json
import math
from effectcraft_session import Session, BASE
out=BASE/'generated/effectcraft-edit-v019'
out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v019.ecproj'
if target.exists():raise SystemExit('Preserve v019')
s=Session(BASE/'generated/effectcraft-edit-v018/Let-the-Phone-Book-Sing-editable-v018.ecproj')
records=[]
try:
 s.command('comp.open',{'comp':675})
 old=json.loads((BASE/'production/cash-echoes-v002.json').read_text())
 s.command('layer.setSwitch',{'layers':[e['layer'] for e in old['events']],'switch':'video','value':False})
 for kind,text,size,end in [('penny','10',185,1232),('rich','1,000',135,1357)]:
  onsets=json.loads((BASE/f'production/{kind}-echo-v001.json').read_text())['events']
  for i,event in enumerate(onsets):
   f=event['masterFrame'];life=min(20,end-f)
   lid=s.command('layer.newText',dict(name=f'{kind.title()} {text} — prop-flight echo {i+1}',text=text,font='Arial Bold Italic',size=size,fill=['#f7dda2','#9dd8cf','#f0b38b'][i],position=[0,0],justify='center'))['layer']
   s.command('layer.style.stroke',{'layers':[lid]})
   for p,v in [('layerStyles/stroke/color','#292536'),('layerStyles/stroke/size',5)]:s.call('set_property',dict(layer=lid,path=p,value=v))
   s.command('layer.timing',{'layers':[lid],'out':(f+life)/24})
   s.command('layer.timing',{'layers':[lid],'in':f/24})
   values={p:[] for p in ['position','scale','rotation','opacity']}
   for n in range(life+1):
    u=n/life;pulse=math.sin(math.pi*u)
    if kind=='penny':
     x=940+850*u;y=430+440*u-145*math.sin(math.pi*u)+i*24
     scale=(.95+.65*u+.12*pulse)*(1-.06*i);rotation=-9+19*u
    else:
     x=1000-1300*u;y=510-100*u-160*math.sin(math.pi*u)+i*22
     scale=(1.05-.20*u+.13*pulse)*(1-.05*i);rotation=8-22*u
    fade=min(1,n/2)*min(1,(1-u)/.48)
    vals=dict(position=[x,y,0],scale=[scale*100,scale*100,100],rotation=rotation,opacity=100*fade)
    for p,v in vals.items():values[p].append(dict(time=(f+n)/24,value=v))
   for p,v in values.items():s.call('add_keyframe',dict(layer=lid,path='transform/'+p,keys=v,interpolation='linear'))
   records.append(dict(character=kind,text=text,layer=lid,startFrame=f,endFrameExclusive=f+life))
 s.command('comp.open',{'comp':1554});s.call('save_project',{'path':str(target)})
finally:s.close()
(BASE/'production/cash-echoes-v003.json').write_text(json.dumps(dict(status='draft_review',concept='Larger bold whole numerals: 10 projects toward foreground-right along apple flight; 1,000 sweeps left after club. Continuous arcs, perspective and moving fades. Same echo onsets, fade ends at scene boundary.',events=records,nativeProject=str(target.relative_to(BASE))),indent=2)+'\n')
