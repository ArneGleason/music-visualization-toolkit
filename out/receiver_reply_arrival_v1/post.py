"""Verify plate, carry approved duet state, track vocal meter, render context."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'out/receiver_reply_arrival_review'
OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
def run(args,**kw): subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
hp=ROOT/'out/receiver_reply_arrival_v1/handoff.json'
h=json.loads(hp.read_text()); base=ROOT/h['output']['base']
assert hashlib.sha256(base.read_bytes()).hexdigest().upper()==h['claude_result']['base']['sha256']

# Reuse the actual approved oscillator, including captured phrase states and trails.
recipe=ROOT/'out/rosette_duet_trial/render.py'
code=recipe.read_text().split('sprites=[Sprite')[0]
code=code.replace('  # Peripheral paths allow frame-edge clipping, never transit across her face.', '''  if songframe>=1082:
   u=(songframe-1082)/24
   mix=smooth(u/1.45)
   # Ease from the original trajectory into receiver-relative loose orbits.
   target=np.array([640+(260 if self.side==1 else -260)+65*np.cos(u*1.5+self.side*np.pi),
                    335+95*np.sin(u*1.5+self.side*np.pi)])
   target=current_transform@np.array([target[0],target[1],1.])
   x=x*(1-mix)+target[0]*mix; y=y*(1-mix)+target[1]*mix
   scale=scale*(1-.35*mix)
  # Preserve scale and trajectory exactly at the cut, then recede towards radio.''')
code=code.replace('  light*=guard[None,:]', '  light*=((1-smooth((songframe-1082)/24))*guard+smooth((songframe-1082)/24))[None,:]')
ns={'__file__':str(recipe),'__name__':'rosette_library','current_transform':np.eye(2,3)}
exec(compile(code,str(recipe),'exec'),ns)
sprites=[ns['Sprite'](1030,1060,0,[1.,.80,.20]),ns['Sprite'](1060,1082,1,[.10,.50,1.])]
for frame in range(1030,1082):
 for sub in range(2):
  for s in sprites:s.render(frame+(sub+.5)/2)

local=json.loads((ROOT/'projects/rivers-of-mars/project.local.json').read_text())
stem=list(Path(local['sources']['stems']).glob('*Lead Vocal*restored.wav'))
assert len(stem)==1
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(stem[0]),
 '-ac','1','-af','highpass=f=80,lowpass=f=5000,aresample=12000','-f','f32le','-']),dtype='<f4')
times=np.arange(1082/24-.25,1201/24, .001);rms=[]
for t in times:
 i=round((t-.178348)*12000);chunk=audio[i-60:i+61]
 rms.append(float(np.sqrt(np.mean(chunk*chunk))))
floor=10**(-48/20);ref=max(np.quantile(rms,.95),floor*2)
target=np.clip((np.array(rms)-floor)/(ref-floor),0,1)**.75
env=[];value=0.
for x in target:
 value+=(1-np.exp(-.001/(.008 if x>value else .065)))*(x-value);env.append(value)

cap=cv2.VideoCapture(str(base));assert cap.get(cv2.CAP_PROP_FPS)==24 and cap.get(cv2.CAP_PROP_FRAME_COUNT)==192
ok,first=cap.read();assert ok
gray0=cv2.cvtColor(first,cv2.COLOR_BGR2GRAY)
featuremask=np.zeros_like(gray0);featuremask[90:650,270:1010]=255
points=cv2.goodFeaturesToTrack(gray0,400,.01,8,mask=featuremask)
yy,xx=np.mgrid[:720,:1280]
mask=((((xx-640)/163)**2+((yy-557)/153)**2<1)&(yy<536)).astype(np.float32)
mask=cv2.GaussianBlur(mask,(0,0),1.4)
outframes=OUT/'frames';outframes.mkdir(exist_ok=True)
records=[]
for f in range(1,131):
 ok,frame=cap.read();assert ok
 if f<12:continue
 gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
 tracked,valid,_=cv2.calcOpticalFlowPyrLK(gray0,gray,points,None,winSize=(31,31),maxLevel=4)
 a=points[valid.ravel()==1].reshape(-1,2);b=tracked[valid.ravel()==1].reshape(-1,2)
 matrix,inliers=cv2.estimateAffinePartial2D(a,b,method=cv2.RANSAC,ransacReprojThreshold=2)
 assert matrix is not None and inliers.sum()>20
 residual=np.linalg.norm(a@matrix[:,:2].T+matrix[:,2]-b,axis=1)[inliers.ravel()==1]
 assert np.median(residual)<2
 ns['current_transform']=matrix
 trackedmask=cv2.warpAffine(mask,matrix,(1280,720))
 pixel=frame.astype(np.float32)/255
 trackedmask*=np.clip((pixel[:,:,2]-pixel[:,:,0]-.12)*4,0,1)
 songframe=1070+f;voice=float(np.interp((songframe+.5)/24,times,env))
 strength=.035+2.8*voice
 linear=np.where(pixel<=.04045,pixel/12.92,((pixel+.055)/1.055)**2.4)
 halo=(cv2.GaussianBlur(trackedmask,(0,0),10)*.18+cv2.GaussianBlur(trackedmask,(0,0),30)*.10)*strength
 linear+=linear*trackedmask[:,:,None]*strength*.65+halo[:,:,None]*np.array([.10,.46,1.])
 linear=np.clip(linear,0,1)
 lit=np.where(linear<=.0031308,linear*12.92,1.055*linear**(1/2.4)-.055)
 result=np.zeros_like(lit);states=[]
 for sub in range(2):
  glow=np.zeros_like(lit)
  for s in sprites:
   light,state=s.render(songframe+(sub+.5)/2);glow+=light
   if sub==1:states.append(state)
  result+=np.clip(lit+glow,0,1)*.5
 cv2.imwrite(str(outframes/f'{f-12:04d}.png'),np.rint(result*255).astype(np.uint8))
 records.append({'song_frame':songframe,'source_frame':f,'transform':matrix.tolist(),
  'inliers':int(inliers.sum()),'median_error_px':float(np.median(residual)),
  'voice':voice,'sprites':states})
cap.release()
assert len(records)==119
run(['ffmpeg','-v','error','-y','-framerate','24','-i',outframes/'%04d.png','-an',
 '-c:v','libx264','-crf','17','-pix_fmt','yuv420p',OUT/'clean.mp4'])
(OUT/'tracking.json').write_text(json.dumps({'frames':records,'stem_offset':.178348,
 'source_origin_frame':1070,'song_frames':[1082,1201]},indent=2))

edl=json.loads((ROOT/'out/rosette_sprite_trial/shotlist.json').read_text())
cues=json.loads((ROOT/'out/rosette_sprite_trial/overlay_cues.json').read_text())
shot=dict(next(s for s in edl['shots'] if s['id']=='s010'))
shot.update(id='receiver_reply_arrival',start_sec=1082/24,end_sec=1201/24,dur_sec=119/24,frames=119,
 clip={'file':'out/receiver_reply_arrival_review/clean.mp4','in_sec':0,'speed':1})
edl['shots'].append(shot)
cue=dict(next(c for c in cues['shots'] if c['id']=='s010'))
cue.update(id='receiver_reply_arrival',start=1082,end=1201);cues['shots'].append(cue)
edl['duration_sec']=cues['duration_sec']=1201/24;cues['frames']=1201
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'blender.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1',
 '-P',ROOT/'out/receiver_reply_arrival_v1/blender_review.py','--','--proxy','--start','1082','--end','1200',
 '--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',ROOT/'out/rosette_duet_trial/preview.mp4','-i',OUT/'raw.mp4',
 '-i',ROOT/'audio/song.wav','-filter_complex',
 '[0:v]trim=end_frame=111,setpts=N/(24*TB)[a];[1:v]trim=end_frame=119,setpts=N/(24*TB)[b];[a][b]concat=n=2:v=1:a=0[v];[2:a]atrim=start=40.458333333333:end=50.041666666667,asetpts=PTS-STARTPTS[audio]',
 '-map','[v]','-map','[audio]','-frames:v','230','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',
 '-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
h['status']='codex_verified_ready_for_owner_review'
h['codex_result']={'hash_verified':True,'native_fps':24,'frames':192,'source_used':[12,131],
 'preview':'out/receiver_reply_arrival_review/preview.mp4','preview_song_frames':[971,1201],
 'clean':'out/receiver_reply_arrival_review/clean.mp4','owner_approval':'pending',
 'max_median_tracking_error_px':max(r['median_error_px'] for r in records),
 'note':'Push stronger than requested. Fresh vocal-meter response and carried duet; production unchanged.'}
hp.write_text(json.dumps(h,indent=2)+'\n')
print(json.dumps(h['codex_result'],indent=2))
