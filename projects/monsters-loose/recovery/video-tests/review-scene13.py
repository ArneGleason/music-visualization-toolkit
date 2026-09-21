from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');o=r/'motion-graphics/SCENE13-PROCESSION-001';o.mkdir(exist_ok=True)
p=r/'video-tests/KLING-SCENE13-PROCESSION-001/KLING-SCENE13-PROCESSION-001-01.mp4'
im=Image.new('RGB',(1280,660))
for i,f in enumerate(range(0,168,18)):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/24),'-i',str(p),'-frames:v','1','-vf','scale=320:180','-f','image2pipe','-vcodec','png','-']);x=i%4*320;y=i//4*220;im.paste(Image.open(io.BytesIO(b)),(x,y));ImageDraw.Draw(im).text((x,y+185),str(f),fill='white')
im.save(o/'review.jpg')

