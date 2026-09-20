from pathlib import Path
import json,subprocess,numpy as np
r=Path(__file__).resolve().parents[2];o=Path(__file__).resolve().parent
src=r/'video-tests/KLING-HABITATS-001/KLING-HABITATS-001-01.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(src)]))['streams'][0]
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vf','fps=24,scale=960:540','-f','rawvideo','-pix_fmt','rgb24','-']),np.uint8).reshape(-1,540,960,3)
# Roof junctions, with local image-template tracking. Validate sampled overlays.
anchors=[(529,28),(474,138),(800,138),(601,318),(867,20)]
gray=a.astype(np.float32).mean(axis=3);tracks={};visibility={}
for i,(x,y) in enumerate(anchors):
 rows=[];template=gray[0,y-8:y+9,x-8:x+9].copy()
 for f in range(len(a)):
  if f:
   best=None
   for dy in range(-4,5):
    for dx in range(-4,5):
     xx=x+dx;yy=y+dy
     if xx<9 or yy<9 or xx>=951 or yy>=531:continue
     patch=gray[f,yy-8:yy+9,xx-8:xx+9];err=np.mean(((patch-patch.mean())-(template-template.mean()))**2)
     score=err+.2*(dx*dx+dy*dy)
     if best is None or score<best[0]:best=(score,xx,yy)
   _,x,y=best
   template=.85*template+.15*gray[f,y-8:y+9,x-8:x+9]
  rows.append([x,y,[0,0,0]])
 tracks[str(i)]=rows;visibility[str(i)]=[1]*len(a)
(o/'tracks.json').write_text(json.dumps(tracks));(o/'visibility.json').write_text(json.dumps(visibility))
s=(r/'motion-graphics/TOUR-LIGHTS-001/build.py').read_text().replace('s.frame_end=145',f's.frame_end={len(a)}').replace('s.render.resolution_x=1916',f's.render.resolution_x={probe["width"]}').replace('s.render.resolution_y=1080',f's.render.resolution_y={probe["height"]}').replace('master=f-1+1495','master=f-1+2024').replace('Tour-lights-v001.blend','Habitat-lights-v001.blend')
s=s.replace('ma.default_value=.94','ma.default_value=0').replace('halo.scale=(12,12,1)','halo.scale=(7,7,1)').replace('core.scale=(3.2,3.2,1)','core.scale=(2,2,1)').replace('hot.scale=(1.5,1.5,1)','hot.scale=(.85,.85,1)')
(o/'build.py').write_text(s)
(o/'timing.json').write_text(json.dumps({'fps':24,'frames':len(a),'source_zero_master_frame':2024,'master_start':2036,'master_end_exclusive':2092,'source_in_frame':12,'source_out_frame_exclusive':68,'period_frames':29,'sigma_frames':3.4,'stagger_frames':4,'coordinates_space':'960x540','input_source':str(src),'tracking':'Local normalized patch matching; five roof junctions; manually review before conform.'},indent=2))
print('Prepared',len(a),'frames and five roof tracks')
