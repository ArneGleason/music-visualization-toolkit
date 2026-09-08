"""End-to-end decode, soundtrack alignment and each-cut picture selection."""
import json,subprocess,sys,hashlib
from pathlib import Path
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
movie=O/'full_native_context.mp4';probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(movie)]))['streams'];v=next(s for s in probe if s['codec_type']=='video')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1280,720,'24/1',4854)
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
def audio(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype='<f4')
a=audio(movie);b=audio(R/'audio/song.wav');n=min(len(a),len(b),1594000);correlation=float(np.corrcoef(a[:n],b[:n])[0,1]);assert correlation>.985,correlation
actual=json.loads((O/'full_blend_check.json').read_text())['checks'];selected=json.loads((O/'full_selection_check.json').read_text());cap=cv2.VideoCapture(str(movie));results=[];tiles=[]
for i,(shot,meta) in enumerate(zip(actual,selected),1):
 start,end=meta['song_frames'];frame=(start+end)//2;cap.set(cv2.CAP_PROP_POS_FRAMES,frame);ok,picture=cap.read();assert ok
 source=cv2.VideoCapture(shot['file']);source.set(cv2.CAP_PROP_POS_FRAMES,shot['source_in']+frame-start);ok,expected=source.read();source.release();assert ok,(i,shot)
 expected=cv2.resize(expected,(1280,720),interpolation=cv2.INTER_LINEAR)
 error=float(np.abs(picture[40:500,40:1150].astype(float)-expected[40:500,40:1150]).mean())
 results.append({'review_number':i,'song_frame':frame,'picture_mean_difference':error,'selection_check_pass':error<8})
 tile=cv2.resize(picture,(384,216));cv2.putText(tile,str(i),(12,25),cv2.FONT_HERSHEY_SIMPLEX,.7,(255,255,255),2);tiles.append(tile)
 if len(tiles)==16 or i==len(actual):
  while len(tiles)<16:tiles.append(np.zeros((216,384,3),np.uint8))
  cv2.imwrite(str(O/f'full_review_contact_{(i-1)//16+1}.jpg'),np.vstack([np.hstack(tiles[k:k+4]) for k in range(0,16,4)]));tiles=[]
cap.release();report={'frames':4854,'fps':24,'resolution':[1280,720],'master_audio_zero_lag_correlation':correlation,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'cut_checks':results,'issues':[r for r in results if not r['selection_check_pass']]}
(O/'full_delivery_check.json').write_text(json.dumps(report,indent=2));assert not report['issues'],report['issues']
print('Full delivery: decode, dimensions, clocks, audio and70cut pictures checked.')
