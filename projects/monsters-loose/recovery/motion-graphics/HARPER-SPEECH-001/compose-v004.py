from pathlib import Path
from PIL import Image
import subprocess
o=Path(__file__).resolve().parent;out=o/'frames-v004-fade';out.mkdir(exist_ok=True)
for f in range(1,145):
 opacity=0
 for a,b in [(13,60),(61,92),(93,140)]:
  if a<=f<=b:
   u=min(1,(f-a+1)/5,(b-f+1)/4);opacity=u*u*(3-2*u)
 im=Image.open(o/'frames-v004'/f'bubble-{f:04}.png').convert('RGBA');im.putalpha(im.getchannel('A').point(lambda v:round(v*opacity)));im.save(out/f'bubble-{f:04}.png')
subprocess.run(['ffmpeg','-y','-v','error','-i',str(o.parent/'HARPER-SIGN-SPLICE-001/Harper-sign-composite-v001.mp4'),'-framerate','24','-i',str(out/'bubble-%04d.png'),'-filter_complex','[0:v][1:v]overlay=0:0:shortest=1[v]','-map','[v]','-map','0:a','-c:v','libx264','-crf','17','-preset','fast','-c:a','copy','-movflags','+faststart',str(o/'Harper-speech-v004.mp4')],check=True)
