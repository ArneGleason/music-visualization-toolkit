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
mask=np.clip((.98-edge)/.19,0,1).astype(np.float32)
mask=mask*mask*(3-2*mask)
alpha=cv2.warpPerspective(mask*.82,H,(1280,720))
# Measure the actual returned TV illumination, not a guessed time or old base.
screen_luma=np.array([cv2.cvtColor(f[370:490,1095:1215],cv2.COLOR_BGR2GRAY).mean() for f in frames])
floor=float(np.median(screen_luma[:24]))
flash=np.clip((screen_luma-floor)/(np.max(screen_luma)-floor+1e-8),0,1)
flash=np.convolve(flash,[.15,.70,.15],mode='same')
peak=int(np.argmax(flash)); onset=int(np.flatnonzero(flash>.2)[0])
burst_time=peak/24
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
    response=float(flash[f])
    resolve=smooth(onset/24-.10,burst_time+.38,t)
    power=.60+.43*v+1.15*response
    # Moving sample and map remain one coherent structure; stronger travel during receipt.
    turn=.34*math.sin(t*1.7)+.26*t+1.2*smooth(onset/24-.10,burst_time+.55,t)
    scale=.86+.12*math.sin(t*2.4)+.13*v+.23*response
    rot=np.array([[math.cos(turn),-math.sin(turn)],[math.sin(turn),math.cos(turn)]])
    moving_stars=(star_xy-S/2)@rot.T*scale+S/2
    moving_stars[:,0]+=S*.035*math.sin(t*2.0)
    moving_stars[:,1]+=S*.025*math.cos(t*1.6)
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
        xx=S*(.5+sign*(.19+.045*v+.035*response)*np.sin(u*math.tau*1.65+t*2.0))
        xx+=S*.006*np.sin(u*math.tau*13+t*4)*(1+v)
        pts=(np.c_[xx,yy]-S/2)@rot.T*(.95+.07*v+.12*response)+S/2; helix.append(pts)
        curve(im,pts,amber*(1-.70*resolve)*power,3)
    for u0 in np.linspace(.08,.92,11):
        j=int(u0*180)
        curve(im,np.array([helix[0][j],helix[1][j]]),amber*(.5-.3*resolve)*power,2)
    for k,target in enumerate(moving_stars):
        j=int((k+1)/10*180); initial=helix[k%2][j]
        p=(1-resolve)*initial+resolve*target
        col=(1-resolve)*amber+resolve*cyan
        scan=.78+.22*np.exp(-(((k/9-t*.22)%1)/.24))
        cv2.circle(im,tuple(p.astype(int)),int(3+2*v),tuple(float(c*power*scan) for c in col),-1,cv2.LINE_AA)
        if resolve>.3:
            radius=int(7+5*(1-v))
            cv2.circle(im,tuple(p.astype(int)),radius,tuple(float(c*.3*resolve) for c in amber),1,cv2.LINE_AA)
    for k,(a,b) in enumerate(edges):
        reveal=smooth(onset/24-.1+k*.025,burst_time+.22+k*.025,t)
        if reveal>0:
            pts=np.array([moving_stars[a],moving_stars[a]+(moving_stars[b]-moving_stars[a])*reveal])
            curve(im,pts,cyan*resolve*(.48+.30*v),2)
            # Bright packets travel along connections instead of a static wire drawing.
            travel=(t*.8+k*.173)%1
            p=moving_stars[a]+(moving_stars[b]-moving_stars[a])*travel
            cv2.circle(im,tuple(p.astype(int)),4,tuple(float(c*power) for c in cyan),-1,cv2.LINE_AA)
    # A brief expanding scan and data spokes coincide with illumination on her face.
    if response>.015:
        ringrad=S*(.10+.34*smooth(onset/24,burst_time+.3,t))
        pts=np.c_[S/2+ringrad*np.cos(theta),S/2+ringrad*np.sin(theta)]
        curve(im,pts,(amber+cyan)*.7*response,5)
        for a in np.linspace(0,math.tau,18,endpoint=False):
            radii=np.array([.12,.25+.16*response])*S
            pts=np.c_[S/2+radii*np.cos(a+t),S/2+radii*np.sin(a+t)]
            curve(im,pts,cyan*.65*response,2)
    # Scanning amber spiral remains faintly visible behind the resolved map.
    q=np.linspace(0,math.tau*2.2,240)
    r=np.linspace(.018,.27,len(q))*S
    spiral=np.c_[S/2+r*np.cos(q+t*.85),S/2+r*np.sin(q+t*.85)]
    curve(im,spiral,amber*(.14+.22*resolve)*power,2)
    trail=trail*.68+im*.48
    trace=im*.70+trail*.68
    trace=cv2.GaussianBlur(trace,(0,0),1.35)
    bloom=cv2.GaussianBlur(trace,(0,0),7)*(.85+.55*response)+cv2.GaussianBlur(trace,(0,0),22)*(.38+.45*response)
    # Retain subdued glass texture; local noise and scan rows belong to the CRT only.
    raster=(.96+.04*np.sin(y*math.pi*.5))[:,:,None]
    current=cv2.warpPerspective(frames[f].astype(np.float32),inv,(S,S))
    # Mostly LIVE glass, including static, rather than a frozen dark replacement.
    backing=current*.72+glass*.15
    light=(trace+bloom)*raster+grain
    # Screen blend retains noisy glass structure instead of opaque pasted-on black.
    screen=255-(255-np.clip(backing,0,255))*np.exp(-np.maximum(light,0)/220)
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
(OUT/'burst_timing.json').write_text(json.dumps({'source_peak_frame':peak,'song_peak_frame':4165+peak,'source_onset_frame':onset,'source_peak_seconds':burst_time,'screen_luma':screen_luma.tolist(),'burst_envelope':flash.tolist(),'mask_feather_normalized':.19,'layer_opacity':.82,'live_glass_weight':.72,'notes':'Burst driven by measured luminance of returned Kling TV, so it shares the original face-light event. Rotating map, faster helix, travelling packets and expanding receipt scan. Manual fixed projection; mask softened, not a claim of tracking.'},indent=2))
