"""Word-choreographed optical/spirograph punctuation on existing performance."""
import json,math,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'out/fx_tracking_deps')]
import cv2
from assembly_sources import load_decisions,resolve_clip,inspect_video
from assembly_timebase import conform_clip
from tracked_light_pilot import linear,display
def run(args,**kw):subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
def smooth(x):x=np.clip(x,0,1);return x*x*(3-2*x)
def hit(sf,on,width):return math.exp(-((sf-on)/width)**2)
edl=json.loads((ROOT/'out/swimmer_chorus_review_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/swimmer_chorus_review_v1/overlay_cues.json').read_text())
decisions=load_decisions(ROOT);pictures=[]
for ident in ['s045','s046']:
    shot=next(s for s in edl['shots'] if s['id']==ident)
    clip=conform_clip(ROOT,resolve_clip(ROOT,shot,24,decisions),24,prepare=True)
    cap=cv2.VideoCapture(str(ROOT/clip['file']));cap.set(cv2.CAP_PROP_POS_FRAMES,round(clip['in_sec']*24))
    for _ in range(shot['frames']):
        ok,p=cap.read();assert ok;pictures.append(p)
    cap.release()
assert len(pictures)==137
yy,xx=np.mgrid[:720,:1280].astype(np.float32)
dx=xx-640;dy=yy-270;rad=np.sqrt(dx*dx+(dy*1.10)**2)+.001
face=np.exp(-((dx/175)**4+((yy-280)/220)**4))
edge=np.exp(-((rad-310)/250)**2)*(1-face)*np.clip((620-yy)/90,0,1)
theta=np.linspace(0,2*np.pi,1100)
rng=np.random.default_rng(91);seeds=rng.random((180,5))
trail=np.zeros((720,1280,3),np.float32)
proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','24','-i','-','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',str(OUT/'clean.mp4')],stdin=subprocess.PIPE)
records=[]
for i,pic in enumerate(pictures):
    sf=3505+i;t=(sf-3513)/24
    buildup=float(smooth((sf-3513)/48))
    fade=float(1-smooth((sf-3618)/19))
    bend=hit(sf,3574,11);mind=hit(sf,3604,13)
    strength=(.18*buildup+.55*bend+.9*mind)*fade
    warp=(2*buildup+17*bend+27*mind)*fade
    wave=np.sin(rad/45-t*4)*warp*edge
    mx=(xx+dx/rad*wave).astype(np.float32);my=(yy+dy/rad*wave*.65).astype(np.float32)
    frame=cv2.remap(pic,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT101)
    # Small spectral splitting in the disturbed background; face remains unwarped.
    split=edge*strength*2.5
    for channel,sign in [(0,1),(2,-1)]:
        frame[:,:,channel]=cv2.remap(pic[:,:,channel],(mx+sign*split).astype(np.float32),my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT101)
    ink=np.zeros((1440,2560,3),np.float32)
    radius=185+110*buildup+85*mind
    for k,color in enumerate([(1.,.46,.68),(.95,.82,.20),(.32,.65,1.)]):
        phase=t*(.25 if k%2 else -.22)+k*2*np.pi/3
        lobes=5+k
        modulation=(.045+.11*bend+.19*mind)*np.sin(lobes*theta+phase*3)
        rr=radius*(1+modulation)
        x=640+rr*np.cos(theta+phase)
        y=275+.78*rr*np.sin(theta+phase)+22*mind*np.sin(3*theta-phase)
        points=np.rint(np.column_stack((x,y))*2).astype(np.int32)
        # Distinct scan head and lingering tail around the loop.
        for j in range(0,len(points)-1,12):
            scan=((j/len(points)-t*.24-k*.2)%1)
            energy=strength*(.45+.55*math.exp(-scan*4))
            cv2.polylines(ink,[points[j:j+14]],False,tuple(float(c*energy) for c in color),2,cv2.LINE_AA)
    for j,(a,b,c,d,e) in enumerate(seeds):
        age=max(0,(sf-3598)/24)
        angle=a*2*np.pi+t*(.14+b*.18)
        rr=radius*(.85+.30*c)+age*(70+130*d)
        x=640+rr*np.cos(angle);y=275+.78*rr*np.sin(angle)+age*age*25
        brightness=strength*(.15+.85*mind)*(.35+.65*e)
        color=(1.,.45,.75) if j%2 else (.55,.9,1.)
        cv2.circle(ink,(round(x*2),round(y*2)),1+int(c*3),tuple(float(v*brightness) for v in color),-1,cv2.LINE_AA)
    ink=cv2.resize(ink,(1280,720),interpolation=cv2.INTER_AREA)
    ink*=((1-.98*face)*np.clip((620-yy)/80,0,1))[:,:,None]
    trail=trail*.78+ink
    glow=trail*.8+cv2.GaussianBlur(trail,(0,0),3)*1.4+cv2.GaussianBlur(trail,(0,0),14)*1.1
    result=np.rint(display(linear(frame.astype(np.float32)/255)+glow)*255).astype(np.uint8)
    proc.stdin.write(result.tobytes())
    records.append({'song_frame':sf,'anticipation':buildup,'strength':strength,'warp_pixels':warp})
proc.stdin.close();assert proc.wait()==0
for ident,offset in [('s045',0),('s046',69)]:
    shot=next(s for s in edl['shots'] if s['id']==ident)
    shot['clip']={'file':'out/bends_mind_fx_v1/clean.mp4','in_sec':offset/24,'speed':1}
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues),('choreography.json',records)]: (OUT/name).write_text(json.dumps(data,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"bends_mind_fx_v1"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','3438','--end','3710','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={3438/24}:end={3711/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','273','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
assert inspect_video(str(OUT/'clean.mp4'))==(24.,137)
assert inspect_video(str(OUT/'preview.mp4'))==(24.,273)
(OUT/'verification.json').write_text(json.dumps({'preview_song_frames':[3438,3711],'clean_song_frames':[3505,3642],'anticipation_start':3513,'phrase_start':3561,'bends':3568,'mind':3598,'effect_end':3637,'status':'owner audition pending; existing lip sync retained'},indent=2))
print('Bends your mind FX preview ready.',flush=True)
