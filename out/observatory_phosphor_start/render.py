"""Reverse CRT-collapse opening, picture-only transition on existing review."""
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
W,H=1280,720
FPS=24
def ease(a,b,t):
    x=np.clip((t-a)/(b-a),0,1)
    return x*x*(3-2*x)
yy,xx=np.mgrid[:H,:W].astype(np.float32)
def effect(frame,t):
    if t>=1.20:return frame.astype(np.float32)
    # Width opens before height, like an unstable raster acquiring deflection.
    wx=5+(W*1.025-5)*ease(.14,.53,t)
    hy=3+(H*1.018-3)*ease(.42,1.03,t)
    settle=ease(1.03,1.20,t)
    wx=wx*(1-settle)+W*settle;hy=hy*(1-settle)+H*settle
    cx=W/2+(1-ease(.25,.95,t))*1.5*np.sin(t*97)
    cy=H/2+(1-ease(.3,.95,t))*1.1*np.sin(t*83)
    mapx=(xx-cx)*W/wx+W/2
    mapy=(yy-cy)*H/hy+H/2
    picture=cv2.remap(frame.astype(np.float32),mapx.astype(np.float32),mapy.astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
    # Feather just the image boundary, not the whole established shot.
    edge=np.clip((wx/2-np.abs(xx-cx))/2,0,1)*np.clip((hy/2-np.abs(yy-cy))/2,0,1)
    picture*=edge[:,:,None]*ease(.26,.66,t)
    flicker=.73+.19*np.sin(t*91)+.08*np.sin(t*213+.4)
    dot=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*2.2**2))
    dotbloom=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*15**2))*.15
    dotlevel=(1-ease(.25,.55,t))*flicker
    bar=np.exp(-((yy-cy)/1.8)**2)*np.exp(-((xx-cx)/max(4,wx*.38))**8)
    bloom=np.exp(-((yy-cy)/11)**2)*np.exp(-((xx-cx)/max(10,wx*.39))**8)*.19
    linelevel=ease(.13,.28,t)*(1-ease(.48,.88,t))
    # BGR phosphor: warm white/amber, no full-screen white flash or added sound.
    light=((dot+dotbloom)*dotlevel+(bar+bloom)*linelevel)[:,:,None]*np.array([155.,222.,255.])*1.6
    return np.clip(picture+light,0,255)
source=ROOT/'out/opening_through_scope/preview.mp4'
cap=cv2.VideoCapture(str(source));assert cap.get(cv2.CAP_PROP_FPS)==24
(OUT/'frames').mkdir(exist_ok=True)
for f in range(155):
    ok,frame=cap.read();assert ok
    if f<29:
        result=sum(effect(frame,(f+(i+.5)/4)/FPS) for i in range(4))/4
        result=np.rint(result).astype(np.uint8)
    else:result=frame
    cv2.imwrite(str(OUT/'frames'/f'{f:04d}.png'),result)
cap.release()
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(OUT/'frames/%04d.png'),
 '-i',str(ROOT/'audio/song.wav'),'-map','0:v:0','-map','1:a:0','-t',str(155/24),
 '-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',str(OUT/'preview.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview.mp4'),'-f','null','-'],check=True)
(OUT/'recipe.json').write_text(json.dumps({'input':str(source),'song_frames':[0,155],
 'effect_seconds':[0,1.2],'width_open':[.14,.53],'height_open':[.42,1.03],
 'settle_end':1.2,'temporal_samples_transition':4,'scope_cut_frame':86,
 'audio':'Unchanged song time zero, no additional sound','status':'owner_review_pending',
 'note':'Preview-stage transition, not a global grade or clean per-shot delivery. Do not add twice in final assembly.'},indent=2))
print('155-frame opening preview, transition settles by1.2s; approved scope unchanged.')
