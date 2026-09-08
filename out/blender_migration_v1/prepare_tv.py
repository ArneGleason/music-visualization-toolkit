"""Capture accepted helix/map geometry and measured face-flash timing."""
import json,gzip,subprocess,numpy as np
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'tv';D.mkdir(exist_ok=True)
code=(R/'out/outro_tv_map_v2/build.py').read_text();code=code[:code.index('    trail=trail*.68')]
code=code.replace('LAYER=OUT/\'layers\'; LAYER.mkdir(exist_ok=True)','LAYER=None')
code=code.replace('im=np.zeros_like(trail)','im=None; current=[]')
code=code.replace('cv2.polylines(im,[np.round(pts).astype(np.int32)],False,tuple(float(v) for v in color),width,cv2.LINE_AA)','record_curve(pts,color,width)')
code=code.replace('cv2.circle(im,','record_circle(')
code+='\n    captured.append(current)\n'
g={'__file__':str(O/'prepare_tv.py'),'captured':[]}
def project(p):
 v=g['H']@np.array([p[0],p[1],1]);return v[:2]/v[2]
def record_curve(pts,color,width):
 color=[float(c/255) for c in color[::-1]]
 for p,q in zip(pts[:-1],pts[1:]):
  a=project(p);z=project(q);scale=np.linalg.norm(project(np.asarray(p)+[1,0])-a)
  g['current'].append([a.tolist(),z.tolist(),max(.2,width*scale),1,color])
def record_circle(p,r,color,thickness,*unused):
 points=np.array([[p[0]+r*np.cos(t),p[1]+r*np.sin(t)] for t in np.linspace(0,np.pi*2,33)])
 if thickness<0:
  record_curve(np.array([[p[0]-.3,p[1]],[p[0]+.3,p[1]]]),color,r*2)
 else:record_curve(points,color,thickness)
g.update(record_curve=record_curve,record_circle=record_circle);exec(compile(code,'tv_numeric_geometry','exec'),g)
with gzip.open(D/'segments.json.gz','wt') as f:json.dump(g['captured'],f)
(D/'controls.json').write_text(json.dumps({'frames':[{'song_frame':4165+i,'flash':float(g['flash'][i]),'voice':float(g['rms'][i])} for i in range(g['N'])],
 'source':str(g['source']),'inverse':g['inv'].tolist(),'quad':g['quad'].tolist()},indent=2))
(D/'plates').mkdir(exist_ok=True)
if not (D/'plates/0191.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(g['source']),str(D/'plates/%04d.png')],check=True)
print('Captured TV geometry on',g['N'],'frames.')
