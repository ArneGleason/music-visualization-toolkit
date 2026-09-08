"""Fictional biological-to-celestial phosphor correspondence, exact A1 clock."""
from pathlib import Path
import json, math, subprocess, sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
LAYER=OUT/'layers'; LAYER.mkdir(exist_ok=True)
source=Path(json.loads((ROOT/'out/outro_A1_kling_v1/codex_verification.json').read_text())['conformed']['file'])
cap=cv2.VideoCapture(str(source)); frames=[]
while True:
    ok,f=cap.read()
    if not ok: break
    frames.append(f)
cap.release()
N=len(frames); assert N==191
S=720
# Four points describe glass, not the outer brass bezel. Mask rounds inward.
quad=np.float32([[1064,308],[1278,363],[1250,582],[1049,512]])
square=np.float32([[0,0],[S-1,0],[S-1,S-1],[0,S-1]])
H=cv2.getPerspectiveTransform(square,quad)
inv=cv2.getPerspectiveTransform(quad,square)
glass=cv2.warpPerspective(frames[0].astype(np.float32),inv,(S,S))
y,x=np.mgrid[:S,:S]; nx=(x-S/2)/(S/2); ny=(y-S/2)/(S/2)
edge=(np.abs(nx)**5+np.abs(ny)**5)**.2
mask=np.clip((.965-edge)/.035,0,1).astype(np.float32)
mask=mask*mask*(3-2*mask)
alpha=cv2.warpPerspective(mask,H,(1280,720))
pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'out/outro_A1_kling_v1/guide.wav'),'-ac','1','-ar','24000','-f','f32le','-'])
audio=np.frombuffer(pcm,dtype='<f4')
rms=np.array([np.sqrt(np.mean(audio[i*1000:(i+1)*1000]**2)) for i in range(N)])
rms=np.convolve(rms,[.18,.64,.18],mode='same'); rms=np.clip(rms/(np.percentile(rms,92)+1e-8),0,1)
rng=np.random.default_rng(711)
grain=rng.normal(0,1.1,(S,S,1)).astype(np.float32)
amber=np.array([62,171,255],np.float32); cyan=np.array([243,225,92],np.float32)
star_xy=np.array([[-.56,-.42],[-.12,-.63],[.34,-.45],[.59,-.05],[.27,.24],[.43,.55],[-.11,.65],[-.50,.39],[-.28,.02]],np.float32)
star_xy=star_xy*S*.44+S*.5
edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,1),(8,4)]
def smooth(a,b,t):
    u=np.clip((t-a)/(b-a),0,1); return u*u*(3-2*u)
def curve(im,pts,color,width=2):
    cv2.polylines(im,[np.round(pts).astype(np.int32)],False,tuple(float(v) for v in color),width,cv2.LINE_AA)
trail=np.zeros((S,S,3),np.float32)
tiles=[]
for f in range(N):
    t=f/24; v=rms[f]
    # Reveal after the screen's existing response. Coherence grows through low light.
    resolve=smooth(2.25,6.1,t)
    power=.65+.38*v
    im=np.zeros_like(trail)
    theta=np.linspace(0,math.tau,241)
    # Peripheral celestial coordinate rings, quiet and sparse, not a dashboard.
    for rad in [.34,.70]:
        pts=np.c_[S/2+S*.44*rad*np.cos(theta),S/2+S*.44*rad*np.sin(theta)]
        curve(im,pts,cyan*(.10+.08*resolve),1)
    for a in np.arange(0,math.tau,math.tau/24):
        pts=np.array([[.78*np.cos(a),.78*np.sin(a)],[.83*np.cos(a),.83*np.sin(a)]])*S*.44+S/2
        curve(im,pts,amber*.25,2)
    # Amber sample helix continuously rearranges into the SAME cyan map nodes.
    u=np.linspace(0,1,181)
    yy=S*(.20+.60*u)
    helix=[]
    for sign in [-1,1]:
        xx=S*(.5+sign*(.19+.018*v)*np.sin(u*math.tau*1.65+t*.5))
        xx+=S*.006*np.sin(u*math.tau*13+t*4)*(1+v)
        pts=np.c_[xx,yy]; helix.append(pts)
        curve(im,pts,amber*(1-.70*resolve)*power,3)
    for u0 in np.linspace(.08,.92,11):
        j=int(u0*180)
        curve(im,np.array([helix[0][j],helix[1][j]]),amber*(.5-.3*resolve)*power,2)
    for k,target in enumerate(star_xy):
        j=int((k+1)/10*180); initial=helix[k%2][j]
        p=(1-resolve)*initial+resolve*target
        col=(1-resolve)*amber+resolve*cyan
        scan=.78+.22*np.exp(-(((k/9-t*.22)%1)/.24))
        cv2.circle(im,tuple(p.astype(int)),int(3+2*v),tuple(float(c*power*scan) for c in col),-1,cv2.LINE_AA)
        if resolve>.3:
            radius=int(7+5*(1-v))
            cv2.circle(im,tuple(p.astype(int)),radius,tuple(float(c*.3*resolve) for c in amber),1,cv2.LINE_AA)
    for k,(a,b) in enumerate(edges):
        reveal=smooth(2.5+k*.18,3.4+k*.18,t)
        if reveal>0:
            pts=np.array([star_xy[a],star_xy[a]+(star_xy[b]-star_xy[a])*reveal])
            curve(im,pts,cyan*resolve*(.48+.30*v),2)
    # Scanning amber spiral remains faintly visible behind the resolved map.
    q=np.linspace(0,math.tau*2.2,240)
    r=np.linspace(.018,.27,len(q))*S
    spiral=np.c_[S/2+r*np.cos(q+t*.19),S/2+r*np.sin(q+t*.19)]
    curve(im,spiral,amber*(.14+.22*resolve)*power,2)
    trail=trail*.78+im*.48
    trace=im*.70+trail*.68
    bloom=cv2.GaussianBlur(trace,(0,0),6)*.75+cv2.GaussianBlur(trace,(0,0),18)*.30
    # Retain subdued glass texture; local noise and scan rows belong to the CRT only.
    raster=(.96+.04*np.sin(y*math.pi*.5))[:,:,None]
    screen=glass*.62+((trace+bloom)*raster)+grain
    response=math.exp(-.5*((t-2.2)/.24)**2)
    current=cv2.warpPerspective(frames[f].astype(np.float32),inv,(S,S))
    screen+=np.maximum(current-glass,0)*.24*response
    screen=np.clip(screen,0,255).astype(np.uint8)
    projected=cv2.warpPerspective(screen,H,(1280,720))
    rgba=np.dstack([projected,(alpha*255).astype(np.uint8)])
    cv2.imwrite(str(LAYER/f'{f:03}.png'),rgba)
    if f in [12,53,110,155]:
        comp=frames[f]*(1-alpha[:,:,None])+projected*alpha[:,:,None]
        cv2.imwrite(str(OUT/f'check_{f:03}.jpg'),comp.astype(np.uint8))
        tiles.append(cv2.resize(comp[290:605,1030:1280].astype(np.uint8),(300,378)))
cv2.imwrite(str(OUT/'screen_detail.jpg'),np.hstack(tiles))
(OUT/'settings.json').write_text(json.dumps({'source':str(source),'source_origin_song_frame':4165,'frames':N,'fps':24,'quad':quad.tolist(),'projection':'Fixed planar screen on locked-camera plate, rounded inset mask; not motion-tracked','driver':'aligned lead vocal RMS, soft saturation, 3-frame smoothing','concept':'FICTIONAL sample-helix nodes resolving into a celestial constellation, not measured scientific data','layer':'straight-alpha screen replacement; original face/room untouched','resolve_source_seconds':[2.25,6.1]},indent=2))
print('Screen layers and QA images ready',flush=True)
