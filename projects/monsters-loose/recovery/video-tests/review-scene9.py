from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io,sys
r=Path(__file__).resolve().parent;n=sys.argv[1];o=r/f'KLING-SCENE9-{n.upper()}-001'
src=o/(o.name+'-01.mp4')
frames=list(map(int,sys.argv[2:])) or list(range(0,120,8))
out=Image.new('RGB',(1600,255*((len(frames)+3)//4)))
for i,f in enumerate(frames):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/24),'-i',str(src),'-frames:v','1','-vf','scale=400:225','-f','image2pipe','-vcodec','mjpeg','-'])
 im=Image.open(io.BytesIO(b));x=i%4*400;y=i//4*255;out.paste(im,(x,y))
 ImageDraw.Draw(out).text((x+8,y+233),f'{n} source {f}',fill='white')
out.save(o/'review.jpg')
