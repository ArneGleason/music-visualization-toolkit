from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io,sys
r=Path(__file__).resolve().parent.parent
for name in sys.argv[1:]:
 o=r/('video-tests/KLING-PORTRAIT-'+name.upper()+'-001');src=o/(o.name+'-01.mp4');out=Image.new('RGB',(1600,960))
 for i,f in enumerate([12,24,36,48,60,72,84,96,108,120,132,143]):
  b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/24),'-i',str(src),'-frames:v','1','-vf','scale=400:225','-f','image2pipe','-vcodec','mjpeg','-']);im=Image.open(io.BytesIO(b));x=i%4*400;y=i//4*320;out.paste(im,(x,y));ImageDraw.Draw(out).text((x+8,y+235),f'{name} source {f}',fill='white')
 out.save(o/'review.jpg')
