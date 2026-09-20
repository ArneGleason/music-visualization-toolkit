from pathlib import Path
import subprocess
o=Path(__file__).resolve().parent;r=o.parents[1]
subprocess.run(['ffmpeg','-y','-v','error','-i',str(r/'motion-graphics/COUNTDOWN-EDIT-001/flight-timed-v001.mp4'),'-framerate','24','-i',str(o/'overlay/snow-%04d.png'),'-filter_complex','[1:v]gblur=sigma=9[cloud];[0:v][cloud]overlay=0:0:shortest=1','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',str(o/'flight-snow-v001.mp4')],check=True)
