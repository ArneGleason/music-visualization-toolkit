"""Native EffectCraft numeral stamps: Penny awards himself perfect tens."""
import json
from effectcraft_session import Session, BASE
out = BASE/'generated/effectcraft-edit-v016'
out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v016.ecproj'
if target.exists(): raise SystemExit('Preserve v016')
# Approximate repeat attacks from local normalized waveform matching, rounded to grid.
events=[(1206,1490,440,-9,'#f7dda2'),(1214,1610,610,7,'#9dd8cf'),(1222,1720,785,-5,'#f0b38b')]
s=Session(BASE/'generated/effectcraft-edit-v015/Let-the-Phone-Book-Sing-editable-v015.ecproj')
layers=[]
def keys(lid,path,values):
 s.call('add_keyframe',dict(layer=lid,path=path,keys=[dict(time=f/24,value=v) for f,v in values],interpolation='linear'))
try:
 s.command('comp.open',{'comp':675})
 for i,(f,x,y,angle,color) in enumerate(events):
  lid=s.command('layer.newText',dict(name=f'Penny echo 10 — score stamp {i+1}',text='10',font='Arial Bold Italic',size=150,fill=color,position=[x,y],justify='center'))['layer'];layers.append(lid)
  s.command('layer.style.stroke',{'layers':[lid]})
  s.call('set_property',dict(layer=lid,path='layerStyles/stroke/color',value='#292536'))
  s.call('set_property',dict(layer=lid,path='layerStyles/stroke/size',value=5))
  s.command('layer.timing',{'layers':[lid],'out':1232/24})
  s.command('layer.timing',{'layers':[lid],'in':f/24})
  keys(lid,'transform/position',[(f,[x-30,y-60,0]),(f+2,[x,y,0]),(f+5,[x,y-9,0]),(f+7,[x,y,0]),(1232,[x,y,0])])
  keys(lid,'transform/scale',[(f,[125,145,100]),(f+2,[112,72,100]),(f+4,[87,112,100]),(f+7,[100,100,100]),(1232,[96,96,100])])
  keys(lid,'transform/rotation',[(f,angle-10),(f+2,angle+3),(f+6,angle),(1232,angle)])
  pairs={f:0,f+1:100,1228:100,1229:80,1230:60,1231:30,1232:0}
  keys(lid,'transform/opacity',sorted(pairs.items()))
 s.command('comp.open',{'comp':1554})
 s.call('save_project',{'path':str(target)})
finally:s.close()
record=dict(status='draft_for_music_review',text='10',concept='Three comic perfect-score stamps beside Penny, punctuating satisfied throw reaction. No narrator orbit or floating-word arc.',events=[dict(masterFrame=e[0],masterSeconds=e[0]/24,position=list(e[1:3])) for e in events],timingMethod='Approximate stereo waveform matching around 50.23,50.59,50.915 seconds, rounded to24fps. Final sync subject to listening review.',layers=layers,nativeProject=str(target.relative_to(BASE)),previousProject='generated/effectcraft-edit-v015/Let-the-Phone-Book-Sing-editable-v015.ecproj')
(BASE/'production/penny-echo-v001.json').write_text(json.dumps(record,indent=2)+'\n')
print(layers)
