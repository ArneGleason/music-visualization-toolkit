"""Approximate room-depth projector and equipment-lamp response, additive FX."""
from pathlib import Path
import json, sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
OLD=ROOT/'out/outro_B1_afterglow_v1'
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
cfg=json.loads((OLD/'settings.json').read_text())
cfg['room_projection']='v3: strong rotating violet/teal projection on approximate curved-wall and raised-bed depth; right equipment lamps respond independently'
(OUT/'settings.json').write_text(json.dumps(cfg,indent=2))
(OUT/'room').mkdir(exist_ok=True)
y,x=np.mgrid[:720,:1280].astype(np.float32)
def smooth(a,b,t):
    u=np.clip((t-a)/(b-a),0,1);return u*u*(3-2*u)
window=1-smooth(.95,1.12,((x-650)/540)**2+((y-190)/245)**2)
person=1-smooth(.78,1.04,((x-650)/255)**4+((y-425)/385)**4)
mask=cv2.GaussianBlur((1-window)*(1-person),(0,0),5)
# Pinhole rays intersect an approximate curved shell; foreground bed is nearer.
# This is a 2.5D lighting proxy, not recovered camera/scene geometry.
bed=smooth(410,490,y)*(1-smooth(1060,1170,x))*smooth(70,160,x)
wall_depth=3.4-1.6*np.clip(abs((x-640)/640),0,1)**1.7
bed_depth=np.clip(2.7-(y-440)*.0045,1.25,2.7)
depth=wall_depth*(1-bed)+bed_depth*bed
X=(x-640)/780*depth; Y=(360-y)/780*depth
# Central projector is forward of back wall and above the seated subject.
Z=depth-.4; Y=Y-.65
az=np.arctan2(X,Z); el=np.arctan2(Y,np.sqrt(X*X+Z*Z))
fixtures=[(1231,164,9),(1224,276,8),(1251,285,7),(1267,305,8),
          (1197,415,9),(1213,438,9),(1252,453,10),(1236,494,10),
          (1163,503,9),(1182,510,8),(1203,525,7)]
for i in range(cfg['frames']):
    t=i/24; v=cfg['records'][i]['voice_envelope']
    pic=cv2.imread(str(OLD/'optical'/f'{i:03}.png')).astype(np.float32)/255
    # Turning gobo texture sampled in projector angular coordinates.
    u=az*5.5-t*.95; w=el*7
    field=np.sin(u*2+1.1*np.sin(w*1.6+t*.23))+.65*np.cos(w*2.2-u*.65)
    violet=cv2.GaussianBlur(np.exp(-((field-.50)/.34)**2),(0,0),5)
    teal=cv2.GaussianBlur(np.exp(-((field+.72)/.38)**2),(0,0),6)
    reflect=np.clip(np.mean(pic,axis=2)*1.9,.20,.85)
    strength=(2.5+.65*v)*mask*reflect
    light=(violet[:,:,None]*[.65,.16,.50]+teal[:,:,None]*[.45,.62,.10])*strength[:,:,None]
    # Warm lamp cores and spill only at existing right-hand practical lights.
    for j,(cx,cy,r) in enumerate(fixtures):
        d2=(x-cx)**2+(y-cy)**2
        pulse=(.5+.5*np.sin(t*(2.1+j*.17)+j*2.4))**5
        level=.10+.8*pulse+.85*v*(.5+.5*np.sin(j*1.7+t*2))
        core=np.exp(-d2/(r*r*.75))
        halo=np.exp(-d2/(r*r*12))
        lit=np.clip((pic[:,:,2]-.10)*3,0,1)
        light+=(core*lit+halo*.13)[:,:,None]*np.array([.13,.52,1.0])*level
    delta=(1-pic)*(1-np.exp(-light))
    cv2.imwrite(str(OUT/'room'/f'{i:03}.png'),np.clip(delta*255,0,255).astype(np.uint8))
    if i in (67,77,96):
        oldlight=cv2.imread(str(OLD/'lights'/f'{i:03}.png')).astype(np.float32)/255
        cv2.imwrite(str(OUT/f'check{i}.jpg'),(np.clip(pic+oldlight+delta,0,1)*255).astype(np.uint8))
print('Depth-shaped rotating projection and practical lights ready',flush=True)
