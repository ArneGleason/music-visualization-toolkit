"""Extract the accepted continuous orb/encoding geometry and original plates."""
import json,gzip,subprocess,shutil,numpy as np
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'meaning';D.mkdir(exist_ok=True)
wrapper=(R/'out/meaning_orb_loop_v4/render.py').read_text().rsplit('exec(compile(source,',1)[0]
ns={'__file__':str(R/'out/meaning_orb_loop_v4/render.py')};exec(compile(wrapper,'meaning_builder','exec'),ns);code=ns['source']
code=code.replace('center=np.array([680-420*q,555-90*q])','center=np.array([680-340*q,555-25*q])')
code=code[:code.index('    trail=trail*.40')]
start=code.index('cap=cv2.VideoCapture');end=code.index('records=[]',start);code=code[:start]+code[end:]
start=code.index('    if shift<1280:');end=code.index('    center,radius=pose',start);code=code[:start]+code[end:]
code=code.replace('trail=np.zeros((720,1280,3),np.float32)','trail=None')
code=code.replace('light=np.zeros_like(trail);levels=[]',"light='payload';levels=[];current=[]")
code=code.replace('beam=np.zeros((720,1280),np.float32)',"beam='beam'")
code=code.replace('        light+=beam[:,:,None]*color','')
code=code.replace('cv2.line(','record_line(').replace('cv2.circle(','record_circle(')
code+='\n    captured.append(current)\n    records.append({"song_frame":sf,"shift":shift,"center":center.tolist(),"radius":float(radius),"levels":levels})\n'
g={'__file__':str(O/'prepare_meaning.py'),'captured':[]}
def record_line(target,p,q,color,width,*unused):
 if target=='beam':side=g['side'];energy=float(color)
 else:
  side=0 if color[0]>color[2] else 1;energy=float(color[0] if side==0 else color[2])
 g['current'].append([list(map(float,p)),list(map(float,q)),width,energy,side])
def record_circle(target,p,r,color,*unused):record_line(target,(p[0]-.5,p[1]),(p[0]+.5,p[1]),color,2*r)
g.update(record_line=record_line,record_circle=record_circle);exec(compile(code,'meaning_geometry','exec'),g)
with gzip.open(D/'segments.json.gz','wt') as f:json.dump(g['captured'],f)
(D/'controls.json').write_text(json.dumps({'song_frames':[2658,2881],'frames':g['records']},indent=2))
for name,file,first,last in [('outgoing','out/meaning_exchange_live_v5/astronaut_24.mp4',12,180),('incoming','out/meaning_exchange_dual_sync_v6/astronomer_combined.mp4',12,107)]:
 folder=D/name;folder.mkdir(exist_ok=True)
 if not (folder/f'{last-first:04d}.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/file),'-vf',f'trim=start_frame={first}:end_frame={last},setpts=PTS-STARTPTS',str(folder/'%04d.png')],check=True)
 # Shader image users can request frame zero before this panel is visible.
 # Hold original first frame there; it remains hidden by the fixed-domain split.
 if not (folder/'0000.png').exists():shutil.copyfile(folder/'0001.png',folder/'0000.png')
print('Captured',len(g['captured']),'continuous exchange frames.')
