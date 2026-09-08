"""Extract numerical sprite paths and existing tracks, never raster FX inputs."""
from pathlib import Path
import json,gzip,subprocess,numpy as np
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'message'; (D/'plates').mkdir(parents=True,exist_ok=True)
tracking=json.loads((R/'out/receiver_now_v3/tracking.json').read_text())['frames']
tracks={v['song_frame']:v for v in tracking}; assert len(tracks)==119
h=json.loads((R/'out/receiver_reply_arrival_v1/handoff.json').read_text())
sources=[{'file':'out/assembly_cfr/synced_49bb1ee673385c931ee7.mp4','source_frames':[72,183],'song_frames':[971,1082]}, {'file':h['output']['base'],'source_frames':[12,131],'song_frames':[1082,1201]}]
for source,offset in zip(sources,[0,111]):
    a,z=source['source_frames']; assert z-a==source['song_frames'][1]-source['song_frames'][0]
    if not (D/'plates'/f'{offset+z-a:04d}.png').exists():
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/source['file']),'-vf',f'trim=start_frame={a}:end_frame={z},setpts=PTS-STARTPTS','-frames:v',str(z-a),'-start_number',str(offset+1),str(D/'plates/%04d.png')],check=True)
# Retain the tested audio folding algorithm, stop before any pixel drawing.
p=R/'out/rosette_duet_trial/render.py'; code=p.read_text().split('  energy=np.zeros((720,1280),np.float32)')[0]
code=code.replace('  self.trail=np.zeros((720,1280),np.float32)','')
code=code.replace('if t<0:return np.zeros((720,1280,3),np.float32),None','if t<0:return None')
needle='  # Peripheral paths allow frame-edge clipping, never transit across her face.'
code=code.replace(needle,'''  if songframe>=1082:
   u=(songframe-1082)/24; mix=smooth(u/1.45)
   target=np.array([640+(260 if self.side==1 else -260)+65*np.cos(u*1.5+self.side*np.pi),335+95*np.sin(u*1.5+self.side*np.pi)])
   target=current_transform@np.array([*target,1.])
   x=x*(1-mix)+target[0]*mix; y=y*(1-mix)+target[1]*mix; scale=scale*(1-.35*mix)
''')
code+='''  bind=smooth((songframe-1110)/20)
  if bind>0:
   cx=425 if self.side==0 else 832; theta=angle+t*.8
   wiggle=np.tile(self.radial-self.radial.mean(),3)*.18
   bound=np.stack([cx+(55+wiggle)*np.cos(theta),280+(55+wiggle)*np.sin(theta)],axis=1)
   bound=bound@current_transform[:,:2].T+current_transform[:,2]; xy=xy*(1-bind)+bound*bind
  level=self.level*smooth(t/.12)*(.78 if not active else 1)
  dwell=1/(1+np.linalg.norm(np.roll(xy,-1,axis=0)-xy,axis=1)*.17)
  weight=(.75+.25*((np.arange(768)/768-t*.55)%1))*level*dwell
  return {'xy':xy.tolist(),'energy':weight.tolist(),'width':max(1,round(scale*.6)),'side':self.side,'kind':'sprite','closed':True}
'''
ns={'__file__':str(p),'current_transform':np.eye(2,3)}; exec(compile(code,str(p),'exec'),ns)
sprites=[ns['Sprite'](1030,1060,0,[1,.8,.2]),ns['Sprite'](1060,1082,1,[.1,.5,1])]
def pulse(sf):
    t=sf-1175; return 0 if t<0 else float((1-np.exp(-t/1.1))*np.exp(-max(0,t-3)/12))
def path(xy,energy,width,side,kind,matrix,closed=False):
    xy=np.asarray(xy)@matrix[:,:2].T+matrix[:,2]
    return {'xy':xy.tolist(),'energy':np.broadcast_to(energy,len(xy)).tolist(),'width':width,'side':side,'kind':kind,'closed':closed}
def hardware(sf,matrix,voice):
    result=[]; pu=pulse(sf)
    for side in range(2):
        for cx,cy,rx,ry,start,span in [(628,260,113,113,1137,30),(370 if side==0 else 890,450,55,55,1150,28)]:
            progress=np.clip((sf-start)/span,0,1)
            if progress<=0:continue
            theta=np.linspace(0,np.pi if start==1137 else 2*np.pi,320)+(np.pi/2 if side==0 else -np.pi/2)
            if side==1:theta=-theta
            ripple=(1+5*pu)*(np.sin(theta*17+sf*.25)+.5*np.sin(theta*37-sf*.18))
            xy=np.column_stack((cx+(rx+ripple)*np.cos(theta),cy+(ry+ripple)*np.sin(theta)))
            count=max(2,int(progress*len(xy))); phase=(np.arange(count)/320-(sf-start)/40)%1
            result.append(path(xy[:count],(.35+.65*phase**2)*(.5+.7*voice)*(1+2.2*pu),1,side,'hardware',matrix))
        if pu<=0:continue
        boundary=[]
        for cx,cy,start in [(998,120,-90),(998,637,0),(267,637,90),(267,120,180)]:
            theta=np.linspace(np.deg2rad(start),np.deg2rad(start+90),32); boundary.extend(np.column_stack((cx+25*np.cos(theta),cy+25*np.sin(theta))))
        points=[]
        for a,b in zip(boundary,boundary[1:]+boundary[:1]):points.extend(np.linspace(a,b,max(2,int(np.linalg.norm(b-a)/2)),endpoint=False))
        points=np.array(points); mix=np.clip((points[:,0]-590)/85,0,1); scan=.7+.3*((np.arange(len(points))/len(points)-(sf-1175)/28)%1)
        result.append(path(points,(1-mix if side==0 else mix)*pu*scan,2,side,'burst',matrix,True))
        for cx,cy,r in [(325 if side==0 else 935,178,53),(333 if side==0 else 927,270,27),(370 if side==0 else 890,604,38),(628,600,78)]:
            theta=np.linspace(0,2*np.pi,320); radius=r+pu*3*np.sin(theta*13+sf*.4)
            xy=np.column_stack((cx+radius*np.cos(theta),cy+radius*np.sin(theta)))
            energy=pu*(.55+.45*((np.arange(320)/320-sf/24)%1))*(.5 if cx==628 else 1)
            result.append(path(xy,energy,2,side,'burst',matrix))
    return result
rows=[]; geometry=[]
for sf in range(971,1201):
    track=tracks.get(sf); matrix=np.array(track['transform']) if track else np.eye(2,3); ns['current_transform']=matrix
    inverse=np.linalg.inv(np.vstack((matrix,[0,0,1])))
    rows.append({'song_frame':sf,'voice':track['voice'] if track else 0,'receiver':bool(track),'inverse':inverse.tolist()})
    subs=[]
    for sub in range(2):
        at=sf+(sub+.5)/2; paths=[]
        for sprite in sprites:
            record=sprite.render(at)
            if record:paths.append(record)
        if track:paths+=hardware(at,matrix,track['voice'])
        subs.append(paths)
    geometry.append(subs)
(D/'controls.json').write_text(json.dumps({'fps':24,'song_frames':[971,1201],'sources':sources,'frames':rows,'decay_per_subsample':.55,'subsamples':2},indent=2))
with gzip.open(D/'paths.json.gz','wt') as f:json.dump(geometry,f)
(D/'continuation_state.json').write_text(json.dumps({'next_song_frame':1201,'sprites':[{'period':float(s.period),'radial':s.radial.tolist(),'level':float(s.level)} for s in sprites],'history':'paths.json.gz contains preceding geometric history; resume both subsamples in order'},indent=2))
print('Prepared230 frames, exact audio curves and receiver tracks; no FX raster input.')
