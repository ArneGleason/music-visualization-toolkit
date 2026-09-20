from pathlib import Path
import json,subprocess,numpy as np
r=Path(__file__).resolve().parents[2];o=Path(__file__).resolve().parent
for name,anchor,start in [('insectarium',(868,59),2118),('exobiology',(805,92),2144)]:
 dest=o/name;dest.mkdir(exist_ok=True);src=r/f'motion-graphics/CREATURE-PORTRAITS-001/{name}-push-v001.mp4'
 a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vf','scale=960:540','-f','rawvideo','-pix_fmt','rgb24','-']),np.uint8).reshape(-1,540,960,3)
 rows=[];x,y=anchor
 for im in a:
  x0=x-10;y0=y-8;patch=im[y0:y+9,x0:x+11].astype(float);score=patch[:,:,0]-np.maximum(patch[:,:,1],patch[:,:,2]);yy,xx=np.unravel_index(score.argmax(),score.shape);x=x0+int(xx);y=y0+int(yy)
  near=im[y-10:y+11,x-10:x+11];bg=np.median(np.concatenate([near[0],near[-1],near[:,0],near[:,-1]]),axis=0)/255;rows.append([x,y,bg.tolist()])
 (dest/'tracks.json').write_text(json.dumps({'0':rows}));(dest/'visibility.json').write_text(json.dumps({'0':[1]*len(a)}))
 s=(r/'motion-graphics/HABITAT-LIGHTS-001/build.py').read_text().replace('s.frame_end=145','s.frame_end=26').replace('master=f-1+2024',f'master=f-1+{start}').replace('d=(master-7-i*4+14.5)%29-14.5','d=f-9').replace('(d/3.4)','(d/2.4)').replace('mute.scale=(7,7,1);ma.default_value=0','mute.scale=(10,10,1);ma.default_value=.97').replace('ma.default_value=0*visible','ma.default_value=.97*visible').replace('halo.scale=(7,7,1)','halo.scale=(10,10,1)').replace('Habitat-lights-v001.blend',name+'-beacon-v001.blend')
 (dest/'build.py').write_text(s)
 (dest/'timing.json').write_text(json.dumps({'fps':24,'frames':26,'master_start':start,'master_end_exclusive':start+26,'source_in_frame':0,'peak_local_frame_one_based':9,'peak_master_frame':start+8,'sigma_frames':2.4,'single_pulse':True,'timing_intent':'Same8frame delay after each cut reinforces edit rhythm; not claimed beat-grid alignment','input_source':str(src)},indent=2))
