"""Local compositing diagnostics; never overwrites source avatar videos."""
import json
import subprocess
from pathlib import Path
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'generated/avatar-tests/hedra-v001'
W,H=1280,720
FONT=ImageFont.truetype(str(BASE/'generated/animatic/assets/BarlowSemiCondensed-SemiBold.ttf'),27)

def frames(path):
    proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-vf',f'scale={W}:{H},fps=24','-t','5.625','-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
    try:
        while True:
            raw=proc.stdout.read(W*H*3)
            if len(raw)!=W*H*3:break
            yield np.frombuffer(raw,np.uint8).reshape(H,W,3).copy()
    finally:
        proc.stdout.close();proc.wait()

def matte(rgb,mode):
    a=rgb.astype(np.float32);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    if mode=='green':
        # Differential chroma matte protects neutral black ink and skin.
        excess=g-np.maximum(r,b)
        alpha=1-np.clip((excess-12)/55,0,1)
        a[:,:,1]=np.minimum(g,np.maximum(r,b)+8+20*alpha)
    else:
        # Compare global dark key with border-connected removal. Neither is AI matting.
        brightness=np.max(a,axis=2)
        neutral=np.max(a,axis=2)-np.min(a,axis=2)
        key=(brightness<55)&(neutral<20)
        if mode=='dark-connected':
            seed=np.zeros((H,W),bool);seed[0,:]=key[0,:];seed[-1,:]=key[-1,:];seed[:,0]=key[:,0];seed[:,-1]=key[:,-1]
            key=ndimage.binary_propagation(seed,mask=key)
        alpha=1-ndimage.gaussian_filter(key.astype(np.float32),.55)
    return a,alpha

def render(name,mode):
    source=OUT/f'{name}-original.mp4'
    bg=np.asarray(Image.open(BASE/'generated/environment-development/old-church-quarter-v006.png').convert('RGB').resize((W,H)),np.float32)
    target=OUT/f'{name}-{mode}-composite.mp4'
    enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','pipe:0','-i',str(source),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','5.625','-movflags','+faststart',str(target)],stdin=subprocess.PIPE)
    count=0
    for i,rgb in enumerate(frames(source)):
        fg,alpha=matte(rgb,mode)
        composite=np.uint8(np.clip(fg*alpha[:,:,None]+bg*(1-alpha[:,:,None]),0,255))
        picture=Image.fromarray(composite)
        d=ImageDraw.Draw(picture);label=f'{name} | {mode} removal';d.rectangle((0,0,FONT.getlength(label)+24,40),fill='#161920');d.text((12,4),label,font=FONT,fill='white')
        if i in [24,72,120]:
            picture.save(OUT/f'{name}-{mode}-{i}.png')
            Image.fromarray(np.uint8(alpha*255)).save(OUT/f'{name}-{mode}-matte-{i}.png')
        enc.stdin.write(picture.tobytes());count+=1
    enc.stdin.close();assert enc.wait()==0;assert count==135,count
    return target.name

if __name__=='__main__':
    outputs=[render('hedra-green','green'),render('hedra-dark','dark-global'),render('hedra-dark','dark-connected')]
    if (OUT/'kling-dark-original.mp4').exists():outputs.append(render('kling-dark','dark-connected'))
    (OUT/'compositing-methods.json').write_text(json.dumps({'outputs':outputs,'method':'Simple diagnostic keys; dark-connected removes only dark neutral pixels connected to frame borders. Not learned video matting.','limitations':['Watermarks retained','AI-generated dark source may differ slightly from green original, so not a pixel-identical background-only experiment','Independent stochastic performances; one sample each is not a model benchmark','No manual rotoscoping or temporal matte stabilization']},indent=2)+'\n')
    print(outputs)
