from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');o=r/'motion-graphics/SCENE12-EXCHANGE-001'
for name in ['yes','no']:
 p=r/f'video-tests/KLING-SCENE12-{name.upper()}-001/KLING-SCENE12-{name.upper()}-001-01.mp4'
 if not p.exists():continue
 im=Image.new('RGB',(1280,440))
 for i,f in enumerate([0,12,24,36,48,60,84,108]):
  b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/24),'-i',str(p),'-frames:v','1','-vf','scale=320:180','-f','image2pipe','-vcodec','png','-']);x=i%4*320;y=i//4*220;im.paste(Image.open(io.BytesIO(b)),(x,y));ImageDraw.Draw(im).text((x,y+185),str(f),fill='white')
 im.save(o/f'{name}-review.jpg')
