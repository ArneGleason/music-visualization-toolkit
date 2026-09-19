import subprocess
from pathlib import Path
o=Path(__file__).resolve().parent
subprocess.run(['ffmpeg','-y','-v','error','-i',str(o.parent/'HARPER-SIGN-SPLICE-001/Harper-sign-composite-v001.mp4'),'-framerate','24','-i',str(o/'frames/bubble-%04d.png'),'-filter_complex','[0:v][1:v]overlay=0:0:shortest=1[v]','-map','[v]','-map','0:a','-c:v','libx264','-crf','17','-preset','fast','-c:a','copy','-movflags','+faststart',str(o/'Harper-speech-v001.mp4')],check=True)
