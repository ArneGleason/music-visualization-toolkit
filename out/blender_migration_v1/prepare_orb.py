"""Retain accepted oscillator/sampling math; export geometry, never FX pixels."""
import json,gzip,subprocess,numpy as np
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'orb';D.mkdir(exist_ok=True)
shape=(R/'out/colony_world_blossom_v2/shape.py').read_text()
shape=shape.replace('light=np.zeros((720,1280,3),np.float32)','paths=[]')
shape=shape.replace('energy=np.zeros((720,1280),np.float32)','energy=None').replace('sample=np.zeros_like(energy)','sample=None')
old='cv2.line(sample,tuple(np.rint(xy[j]).astype(int)),tuple(np.rint(xy[q]).astype(int)),float(intensity),2 if xyz[j,2]<0 else 3,cv2.LINE_AA)'
new="paths.append([list(map(float,xy[j])),list(map(float,xy[q])),2 if xyz[j,2]<0 else 3,float(intensity)/len(offsets),side])"
assert old in shape;shape=shape.replace(old,new)
old='cv2.circle(sample,tuple(pos.astype(int)),1 if k%3 else 2,float(brightness),-1,cv2.LINE_AA)'
new="paths.append([[float(pos[0]-.5),float(pos[1])],[float(pos[0]+.5),float(pos[1])],2 if k%3 else 4,float(brightness)/len(offsets),side])"
assert old in shape;shape=shape.replace(old,new).replace('            energy+=sample/len(offsets)','')
shape=shape[:shape.index('        trail[side]=')]+ '\n    return paths\n'
ns={};exec(compile(shape,'native_numeric_orb','exec'),ns);draw=ns['draw']
builder=(R/'out/colony_world_blossom_v2/render.py').read_text().split("exec(compile(s,str(p),'exec')")[0]
bns={'__file__':str(R/'out/colony_world_blossom_v2/render.py')};exec(compile(builder,'orb_recipe_builder','exec'),bns)
code=bns['s'];code=code[:code.index('    pic=f.astype')]
code=code.replace("(OUT/'frames').mkdir(exist_ok=True)",'')
code=code.replace("cap=cv2.VideoCapture(str(ROOT/'clips/raw/mars_domes_wide_v6.mp4'));cap.set(cv2.CAP_PROP_POS_FRAMES,12)",'')
code=code.replace('    ok,f=cap.read();assert ok','')
code+='\n    captured.append(light)\n    diagnostics.append({"song_frame":sf,"vocal_level":level,"guitar_level":guitar_level,"spin":float(spin)})\n'
captured=[];diagnostics=[]
exec(compile(code,'accepted_oscillator_geometry','exec'),{'__file__':str(O/'prepare_orb.py'),'draw':draw,'captured':captured,'diagnostics':diagnostics})
with gzip.open(D/'segments.json.gz','wt') as f:json.dump(captured,f)
(D/'controls.json').write_text(json.dumps({'song_frames':[2271,2399],'frames':diagnostics},indent=2))
(D/'plates').mkdir(exist_ok=True)
if not (D/'plates/0128.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/'clips/raw/mars_domes_wide_v6.mp4'),'-vf','trim=start_frame=12:end_frame=140,setpts=PTS-STARTPTS',str(D/'plates/%04d.png')],check=True)
print('Captured',len(captured),'frames of native geometry.')
