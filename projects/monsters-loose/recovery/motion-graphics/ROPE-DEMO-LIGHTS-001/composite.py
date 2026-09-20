import subprocess
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent.parent
subprocess.run(['ffmpeg','-v','error','-y','-i',str(r/'video-tests/KLING-ROPE-DEMO-001/KLING-ROPE-DEMO-001-01.mp4'),'-framerate','24','-i',str(o/'overlay/lights-%04d.png'),'-filter_complex','[0:v][1:v]overlay=0:0:format=auto','-an','-frames:v','97','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(o/'Rope-demo-lights-v001.mp4')],check=True)
