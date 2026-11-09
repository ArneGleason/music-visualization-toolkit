"""Local tracked petal hue correction; preserves the separate flower in the vase."""
import json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter

BASE = Path(__file__).resolve().parents[1]
OUT = BASE/'generated/color-corrections/april-yellow-v001'
SOURCE = BASE/'generated/kling-tests/april-bloom-v001/april-original-1080p.mp4'
OUT.mkdir(parents=True, exist_ok=True)
# Source-frame coordinates, following only the flower carried with the bouquet.
KEYS = np.array([
 [0,945,320], [24,947,320], [48,948,323], [66,960,318],
 [72,950,302], [78,950,275], [84,936,188], [90,902,98],
 [96,944,56], [99,1030,80], [100,1065,92], [101,1100,114],
 [102,1127,144], [103,1170,168], [104,1200,202], [105,1230,230],
 [106,1260,270], [107,1286,314], [108,1310,350],
 [109,1330,400], [110,1342,438], [111,1365,478], [112,1375,518],
 [113,1380,535], [114,1372,548], [116,1376,546], [117,1383,544],
 [118,1385,535], [119,1397,553], [120,1410,560], [121,1420,552],
 [122,1440,545], [123,1460,530], [124,1510,506], [125,1520,500], [126,1535,545]
], dtype=float)
W,H,FPS = 1916,1080,24
count = 193
frames = []
reader = subprocess.Popen(['ffmpeg','-v','error','-i',str(SOURCE),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
writer = subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'april-yellow-full-silent.mp4')],stdin=subprocess.PIPE)
for f in range(count):
 raw=reader.stdout.read(W*H*3); assert len(raw)==W*H*3
 original=Image.frombytes('RGB',(W,H),raw)
 corrected=original.copy()
 if f<=126:
  cx=np.interp(f,KEYS[:,0],KEYS[:,1]); cy=np.interp(f,KEYS[:,0],KEYS[:,2])
  rx,ry=(32,36) if f<80 else ((39,33) if f<111 else (44,46))
  x0,x1=max(0,int(cx-rx-5)),min(W,int(cx+rx+6));y0,y1=max(0,int(cy-ry-5)),min(H,int(cy+ry+6))
  patch=original.crop((x0,y0,x1,y1));hsv=np.asarray(patch.convert('HSV')).astype(float);rgb=np.asarray(patch).astype(float)
  yy,xx=np.mgrid[y0:y1,x0:x1];distance=((xx-cx)/rx)**2+((yy-cy)/ry)**2
  spatial=np.clip((1.05-distance)/.18,0,1)
  hue=hsv[:,:,0];hue=np.where(hue>240,hue-255,hue)
  red=np.clip((20-hue)/6,0,1)*np.clip((hsv[:,:,1]-65)/35,0,1)*np.clip((rgb[:,:,0]-rgb[:,:,1]-25)/25,0,1)
  alpha=gaussian_filter(spatial*red,.65)
  # The last petals become occluded in the landed bouquet; taper only at disappearance.
  if f>124:alpha*=max(0,(127-f)/3)
  target=hsv.copy();target[:,:,0]=34;target[:,:,1]*=.88
  recolored=np.asarray(Image.fromarray(target.astype(np.uint8),'HSV').convert('RGB')).astype(float)
  result=np.clip(rgb+(recolored-rgb)*alpha[:,:,None],0,255).astype(np.uint8)
  corrected.paste(Image.fromarray(result),(x0,y0))
  frames.append(dict(frame=f,x=round(cx,2),y=round(cy,2),changedPixels=int((alpha>.05).sum())))
  if f in [0,45,72,84,96,102,106,110,114,118,122,125]:
   before=original.crop((max(0,int(cx)-90),max(0,int(cy)-70),int(cx)+90,int(cy)+70));after=corrected.crop((max(0,int(cx)-90),max(0,int(cy)-70),int(cx)+90,int(cy)+70))
   pair=Image.new('RGB',(360,160),'#202020');pair.paste(before,(0,20));pair.paste(after,(180,20));ImageDraw.Draw(pair).text((4,3),f'Frame {f}: original / yellow',fill='white');pair.save(OUT/f'check-{f:03}.png')
 writer.stdin.write(corrected.tobytes())
reader.stdout.close();assert reader.wait()==0;writer.stdin.close();assert writer.wait()==0
(OUT/'tracking.json').write_text(json.dumps(dict(source=str(SOURCE.relative_to(BASE)),keyframes=KEYS.tolist(),frames=frames,method='Keyframed local elliptical mask intersected with soft coral hue key; preserve value/ink, shift petal hue to yellow. No edits after source126.'),indent=2)+'\n')
subprocess.run(['ffmpeg','-y','-v','error','-i',str(OUT/'april-yellow-full-silent.mp4'),'-ss',str(571/24),'-i',str(BASE/'generated/source/master.wav'),'-filter_complex','[0:v]trim=start_frame=45:end_frame=169,setpts=PTS-STARTPTS,pad=1920:1080:2:0[v]','-map','[v]','-map','1:a','-frames:v','124','-t',str(124/24),'-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','320k','-movflags','+faststart',str(OUT/'april-yellow-edit-1080p.mp4')],check=True)
print(OUT/'april-yellow-edit-1080p.mp4')
