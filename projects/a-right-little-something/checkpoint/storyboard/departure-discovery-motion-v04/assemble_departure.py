"""Use Blender for the first 59 frames, preserving the remaining source frames."""
import json
from pathlib import Path
import shutil
import subprocess
from PIL import Image, ImageChops, ImageStat

OUT=Path(__file__).resolve().parent
for i in range(1,60):
    assert (OUT/'departure-frames'/f'frame_{i:04d}.png').exists()
for i in range(60,141):
    shutil.copy2(OUT/'departure-source'/f'{i:03d}.png', OUT/'departure-frames'/f'frame_{i:04d}.png')
source=Image.open(OUT/'departure-source/059.png').convert('RGB')
render=Image.open(OUT/'departure-frames/frame_0059.png').convert('RGB')
mean=ImageStat.Stat(ImageChops.difference(source,render)).mean
assert max(mean)<1,mean
subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(OUT/'departure-frames/frame_%04d.png'),
    '-frames:v','140','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
    str(OUT/'departure-pullout-twinkle.mp4')],check=True)
manifest=dict(kind='Blender compositor pullout and cyan station twinkle',frames=140,
    startFrame=2665,pulloutEndFrameInclusive=2723,renderedFrames=59,sourceSpeed='Unchanged V56 reversed video',
    startScale=1.18,endScale=1.0,scaleCurve='1+0.18*(1-(localFrame-1)/58)^1.6',
    twinkle=dict(sourceAnchorPixels=[960,514],localStartFrame=1,peakFrame=6,localEndFrame=17,color='cyan'),
    fullFrameReturnMeanAbsoluteErrorRGB=mean,
    tail='Frames 60–140 copied pixel-for-pixel from source PNGs before encoding',
    blend='departure-pullout-twinkle.blend',newCredits=0)
(OUT/'departure-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('140-frame departure assembled; full-frame return mean pixel error:',mean)
