from pathlib import Path
import subprocess
o=Path(__file__).resolve().parent;r=o.parents[1]
subprocess.run(['ffmpeg','-y','-v','error','-i',str(r/'video-tests/KLING-HABITATS-001/KLING-HABITATS-001-01.mp4'),'-framerate','24','-i',str(o/'overlay/lights-%04d.png'),'-filter_complex','[0:v][1:v]overlay=0:0:format=auto:shortest=1[v]','-map','[v]','-an','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(o/'Habitat-lights-v001.mp4')],check=True)
