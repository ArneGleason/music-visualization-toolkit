"""Unpaid timing mockup: garden departure, temporary Mars globe, orbital cues."""
import json,sys,subprocess,copy
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
(OUT/'frames').mkdir(exist_ok=True)
def smooth(t):
    t=np.clip(t,0,1);return t*t*(3-2*t)
y,x=np.mgrid[:720,:1280].astype(np.float32)
garden=cv2.resize(cv2.imread(str(ROOT/'codex/out/forest_walk_track_b.jpg')),(1280,853))[66:786].astype(np.float32)/255
texture=cv2.imread(str(ROOT/'codex/out/signal_crossing_space_a.jpg'))[320:1015,1060:1536].astype(np.float32)/255
rng=np.random.default_rng(274)
stars=np.zeros((720,1280,3),np.float32)+np.array([.020,.015,.012],np.float32)
for px,py,v in zip(rng.integers(0,1280,400),rng.integers(0,720,400),rng.uniform(.12,.65,400)):
    cv2.circle(stars,(int(px),int(py)),1,(float(v),float(v*.95),float(v*.85)),-1,cv2.LINE_AA)
for i,sf in enumerate(range(2122,2199)):
    flight=smooth((sf-2128)/21)
    radius=np.exp(np.log(1600)*(1-flight)+np.log(210)*flight)
    nx=(x-640)/radius;ny=(y-324)/radius
    rr=nx*nx+ny*ny;nz=np.sqrt(np.maximum(0,1-rr))
    longitude=np.arctan2(nx,np.maximum(nz,.001))
    latitude=np.arcsin(np.clip(ny,-1,1))
    u=((longitude/np.pi+.5)*475).astype(np.float32)
    v=((latitude/np.pi+.5)*694).astype(np.float32)
    surface=cv2.remap(texture,u,v,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    shade=.22+.78*np.clip(-.40*nx-.28*ny+.82*nz,0,1)
    mask=np.clip((1-np.sqrt(rr))*radius,0,1)
    planet=surface*shade[:,:,None]
    rim=np.exp(-((np.sqrt(rr)-1)*radius/5)**2)*.25
    pic=stars*(1-mask[:,:,None])+planet*mask[:,:,None]+rim[:,:,None]*np.array([.62,.38,.16])
    # Soft-edged optical bridge, deliberately a timing stand-in, not solved geography.
    scale=np.exp(-3.7*smooth((sf-2126)/17))
    matrix=np.array([[scale,0,640*(1-scale)],[0,scale,324*(1-scale)]],np.float32)
    ground=cv2.warpAffine(garden,matrix,(1280,720))
    soft=np.exp(-(((x-640)/(880*scale))**6+((y-324)/(610*scale))**6))
    mix=1-smooth((sf-2131)/11)
    if sf<=2126: soft=np.ones_like(x)
    alpha=soft*mix
    pic=pic*(1-alpha[:,:,None])+ground*alpha[:,:,None]
    haze=np.exp(-((sf-2136)/3.0)**2)*.13
    pic+=haze*np.exp(-(((x-640)/420)**2+((y-324)/260)**2))[:,:,None]*np.array([.65,.85,.9])
    glow=np.zeros_like(pic)
    for entry,color,tilt in [(2149,(.25,.70,1.),-.25),(2157,(1.,.85,.30),.35)]:
        amount=smooth((sf-entry)/6)*(1-smooth((sf-2173)/22))
        if amount<=0: continue
        theta=np.linspace(0,2*np.pi,500)
        a=(sf-entry)*.14
        ox=300*np.cos(theta);oy=98*np.sin(theta)
        px=640+ox*np.cos(tilt)-oy*np.sin(tilt)
        py=324+ox*np.sin(tilt)+oy*np.cos(tilt)
        strength=(.25+.75*np.exp(-np.mod(a-theta,2*np.pi)/1.7))*amount
        # Back half correctly hidden by the globe; front half crosses it.
        for j in range(len(theta)-1):
            if np.sin(theta[j])<0 and (px[j]-640)**2+(py[j]-324)**2<radius**2: continue
            c=tuple(float(q*strength[j]) for q in color)
            cv2.line(glow,(int(px[j]),int(py[j])),(int(px[j+1]),int(py[j+1])),c,2,cv2.LINE_AA)
    pic+=glow+cv2.GaussianBlur(glow,(0,0),5)*1.1+cv2.GaussianBlur(glow,(0,0),15)*.6
    cv2.imwrite(str(OUT/'frames'/f'{i:04d}.png'),np.clip(pic*255,0,255).astype(np.uint8))
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)
run(['ffmpeg','-v','error','-y','-framerate','24','-i',OUT/'frames/%04d.png','-frames:v','77','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'clean.mp4'])
edl=json.loads((ROOT/'out/next_exchange_timing_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/next_exchange_timing_v1/overlay_cues.json').read_text())
shot=copy.deepcopy(edl['shots'][-1]);shot.update(id='world_pullback_timing_test',setup='world_pullback_test',start_sec=2122/24,end_sec=2199/24,dur_sec=77/24,frames=77,lyric='I see the world plus more. More is probably nothing.',description='Temporary procedural globe and existing garden still. Timing mockup only.',prompt='',clip={'file':'out/world_pullback_test_v1/clean.mp4','in_sec':0,'speed':1})
edl['shots'].append(shot);cues['shots'].append({'id':shot['id'],'setup':shot['setup'],'section':shot['section'],'start':2122,'end':2199,'lyric':shot['lyric']})
edl['duration_sec']=cues['duration_sec']=2199/24;cues['frames']=2199
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2122','--end','2198','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start={2122/24}:end={2199/24},asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','77','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'recipe.json').write_text(json.dumps({'status':'timing_mockup_owner_review_pending','song_frames':[2122,2199],'frames':77,'world_on':2141,'orbit_entries':[2149,2157],'settle_phrase_on':2165,'sources':['codex/out/forest_walk_track_b.jpg','codex/out/signal_crossing_space_a.jpg'],'limitations':'Temporary textured sphere and soft optical image join, not continuous generated camera geography. Garden still is a framing stand-in. No paid generation. Prior shots in snapshot are not all approved; no production merge.','mastering':False},indent=2))
print('Pullback test ready:77frames.')
