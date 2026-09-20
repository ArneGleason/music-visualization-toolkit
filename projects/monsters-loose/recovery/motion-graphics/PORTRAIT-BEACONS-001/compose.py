from pathlib import Path
import subprocess
r=Path(__file__).resolve().parents[2];o=Path(__file__).resolve().parent
for name in ['insectarium','exobiology']:
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(r/f'motion-graphics/CREATURE-PORTRAITS-001/{name}-push-v001.mp4'),'-framerate','24','-i',str(o/name/'overlay/lights-%04d.png'),'-filter_complex','[0:v][1:v]overlay=0:0:format=auto:shortest=1[v]','-map','[v]','-an','-frames:v','26','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(o/name/(name+'-beacon-v001.mp4'))],check=True)
