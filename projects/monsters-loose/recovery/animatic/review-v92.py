import json,subprocess,io
from pathlib import Path
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parent.parent
v=r/'animatic/MonstersLoose-v92-outro-performances.mp4'
frames=[4413,4436,4478,4516,4553,4606,4684,4760,4870,4951,5140,5290]
sheet=Image.new('RGB',(1440,1160),(25,25,25));draw=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
 raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str((f-1)/24),'-i',str(v),'-frames:v','1','-vf','scale=480:270','-f','image2pipe','-vcodec','png','-threads','1','-'])
 im=Image.open(io.BytesIO(raw));x=i%3*480;y=i//3*290
 sheet.paste(im,(x,y));draw.text((x+5,y+274),'Master frame '+str(f),fill='white')
sheet.save(r/'motion-graphics/OUTRO-001/assembled-review.jpg')
hashes=[]
for name in ['MonstersLoose-v91-swamp-meeting.mp4','MonstersLoose-v92-outro-performances.mp4']:
 hashes.append(subprocess.check_output(['ffmpeg','-v','error','-i',str(r/'animatic'/name),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).decode().strip())
print('Audio stream identical:',hashes[0]==hashes[1])
print('Audio hashes:',hashes)
assert hashes[0]==hashes[1]
