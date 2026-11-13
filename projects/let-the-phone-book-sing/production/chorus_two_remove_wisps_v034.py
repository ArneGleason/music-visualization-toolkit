"""Analyze native alpha islands; remove them with editable per-frame native masks.
Python only measures alpha. All masking and final pixels are rendered by EffectCraft.
"""
import json
import numpy as np
from PIL import Image
from scipy import ndimage
from effectcraft_session import Session,BASE
out=BASE/'generated/effectcraft-edit-v034';out.mkdir(parents=True,exist_ok=True)
target=out/'Let-the-Phone-Book-Sing-editable-v034.ecproj'
if target.exists():raise SystemExit('Preserve v034')
s=Session(BASE/'generated/effectcraft-edit-v033/Let-the-Phone-Book-Sing-editable-v033.ecproj')
records=[]
try:
 for f in range(1619,1901):
  sample=out/'analysis-alpha.png'
  s.call('render_frame',{'comp':19862,'time':f/24,'path':str(sample),'transparent':True,'inline':False,'max_side':1920})
  a=np.asarray(Image.open(sample))[:,:,3]
  labels,n=ndimage.label(a>8)
  sizes=np.bincount(labels.ravel());sizes[0]=0
  main=int(sizes.argmax());mainmask=labels==main
  protected=ndimage.binary_dilation(mainmask,iterations=2)
  rects=[]
  for i,sl in enumerate(ndimage.find_objects(labels),1):
   if sl is None or i==main or sizes[i]<3 or sizes[i]>2500:continue
   y,x=sl
   if y.stop>550:continue
   x0,x1=max(0,x.start-2),min(1920,x.stop+2);y0,y1=max(0,y.start-2),min(1080,y.stop+2)
   if protected[y0:y1,x0:x1].any():continue
   rects.append([x0,y0,x1,y1])
  records.append({'frame':f,'rects':sorted(rects,key=lambda r:(r[0],r[1]))})
  if f%48==0:print('Analyzed',f,flush=True)
 (out/'island-analysis.json').write_text(json.dumps(records))
 s.command('comp.open',{'comp':19864})
 singer=next(l['id'] for l in s.call('get_comp',{'comp':19864})['layers'] if l['name']=='Approved narrator B — original plate framing')
 count=max(len(r['rects']) for r in records)
 def shape(rect):
  x0,y0,x1,y1=rect
  return {'t':'Path','v':{'closed':True,'vertices':[[x0,y0],[x1,y0],[x1,y1],[x0,y1]],'in_tangents':[[0,0]]*4,'out_tangents':[[0,0]]*4}}
 for k in range(count):
  off=[-20,-20,-10,-10]
  s.command('mask.new',{'layer':singer,'vertices':shape(off)['v']['vertices'],'closed':True,'mode':'Subtract'})
  prop=f'masks/#{k+1}'
  s.call('set_property',{'layer':singer,'path':prop+'/feather','value':[.35,.35]})
  keys=[{'time':r['frame']/24,'value':shape(r['rects'][k] if k<len(r['rects']) else off)} for r in records]
  s.call('add_keyframe',{'layer':singer,'path':prop+'/path','keys':keys,'interpolation':'hold'})
 s.call('save_project',{'path':str(target)})
 for f in [1634,1690,1750,1820]:s.call('render_frame',{'comp':1554,'time':f/24,'path':str(out/f'check-{f}.png'),'inline':False,'max_side':1920})
 print('Masks',count,'frames with islands',sum(bool(r['rects']) for r in records),flush=True)
 (BASE/'production/chorus-two-wisp-removal-v001.json').write_text(json.dumps({'status':'pending_review','nativeProject':str(target.relative_to(BASE)),'maskLayer':singer,'maskCount':count,'frames':[1619,1901],'method':'Measure disconnected alpha islands above y550; subtract padded rectangles only when safely separated from main silhouette. Native hold-keyed masks on final singer precomp, after key and outline.','analysis':'generated/effectcraft-edit-v034/island-analysis.json'},indent=2)+'\n')
finally:s.close()
