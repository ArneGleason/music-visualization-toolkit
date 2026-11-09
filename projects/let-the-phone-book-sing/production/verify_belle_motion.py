"""Check rendered frames against independent source-frame mappings, including dissolves."""
import json,math,subprocess
from pathlib import Path
import numpy as np

BASE=Path(__file__).resolve().parents[1]

def decode(path, selection=None):
    filters=[]
    if selection:filters.append(selection)
    filters+=['scale=1920:1080:force_original_aspect_ratio=decrease','pad=1920:1080:(ow-iw)/2:(oh-ih)/2','scale=480:270']
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',','.join(filters),'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','rgb24','-'])
    return np.frombuffer(raw,np.uint8).reshape(-1,270,480,3)

def at(frames,pos):
    return frames[math.floor(pos)].astype(float)*(1-pos%1)+frames[math.ceil(pos)].astype(float)*(pos%1)

if __name__=='__main__':
    out=BASE/'generated/visual-animatic-v012'
    belle=decode(BASE/'generated/kling-tests/belle-bell-v001/belle-original-1080p.mp4')
    liberty=decode(BASE/'generated/kling-tests/liberty-bell-v003/liberty-original-1080p.mp4')
    baked=decode(BASE/'generated/motion-graphics/belle-echo-v006/belle-word-art-silent.mp4')
    assert len(baked)==141
    roi=(slice(0,260),slice(70,250),slice(None))
    opening_errors=[float(abs(baked[n][roi].astype(float)-at(belle,42+n*124/140)[roi]).mean()) for n in range(30)]
    assert max(opening_errors)<3.5, opening_errors
    actual=decode(out/'Let-the-Phone-Book-Sing-fullframe-clean-v012.mp4',"select='between(n,430,440)'")
    assert len(actual)==11
    errors=[]
    for f in range(430,441):
        if f<435:expected=at(belle,42+(f-296)*124/140)
        elif f<439:
            alpha=(f-434)/5
            expected=at(belle,42+(f-296)*124/140)*(1-alpha)+at(liberty,32+f-437)*alpha
        else:expected=at(liberty,32+f-437)
        error=float(abs(actual[f-430].astype(float)-expected).mean())
        errors.append(dict(masterFrame=f,meanPixelError=error))
    assert max(x['meanPixelError'] for x in errors)<3.5,errors
    report=dict(firstThirtyFramesMaxSourceMappingError=max(opening_errors),dissolveFrameChecks=errors,blendFrames=[435,436,437,438],result='pass: no leading freeze or source-time jump into dissolve')
    (out/'belle-motion-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
