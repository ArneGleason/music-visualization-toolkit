import subprocess,io
from pathlib import Path
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parent.parent;o=r/'motion-graphics/OUTRO-LIGHTS-001'
src=r/'motion-graphics/OUTRO-003/FINALE-timed-v003.mp4'
for f in [0,85,170,255,339]:
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/24),'-i',str(src),'-frames:v','1','-vf','scale=960:540','-f','image2pipe','-vcodec','png','-threads','1','-'])
 im=Image.open(io.BytesIO(raw));im.save(o/('finale-plain-'+str(f)+'.png'))
 d=ImageDraw.Draw(im)
 for x in range(0,960,50):d.line((x,0,x,300),fill=(40,60,70));d.text((x+2,5),str(x),fill='cyan')
 for y in range(50,300,50):d.line((0,y,960,y),fill=(40,60,70));d.text((2,y+2),str(y),fill='cyan')
 im.save(o/('finale-grid-'+str(f)+'.jpg'))
