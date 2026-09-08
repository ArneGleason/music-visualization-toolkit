import json,sys,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
def run(args,**kw):subprocess.run([str(a) for a in args],cwd=ROOT,check=True,**kw)
cap=cv2.VideoCapture(str(ROOT/'out/garden_eyes_motion_v1/base.mp4'))
encoder=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','24','-i','-',
 '-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'clean.mp4')],stdin=subprocess.PIPE)
for i in range(81):
 ok,f=cap.read();assert ok
 # Blender composites in linear light before display conversion, avoiding
 # highlight clipping from re-multiplying exported translucent RGB sprites.
 composed=cv2.imread(str(OUT/'composite'/f'{i:04d}.png'));assert composed is not None
 encoder.stdin.write(composed.tobytes())
 if i in (0,24,48,80):cv2.imwrite(str(OUT/f'check_{i:03d}.jpg'),composed)
encoder.stdin.close();assert encoder.wait()==0
edl=json.loads((ROOT/'out/garden_eyes_motion_review/shotlist.json').read_text())
cues=json.loads((ROOT/'out/garden_eyes_motion_review/overlay_cues.json').read_text())
edl['shots'][-1]['id']='garden_eyes_airflow_motion_audition'
edl['shots'][-1]['clip']={'file':'out/garden_eyes_airflow_v2/clean.mp4','in_sec':0,'speed':1}
cues['shots'][-1]['id']=edl['shots'][-1]['id']
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'assembly.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py',
 '--','--proxy','--start','1514','--end','1649','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
 '[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start=63.083333333333:end=68.75,asetpts=PTS-STARTPTS[a]',
 '-map','[v]','-map','[a]','-frames:v','136','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
print('Preview complete:136frames. Clean:81frames. Master once. No holds.')
