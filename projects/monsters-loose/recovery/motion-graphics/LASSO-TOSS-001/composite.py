import subprocess
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent.parent
source=r/'video-tests/KLING-LASSO-TOSS-001/KLING-LASSO-TOSS-001-01.mp4'
clean=r/'assets/SCN-006-lasso-underhand-plate-v002.png'
# Repaired cage region only; preserve generated performance and all other pixels.
alpha="255*min(1,min(min(X/18,(W-1-X)/18),min(Y/18,(H-1-Y)/18)))"
filters=f"[1:v]scale=1916:1080,crop=270:330:1580:30,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='{alpha}'[patch];[0:v][patch]overlay=1580:30:format=auto[clean];[clean][2:v]overlay=0:0:format=auto[out]"
subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-loop','1','-i',str(clean),'-framerate','24','-i',str(o/'overlay/rope-%04d.png'),'-filter_complex',filters,'-map','[out]','-an','-frames:v','97','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(o/'Lasso-toss-v001.mp4')],check=True)
