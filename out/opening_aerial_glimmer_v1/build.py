"""Tracked garden signal and music-responsive architecture, additive Blender layer."""
from pathlib import Path
import json, subprocess, sys, shutil
import numpy as np

ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2

def run(args,**kw):
    subprocess.run([str(a) for a in args],cwd=ROOT,check=True,**kw)

frames_dir=OUT/'lights'; frames_dir.mkdir(exist_ok=True)
cap=cv2.VideoCapture(str(ROOT/'out/opening_aerial_flow_v1/base.mp4'))
frames=[]
for n in range(77):
    ok,frame=cap.read(); assert ok
    frames.append(frame)
cap.release()
# Local textured neighborhoods, tracked incrementally. Not a solved 3D camera.
anchors=np.array([[754,418],[672,435],[833,507]],np.float32)
positions=[anchors.copy()]; failures=[]; valid_until=[76,76,76]
for n in range(1,77):
    prev=cv2.cvtColor(frames[n-1],cv2.COLOR_BGR2GRAY)
    curr=cv2.cvtColor(frames[n],cv2.COLOR_BGR2GRAY)
    nextanchors=[]
    for k,(x,y) in enumerate(positions[-1]):
        if n>valid_until[k]:
            nextanchors.append([x,y]);continue
        mask=np.zeros_like(prev);cv2.circle(mask,(int(x),int(y)),22,255,-1)
        pts=cv2.goodFeaturesToTrack(prev,40,.01,3,mask=mask)
        assert pts is not None and len(pts)>=4,(n,k)
        moved,status,_=cv2.calcOpticalFlowPyrLK(prev,curr,pts,None,winSize=(25,25),maxLevel=3)
        back,backstatus,_=cv2.calcOpticalFlowPyrLK(curr,prev,moved,None,winSize=(25,25),maxLevel=3)
        good=(status.ravel()==1)&(backstatus.ravel()==1)&(np.linalg.norm(back-pts,axis=2).ravel()<1.2)
        if good.sum()<3:
            assert k!=0, 'Garden track lost'
            valid_until[k]=n-1;failures.append([n,k]);nextanchors.append([x,y]);continue
        delta=np.median((moved-pts).reshape(-1,2)[good],axis=0)
        nextanchors.append([x+delta[0],y+delta[1]])
    positions.append(np.array(nextanchors))
positions=np.array(positions)
# Master amplitude at the exact song position, no imported/generated audio.
pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'audio/song.wav'),'-f','f32le','-ac','1','-ar','24000','-'])
audio=np.frombuffer(pcm,dtype=np.float32)
energy=np.array([np.sqrt(np.mean(audio[(205+i)*1000:(206+i)*1000]**2)) for i in range(77)])
energy=np.convolve(energy,[.2,.6,.2],mode='same')
energy=np.clip(energy/(np.percentile(energy,90)+1e-9),0,1)
candidates=[i for i in range(12,65) if energy[i]>=energy[i-1] and energy[i]>energy[i+1]]
peaks=[]
for i in sorted(candidates,key=lambda j:-energy[j]):
    if all(abs(i-j)>=12 for j in peaks): peaks.append(i)
    if len(peaks)==2:break
assert peaks
yy,xx=np.mgrid[0:720,0:1280]
strengths=[]
for n in range(77):
    layer=np.zeros((720,1280,3),np.float32)
    gate=min(1,n/7,(76-n)/8)
    pulse=sum(np.exp(-.5*((n-p)/(2.1 if n<p else 4.2))**2) for p in peaks)
    strengths.append(float(pulse))
    for k,(x,y) in enumerate(positions[n]):
        visibility=max(0,min(1,(valid_until[k]-n)/6))
        r2=(xx-x)**2+(yy-y)**2
        if k==0:
            # Small leaf-green emitter with a softer, wider spill, not a floating orb.
            intensity=gate*(.025+.9*pulse)
            shape=np.exp(-r2/(2*1.65**2))+.17*np.exp(-r2/(2*7.0**2))+.025*np.exp(-r2/(2*15**2))
            color=np.array([65,240,110],np.float32) # BGR
        else:
            intensity=gate*(.025+.36*energy[n]**2)
            shape=np.exp(-r2/(2*1.4**2))+.2*np.exp(-r2/(2*4.4**2))
            color=np.array([105,184,245] if k==1 else [190,214,135],np.float32)
        layer+=shape[:,:,None]*color*intensity*visibility
    cv2.imwrite(str(frames_dir/f'{n:03}.png'),np.uint8(np.clip(layer,0,255)))

(OUT/'tracking.json').write_text(json.dumps({'initial_points':anchors.tolist(),'positions':positions.tolist(),'garden_peak_source_frames':peaks,'garden_peak_song_frames':[205+p for p in peaks],'driver':'master RMS, exact song clock','strengths':strengths,'tracking':'local sparse optical flow, forward/backward checked'},indent=2))
# Diagnostic sheet showing the intended anchoring, not part of the preview.
tiles=[]
for n in [0,24,48,76]:
    im=frames[n].copy()
    for k,pt in enumerate(positions[n]):cv2.circle(im,tuple(np.round(pt).astype(int)),9,(0,255,0) if k==0 else (0,180,255),1)
    cv2.putText(im,f'source {n}',(20,35),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    tiles.append(cv2.resize(im,(640,360)))
cv2.imwrite(str(OUT/'tracking_check.jpg'),np.vstack([np.hstack(tiles[:2]),np.hstack(tiles[2:])]))
for name in ['shotlist.json','overlay_cues.json']:
    shutil.copy2(ROOT/'out/opening_aerial_review_v1'/name,OUT/name)
adapter=(ROOT/'out/opening_aerial_review_v1/blender_review.py').read_text().replace('opening_aerial_review_v1','opening_aerial_glimmer_v1')
injection="""    lightdir = ROOT / 'out/opening_aerial_glimmer_v1/lights'
    light = strips.new_image(name='garden_signal_and_architecture', filepath=str(lightdir/'000.png'), channel=90, frame_start=B(205))
    for number in range(1,77): light.elements.append(f'{number:03}.png')
    light.frame_final_duration = 77
    light.blend_type = 'ADD'
    light.blend_alpha = 0.85
"""
adapter=adapter.replace("exec(compile(s,str(p),'exec')", "s=s.replace('    bpy.ops.render.render(animation=True)',"+repr(injection)+"+'    bpy.ops.render.render(animation=True)')\nexec(compile(s,str(p),'exec')")
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'render.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','155','--end','333','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={155/24}:end={334/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','179','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(OUT/'preview.mp4')]))['streams'][0]
assert int(info['nb_frames'])==179 and info['r_frame_rate']=='24/1'
(OUT/'verification.json').write_text(json.dumps({'preview_frames':[155,334],'fx_song_frames':[205,282],'source_unchanged':True,'layer':'77 additive light PNGs composited by Blender below lyrics','driver':'master amplitude','garden_peaks_song_frames':[205+p for p in peaks],'status':'owner review pending'},indent=2))
