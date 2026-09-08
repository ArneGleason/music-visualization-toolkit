"""Soft room-projected liquid-light patterns, separate from approved artifact FX."""
from pathlib import Path
import json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
OLD=ROOT/'out/outro_B1_afterglow_v1'
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
cfg=json.loads((OLD/'settings.json').read_text());cfg['room_projection']='Soft violet/teal oil-lamp caustics on interior surfaces; no face/window overlay'
(OUT/'settings.json').write_text(json.dumps(cfg,indent=2))
(OUT/'room').mkdir(exist_ok=True)
y,x=np.mgrid[:720,:1280].astype(np.float32)
def smooth(a,b,t):
    u=np.clip((t-a)/(b-a),0,1);return u*u*(3-2*u)
# Soft approximate receiver surfaces, not a new 3D room solve.
left=np.exp(-((x-165)/205)**4-((y-450)/260)**4)
right=np.exp(-((x-1120)/185)**4-((y-420)/270)**4)
pillows=np.exp(-((y-540)/100)**4)*(np.exp(-((x-280)/190)**4)+np.exp(-((x-1030)/150)**4))
window=1-smooth(.95,1.12,((x-650)/540)**2+((y-190)/245)**2)
person=1-smooth(.78,1.04,((x-650)/255)**4+((y-425)/385)**4)
mask=np.clip(left+right+pillows,0,1)*(1-window)*(1-person)
mask=cv2.GaussianBlur(mask,(0,0),7)
for i in range(cfg['frames']):
    t=i/24;v=cfg['records'][i]['voice_envelope']
    pic=cv2.imread(str(OLD/'optical'/f'{i:03}.png')).astype(np.float32)/255
    # Broad interlocking liquid-light contours drift slowly, not rainbow cycling.
    a=np.sin(x*.018+np.sin(y*.017+t*.57)*1.8-t*.72)
    b=np.cos(y*.022+np.sin(x*.012-t*.48)*1.65+t*.41)
    c=np.sin((x+y)*.013+t*.53)
    field=a+b*.8+c*.45
    violet=np.exp(-((field-.65)/.32)**2)
    teal=np.exp(-((field+.8)/.38)**2)
    violet=cv2.GaussianBlur(violet,(0,0),8)
    teal=cv2.GaussianBlur(teal,(0,0),10)
    # Light responds to surface reflectance, leaving black recesses dark.
    reflect=np.clip(np.mean(pic,axis=2)*2.0,.12,.85)
    strength=(.60+.16*v)*mask*reflect
    light=(violet[:,:,None]*np.array([.36,.10,.25])+teal[:,:,None]*np.array([.20,.30,.06]))*strength[:,:,None]
    delta=(1-pic)*(1-np.exp(-light))
    cv2.imwrite(str(OUT/'room'/f'{i:03}.png'),np.clip(delta*255,0,255).astype(np.uint8))
    if i==77:
        oldlight=cv2.imread(str(OLD/'lights'/f'{i:03}.png')).astype(np.float32)/255
        comp=np.clip(pic+oldlight+delta,0,1)
        cv2.imwrite(str(OUT/'check77.jpg'),(comp*255).astype(np.uint8))
print('Soft projector layer ready',flush=True)
