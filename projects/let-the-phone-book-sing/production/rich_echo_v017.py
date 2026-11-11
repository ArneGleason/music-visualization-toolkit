"""Native EffectCraft numeral stamps: Rich receives an absurd golf score."""
import json
from effectcraft_session import Session, BASE
out = BASE/'generated/effectcraft-edit-v017'
out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v017.ecproj'
if target.exists(): raise SystemExit('Preserve v017')
# Approximate repeat attacks from local normalized waveform matching, rounded to grid.
events=[(1321,270,650,-7,'#f7dda2'),(1330,320,785,6,'#9dd8cf'),(1338,370,920,-4,'#f0b38b')]
s=Session(BASE/'generated/effectcraft-edit-v016/Let-the-Phone-Book-Sing-editable-v016.ecproj')
layers=[]
def keys(lid,path,values):
 s.call('add_keyframe',dict(layer=lid,path=path,keys=[dict(time=f/24,value=v) for f,v in values],interpolation='linear'))
try:
 s.command('comp.open',{'comp':675})
 for i,(f,x,y,angle,color) in enumerate(events):
  lid=s.command('layer.newText',dict(name=f'Rich echo 1,000 — score stamp {i+1}',text='1,000',font='Arial Bold Italic',size=108,fill=color,position=[x,y],justify='center'))['layer'];layers.append(lid)
  s.command('layer.style.stroke',{'layers':[lid]})
  s.call('set_property',dict(layer=lid,path='layerStyles/stroke/color',value='#292536'))
  s.call('set_property',dict(layer=lid,path='layerStyles/stroke/size',value=5))
  s.command('layer.timing',{'layers':[lid],'out':1357/24})
  s.command('layer.timing',{'layers':[lid],'in':f/24})
  keys(lid,'transform/position',[(f,[x-30,y-60,0]),(f+2,[x,y,0]),(f+5,[x,y-9,0]),(f+7,[x,y,0]),(1357,[x,y,0])])
  keys(lid,'transform/scale',[(f,[125,145,100]),(f+2,[112,72,100]),(f+4,[87,112,100]),(f+7,[100,100,100]),(1357,[96,96,100])])
  keys(lid,'transform/rotation',[(f,angle-10),(f+2,angle+3),(f+6,angle),(1357,angle)])
  pairs={f:0,f+1:100,1353:100,1354:80,1355:60,1356:30,1357:0}
  keys(lid,'transform/opacity',sorted(pairs.items()))
 s.command('comp.open',{'comp':1554})
 s.call('save_project',{'path':str(target)})
finally:s.close()
record=dict(status='draft_for_music_review',text='1,000',concept='Three absurd golf-score stamps on open left green; same visual bookend as Penny, clear of throw and cat.',events=[dict(masterFrame=e[0],masterSeconds=e[0]/24,position=list(e[1:3])) for e in events],timingMethod='Approximate stereo waveform matching around 55.05,55.395,55.746 seconds, rounded to24fps. Final sync subject to listening review.',layers=layers,nativeProject=str(target.relative_to(BASE)),previousProject='generated/effectcraft-edit-v016/Let-the-Phone-Book-Sing-editable-v016.ecproj')
(BASE/'production/rich-echo-v001.json').write_text(json.dumps(record,indent=2)+'\n')
print(layers)
