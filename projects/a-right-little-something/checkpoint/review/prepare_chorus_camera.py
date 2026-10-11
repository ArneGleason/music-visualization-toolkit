from pathlib import Path
import sys,json,shutil
sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import encode,probe
base=Path('projects/a-right-little-something').resolve()
spec=json.loads((base/'revision-chorus-v02.json').read_text(encoding='utf-8'))
entries=json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))['editProposals']['chorus-revision-v01']['entries']
out=base/spec['output'];old=base/'generated/storyboard/chorus-revision-v01'
for e in entries:
 if e['id']=='orbit-pullback':continue
 e.update(spec['entryOverrides'].get(e['id'],{}))
 count=e['renderFrames'];target=out/(e['id']+'.mp4')
 if e['id'] not in spec['cameraMoves']:
  shutil.copy2(old/target.name,target);continue
 move=spec['cameraMoves'][e['id']];path=base/e['path']
 if e.get('still'):
  args=['-loop','1','-framerate','24','-i',str(path)];filters='scale=1920:1080,setsar=1'
 else:
  lead=e['lead']-e['head'];args=['-i',str(path)];filters=f'fps=24,trim=start_frame={lead}:end_frame={lead+count},setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1'
 t=f'min(1,max(0,on/{count-1}))';ease=f'(({t})*({t})*(3-2*({t})))'
 def expr(v):return f'{v[0]}+({v[1]}-{v[0]})*{ease}'
 z,x,y=[expr(move[k]) for k in ('zoom','panX','panY')]
 filters+=f",scale=3840:2160,zoompan=z='{z}':x='(iw-iw/zoom)*({x})':y='(ih-ih/zoom)*({y})':d=1:s=1920x1080:fps=24"
 encode([*args,'-vf',filters],count,target)
 assert int(probe(target)['nb_frames'])==count
 print(e['id'],'ready',count,'frames',flush=True)
