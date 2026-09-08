"""Validate/render contextual native vector-family deliveries without promotion."""
import sys,json,subprocess,hashlib,numpy as np
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];name=sys.argv[1];D=O/name;sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
settings={'orb':(2271,2399,'out/colony_world_blossom_v2/clean.mp4','world_shotlist.json',['mars_colony_reply_test']),
          'meaning':(2658,2881,'out/meaning_exchange_dual_sync_v6/clean.mp4','orb_shotlist.json',['meaning_reply_test','meaning_listener_test'])}
a,z,reference,parent,ids=settings[name];count=z-a
assert len(list((D/'native_1280').glob('*.png')))==count
errors=[];resolution=[];tiles=[];cap=cv2.VideoCapture(str(R/reference))
for i in range(count):
 ok,old=cap.read();assert ok;new=cv2.imread(str(D/'native_1280'/f'{i+1:04d}.png'));assert new is not None
 errors.append(float(np.abs(new.astype(float)-old).mean()))
 hi=D/'native_1920'/f'{i+1:04d}.png'
 if hi.exists():resolution.append({'frame':i+1,'mean_1080_downsample_difference':float(np.abs(new.astype(float)-cv2.resize(cv2.imread(str(hi)),(1280,720),interpolation=cv2.INTER_AREA)).mean())})
 if i in np.linspace(0,count-1,8).astype(int):
  tile=cv2.resize(new,(384,216));cv2.putText(tile,str(a+i),(10,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1);tiles.append(tile)
cap.release();cv2.imwrite(str(D/'contact.jpg'),np.vstack([np.hstack(tiles[:4]),np.hstack(tiles[4:])]))
def run(args):subprocess.run([str(x) for x in args],cwd=R,check=True)
clean=D/'native_clean.mp4';run(['ffmpeg','-v','error','-y','-framerate','24','-i',D/'native_1280/%04d.png','-frames:v',count,'-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',clean])
edl=json.loads((O/parent).read_text());found=[]
for shot in edl['shots']:
 if shot['id'] in ids:
  # Preserve local inpoints for the two-cut continuous exchange.
  shot['clip']['file']=str(clean.relative_to(R)).replace('\\','/');found.append(shot['id'])
assert set(found)==set(ids),found
(O/f'{name}_shotlist.json').write_text(json.dumps(edl,indent=2))
BL='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
with (D/'context.log').open('w') as log:subprocess.run([BL,'-b','-t','8','--python-exit-code','1','-P',str(O/'batch3_preview.py'),'--','--proxy','--start',str(a),'--end',str(z-1),'--shotlist',str(O/f'{name}_shotlist.json'),'--lyric-flat','shots/lyric_motion_full.json','--out',str(D/'context_raw.mp4')],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
run(['ffmpeg','-v','error','-y','-i',D/'context_raw.mp4','-i',R/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={a/24}:end={z/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v',count,'-c:v','copy','-c:a','aac','-b:a','256k',O/f'{name}_context.mp4'])
run(['ffmpeg','-v','error','-i',O/f'{name}_context.mp4','-f','null','-'])
qa={'status':'native_candidate_technical_checks_complete','song_frames':[a,z],'frames':count,'fps':24,'mean_old_difference':float(np.mean(errors)),'max_old_difference':max(errors),'resolution':resolution,'clean_sha256':hashlib.sha256(clean.read_bytes()).hexdigest(),'production_promoted':False}
(D/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
