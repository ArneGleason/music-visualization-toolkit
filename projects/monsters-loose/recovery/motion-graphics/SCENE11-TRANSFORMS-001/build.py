from pathlib import Path
from PIL import Image
import subprocess,json,math,bisect
o=Path(__file__).resolve().parent;r=o.parents[1]
selections=json.loads((o/'source-selections.json').read_text())
w,h=1280,720;size=w*h*3
for name,sel in selections.items():
 src=r/f'video-tests/KLING-SCENE11-{name.upper()}-001/KLING-SCENE11-{name.upper()}-001-01.mp4'
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-'])
 count=len(raw)//size;keys=sel['map'];target=o/f'{name}-timed-v001.mp4'
 enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r','24','-i','-','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',str(target)],stdin=subprocess.PIPE)
 for f in range(sel['frames']):
  j=min(len(keys)-2,max(0,bisect.bisect_right([k[0] for k in keys],f)-1));a,b=keys[j:j+2]
  q=a[1]+(b[1]-a[1])*(f-a[0])/(b[0]-a[0]);lo=math.floor(q);hi=min(count-1,lo+1);frac=q-lo
  assert 0<=lo<count,(name,f,q,count)
  im=Image.frombytes('RGB',(w,h),raw[lo*size:(lo+1)*size])
  if frac>.001:im=Image.blend(im,Image.frombytes('RGB',(w,h),raw[hi*size:(hi+1)*size]),frac)
  enc.stdin.write(im.tobytes())
 enc.stdin.close();assert enc.wait()==0
 del raw
 sel['source']=str(src.relative_to(r));sel['output']=str(target.relative_to(r))
 sel['interpolation']='linear frame blend; no optical-flow geometry'
 print(name,'rendered',flush=True)
(o/'selections.json').write_text(json.dumps(selections,indent=2))
