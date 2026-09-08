"""Validate native reveal and prepare an isolated, registry-aware context."""
import json,subprocess,hashlib,sys,numpy as np
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'world';BL='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
def run(args):subprocess.run([str(a) for a in args],cwd=R,check=True)
files=list((D/'native_1280').glob('*.png'));assert len(files)==111
resolution=[];tiles=[]
for frame in [1,7,10,16,25,42,60,111]:
 a=cv2.imread(str(D/'native_1280'/f'{frame:04d}.png'));hi=cv2.imread(str(D/'native_1920'/f'{frame:04d}.png'))
 assert a.shape==(720,1280,3) and hi.shape==(1080,1920,3)
 resolution.append({'frame':frame,'mean_1080_downsample_difference':float(np.abs(a.astype(float)-cv2.resize(hi,(1280,720),interpolation=cv2.INTER_AREA)).mean())})
 tile=cv2.resize(a,(384,216));cv2.putText(tile,f'26 / {2121+frame}',(10,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1);tiles.append(tile)
cv2.imwrite(str(D/'contact.jpg'),np.vstack([np.hstack(tiles[:4]),np.hstack(tiles[4:])]))
clean=D/'native_clean.mp4';run(['ffmpeg','-v','error','-y','-framerate','24','-i',D/'native_1280/%04d.png','-frames:v','111','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',clean])
edl=json.loads((O/'waking_shotlist.json').read_text());shot=next(q for q in edl['shots'] if q['id']=='world_pullback_timing_test');shot['clip']={'file':str(clean.relative_to(R)).replace('\\','/'),'in_sec':0,'speed':1}
(O/'world_shotlist.json').write_text(json.dumps(edl,indent=2))
with (D/'context.log').open('w') as log:
 subprocess.run([BL,'-b','-t','8','--python-exit-code','1','-P',str(O/'batch3_preview.py'),'--','--proxy','--start','2122','--end','2232','--shotlist',str(O/'world_shotlist.json'),'--lyric-flat','shots/lyric_motion_full.json','--out',str(D/'context_raw.mp4')],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
run(['ffmpeg','-v','error','-y','-i',D/'context_raw.mp4','-i',R/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={2122/24}:end={2233/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','111','-c:v','copy','-c:a','aac','-b:a','256k',O/'world_context.mp4'])
for file in [clean,O/'world_context.mp4']:
 run(['ffmpeg','-v','error','-i',file,'-f','null','-'])
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=nb_frames,r_frame_rate,codec_type','-of','json',str(file)]))['streams'];video=next(x for x in probe if x['codec_type']=='video');assert int(video['nb_frames'])==111 and video['r_frame_rate']=='24/1'
qa={'status':'native_reveal_technical_checks_complete','song_frames':[2122,2233],'frames':111,'fps':24,'resolution':resolution,
 'source_images':['codex/out/forest_walk_track_b.jpg','codex/out/signal_crossing_space_a.jpg'],
 'intentional_approximation':'Native noise nebula and procedural stars preserve composition/palette, not the exact old random texture. Authored polygon silhouette remains a still-image cutout, not moving footage roto.',
 'production_promoted':False,'clean_sha256':hashlib.sha256(clean.read_bytes()).hexdigest()}
(D/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
