from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913/motion-graphics/SCENE11-SMOKE-003')
im=Image.new('RGB',(1280,210))
for i,f in enumerate([20,32,41,50]):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/24),'-i',str(r/'smoke-b-turbulence-v001.mp4'),'-frames:v','1','-vf','scale=320:180','-f','image2pipe','-vcodec','png','-']);im.paste(Image.open(io.BytesIO(b)),(i*320,0));ImageDraw.Draw(im).text((i*320,185),str(f+3724),fill='white')
im.save(r/'review.jpg')
