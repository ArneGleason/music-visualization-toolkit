"""Four later TV cuts, using each take's own glass geometry and source clock."""
import json,gzip,subprocess,shutil,math,numpy as np,sys
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'tv_late';(D/'plates').mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
def sm(a,b,t):u=np.clip((t-a)/(b-a),0,1);return u*u*(3-2*u)
beats=[v for bar in json.loads((R/'analysis/beatmap.json').read_text())['bars'] for v in bar['beats']]
def beat_power(t):return max([math.exp(-max(0,t-b)/.17)*sm(-.04,0,t-b) for b in beats if -.04<=t-b<.9]+[0.0])
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'audio/song.wav'),'-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
env=np.array([np.sqrt(np.mean(audio[i*1000:(i+1)*1000]**2)) for i in range(4782)]);env=np.clip(env/(np.percentile(env[4362:4782],85)+1e-8),0,1)
script=(R/'out/outro_additive_green_v1/build.py').read_text();script=script[script.index('def tv('):script.index('def tooth(')]
script=script[:script.index('    H=cv2.getPerspectiveTransform')]+ '\n    return current,q\n'
script=script.replace('im=np.zeros((S,S,3),np.float32)','im=None;current=[]')
script=script.replace('cv2.polylines(im,','record_poly(current,').replace('cv2.circle(im,','record_circle(current,').replace('cv2.line(im,','record_line(current,')
script=script.replace('    im+=cv2.GaussianBlur(im,(0,0),3)*(1.1+p)','')
script=script.replace('        im=cv2.warpAffine(im,transform,(S,S))','        current=[([sx*(a[0]-200)+200,sy*(a[1]-200)+200],[sx*(z[0]-200)+200,sy*(z[1]-200)+200],width,color) for a,z,width,color in current]')
script=script.replace('        im*=1-sm(4663,4671,song)','        current=[(a,z,width,[c*(1-sm(4663,4671,song)) for c in color]) for a,z,width,color in current]')
script=script.replace('        im+=cv2.GaussianBlur(im,(0,0),4)*2','')
def record_line(current,a,z,color,width,*unused):current.append((list(a),list(z),width,list(color)))
def record_poly(current,arrays,closed,color,width,*unused):
 for pts in arrays:
  for a,z in zip(pts,np.roll(pts,-1,axis=0) if closed else pts[1:]):record_line(current,a,z,color,width)
def record_circle(current,p,r,color,width,*unused):
 if width<0:record_line(current,[p[0]-.3,p[1]],[p[0]+.3,p[1]],color,2*r)
 else:record_poly(current,[np.array([[p[0]+r*math.cos(t),p[1]+r*math.sin(t)] for t in np.linspace(0,math.tau,65)])],False,color,width)
g=globals();exec(compile(script,'native_late_tv_paths','exec'),g)
cuts=[(59,4362,4400,2),(61,4431,4449,2),(63,4516,4538,3),(67,4644,4671,3)]
segments=[];rows=[];offset=0;uses=[]
for number,a,z,which in cuts:
 file='out/outro_A2_v2/take1/synced.mp4' if which==2 else 'out/outro_closing_generations_v1/A3/synced.mp4';origin=4320 if which==2 else 4492
 folder=D/str(number);folder.mkdir(exist_ok=True)
 if not (folder/f'{z-a:04d}.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/file),'-vf',f'fps=24,trim=start_frame={a-origin}:end_frame={z-origin},setpts=PTS-STARTPTS',str(folder/'%04d.png')],check=True)
 uses.append({'review_number':number,'song_frames':[a,z],'native_frames':[offset,offset+z-a],'source':file,'source_frames':[a-origin,z-origin]})
 for sf in range(a,z):
  current,q=tv(None,which,sf,sf>=4644);H=cv2.getPerspectiveTransform(np.float32([[0,0],[399,0],[399,399],[0,399]]),q);inv=np.linalg.inv(H);paths=[]
  def project(p):v=H@np.array([*p,1]);return v[:2]/v[2]
  for p,endpoint,width,color in current:
   aa=project(p);zz=project(endpoint);scale=np.linalg.norm(project(np.array(p)+[1,0])-aa);paths.append([aa.tolist(),zz.tolist(),max(.1,width*scale),1,[float(c/255) for c in color[::-1]]])
  segments.append(paths);rows.append({'song_frame':sf,'inverse':inv.tolist(),'shutdown':int(sf>=4644),'beat':beat_power(sf/24)})
  shutil.copyfile(folder/f'{sf-a+1:04d}.png',D/'plates'/f'{offset+sf-a+1:04d}.png')
 offset+=z-a
with gzip.open(D/'segments.json.gz','wt') as f:json.dump(segments,f)
(D/'controls.json').write_text(json.dumps({'frames':rows,'uses':uses},indent=2));print('Captured',offset,'late TV frames.')
