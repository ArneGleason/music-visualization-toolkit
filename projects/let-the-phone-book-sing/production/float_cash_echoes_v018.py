"""Replace numeral score stamps with short, continuously drifting echo pulses."""
import json
import math
from effectcraft_session import Session, BASE
out=BASE/'generated/effectcraft-edit-v018'
out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v018.ecproj'
if target.exists(): raise SystemExit('Preserve v018')
s=Session(BASE/'generated/effectcraft-edit-v017/Let-the-Phone-Book-Sing-editable-v017.ecproj')
records=[]
try:
 s.command('comp.open',{'comp':675})
 for kind,text,size,side,positions in [
  ('penny','10',150,1,[(1450,520),(1530,630),(1610,740)]),
  ('rich','1,000',108,-1,[(310,660),(330,770),(350,880)])]:
  old=json.loads((BASE/f'production/{kind}-echo-v001.json').read_text())
  s.command('layer.setSwitch',{'layers':old['layers'],'switch':'video','value':False})
  for i,(event,(x,y)) in enumerate(zip(old['events'],positions)):
   f=event['masterFrame'];life=13
   lid=s.command('layer.newText',dict(name=f'{kind.title()} echo {text} — drifting pulse {i+1}',text=text,font='Arial Bold Italic',size=size,fill=['#f7dda2','#9dd8cf','#f0b38b'][i],position=[x,y],justify='center'))['layer']
   s.command('layer.style.stroke',{'layers':[lid]})
   for path,value in [('layerStyles/stroke/color','#292536'),('layerStyles/stroke/size',4)]:
    s.call('set_property',dict(layer=lid,path=path,value=value))
   s.command('layer.timing',{'layers':[lid],'out':(f+life)/24})
   s.command('layer.timing',{'layers':[lid],'in':f/24})
   values={p:[] for p in ['position','scale','rotation','opacity']}
   for n in range(life+1):
    u=n/life
    # One soft acoustic-like attack, immediate decay; no landing or held pose.
    pulse=math.sin(math.pi*min(1,u/.32)/2) if u<.32 else math.exp(-3.2*(u-.32))
    fade=min(1,n/2)*max(0,1-u)**.8
    depth=(1-.16*u)*(1-.06*i)
    scale=depth*(.65+.35*pulse)
    vals=dict(position=[x+side*(110*u+20*math.sin(math.pi*u)),y-65*u-24*math.sin(2*math.pi*u),0],scale=[100*scale*(1+.035*math.sin(2*math.pi*u)),100*scale,100],rotation=side*(-5+11*math.sin(math.pi*u)),opacity=90*fade*pulse)
    for p,v in vals.items():values[p].append(dict(time=(f+n)/24,value=v))
   for p,v in values.items():s.call('add_keyframe',dict(layer=lid,path='transform/'+p,keys=v,interpolation='linear'))
   records.append(dict(character=kind,text=text,layer=lid,startFrame=f,endFrameExclusive=f+life))
 s.command('comp.open',{'comp':1554})
 s.call('save_project',{'path':str(target)})
finally:s.close()
(BASE/'production/cash-echoes-v002.json').write_text(json.dumps(dict(status='draft_review',concept='Soft short-lived numeral pulses with continuous curved drift and immediate decay; no score stamps or held stacks.',durationFrames=13,events=records,nativeProject=str(target.relative_to(BASE))),indent=2)+'\n')
