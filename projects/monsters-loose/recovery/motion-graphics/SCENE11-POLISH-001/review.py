from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,io
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913/motion-graphics/SCENE11-POLISH-001')
for name,fs in [('shrink-b',[70,75,82,89]),('grow-a',[0,12,24,35]),('grow-b',[30,50,70,88]),('smoke-b',[30,36,42,50])]:
 p=r/f'{name}-polished-v001.mp4'
 if not p.exists():continue
 try:
  im=Image.new('RGB',(1280,210))
  for i,f in enumerate(fs):
   b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(f/24),'-i',str(p),'-frames:v','1','-vf','scale=320:180','-f','image2pipe','-vcodec','png','-']);im.paste(Image.open(io.BytesIO(b)),(i*320,0));ImageDraw.Draw(im).text((i*320,185),str(f),fill='white')
  im.save(r/(name+'-after.jpg'))
 except Exception:pass
