from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io
r=Path(__file__).resolve().parent
src=r/'MonstersLoose-v70-scene9-performances.mp4'
frames=[2906,2940,2956,2973,2986,3026,3031,3058,3087,3088,3095,3103,3128,3158,3185,3222]
im=Image.new('RGB',(1600,1020))
for i,f in enumerate(frames):
 b=subprocess.check_output(['ffmpeg','-v','error','-ss',str((f-1)/24),'-i',str(src),'-frames:v','1','-vf','scale=400:225','-f','image2pipe','-vcodec','png','-'])
 im.paste(Image.open(io.BytesIO(b)),(i%4*400,i//4*255));ImageDraw.Draw(im).text((i%4*400+6,i//4*255+234),str(f),fill='white')
im.save(r/'review-v70.jpg')
