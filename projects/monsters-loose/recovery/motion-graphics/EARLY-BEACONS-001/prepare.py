from pathlib import Path
import json,subprocess,numpy as np
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');o=Path(__file__).resolve().parent
shots=json.loads((r/'shots/shotlist.json').read_text())['shots'][1:5]
coords={'OPEN-LANDING':[(68,5),(29,70),(166,93),(291,128),(383,32)],'HARPER-INTRO':[(658,60),(458,8),(548,150)],'HARPER-BOLT':[(659,53),(681,69)],'STEALTH-POV':[(151,26),(225,53)]}
config=[]
previous={c["id"]:c for c in json.loads((o/"shots.json").read_text())} if (o/"shots.json").exists() else {}
for sh in shots:
 name=sh['id'];sh=dict(sh)
 if name in previous:sh['source']=previous[name]['input_source']
 dest=o/name;dest.mkdir(exist_ok=True);src=r/sh['source']
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(src)]))['streams'][0]
 a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vf','scale=960:540','-f','rawvideo','-pix_fmt','rgb24','-']),np.uint8).reshape(-1,540,960,3)
 tracks={};visibility={}
 for i,(xx,yy) in enumerate(coords[name]):
  ex,ey=xx*1.2,yy*1.2;rows=[];vis=[]
  for f,im in enumerate(a):
   # Narrow red-feature search follows modest perspective, bob and lens motion.
   x=int(round(ex));y=int(round(ey));x0=max(0,x-10);y0=max(0,y-8)
   patch=im[y0:min(540,y+9),x0:min(960,x+11)].astype(float)
   score=patch[:,:,0]-np.maximum(patch[:,:,1],patch[:,:,2]);py,px=np.unravel_index(score.argmax(),score.shape)
   seen=float(score.max()>25)
   if seen:
    x=x0+int(px);y=y0+int(py);ex,ey=x,y
   bg=np.median(np.concatenate([patch[0],patch[-1],patch[:,0],patch[:,-1]]),axis=0)/255
   rows.append([x,y,bg.tolist()]);vis.append(seen)
  tracks[str(i)]=rows;visibility[str(i)]=vis
 (dest/'tracks.json').write_text(json.dumps(tracks),encoding='utf-8');(dest/'visibility.json').write_text(json.dumps(visibility),encoding='utf-8')
 s=(r/'motion-graphics/TOUR-LIGHTS-001/build.py').read_text()
 s=s.replace('s.frame_end=145',f's.frame_end={len(a)}').replace('s.render.resolution_x=1916',f's.render.resolution_x={probe["width"]}').replace('s.render.resolution_y=1080',f's.render.resolution_y={probe["height"]}').replace('master=f-1+1495',f'master=f-1+{sh["start_frame"]-sh["source_in_frame"]}').replace('Tour-lights-v001.blend',name+'-beacons-v001.blend')
 # Preserve the established pulse shape while scaling halos for these distant lamps.
 s=s.replace('mute.scale=(7,7,1)','mute.scale=(5,5,1)').replace('halo.scale=(12,12,1)','halo.scale=(8,8,1)').replace('core.scale=(3.2,3.2,1)','core.scale=(2.7,2.7,1)').replace('hot.scale=(1.5,1.5,1)','hot.scale=(1.2,1.2,1)')
 (dest/'build.py').write_text(s,encoding='utf-8')
 conf={'id':name,'input_source':sh['source'],'output_source':f'motion-graphics/EARLY-BEACONS-001/{name}/{name}-beacons-v001.mp4','frames':len(a),'master_start_frame':sh['start_frame'],'master_end_frame_exclusive':sh['end_frame_exclusive'],'source_in_frame':sh['source_in_frame'],'period_frames':29,'sigma_frames':3.4,'stagger_frames':4,'coordinates_space':'960x540','visible_counts':{k:sum(v) for k,v in visibility.items()}}
 (dest/'timing.json').write_text(json.dumps(conf,indent=2),encoding='utf-8');config.append(conf);print(name,len(a),'frames',conf['visible_counts'],flush=True)
(o/'shots.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
