"""Verify returned takes and replace the message-test placeholders on exact clocks."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(a):subprocess.run([str(x) for x in a],cwd=ROOT,check=True)
sources={
 'astronaut':('out/meaning_exchange_handoff_v1/astronaut/take3/synced.mp4','66ccdb53e129368d36fe200b067f54b2feff9e8fed430d7ed302272c2b806e76'),
 'astronomer':('out/meaning_exchange_handoff_v1/astronomer/base.mp4','9e2931728f3357b2d7ab07d8488cc93bd7cf4d966537b6abb6c142e5ae20e72e')}
verified={}
for name,(path,digest) in sources.items():
    p=ROOT/path;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
    run(['ffmpeg','-v','error','-i',p,'-f','null','-'])
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,width,height,duration','-of','json',str(p)]))
    verified[name]=probe['streams'][0]
run(['ffmpeg','-v','error','-y','-i',ROOT/sources['astronaut'][0],'-vf','fps=24','-an','-c:v','libx264','-crf','16',OUT/'astronaut_24.mp4'])
def audio(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a=audio(ROOT/sources['astronaut'][0]);b=audio(ROOT/'out/meaning_exchange_handoff_v1/astronaut/guide.wav');n=min(len(a),len(b))
corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.98
verified['guide_correlation_zero_lag']=corr
verified['status']='verified return; combined preview pending owner review'
# Execute only the existing recipe construction, then substitute fresh source readers.
wrapper=(ROOT/'out/meaning_orb_loop_v4/render.py').read_text().replace('meaning_orb_loop_v4','meaning_exchange_live_v5')
prefix=wrapper.rsplit('exec(compile(source,',1)[0]
ns={'__file__':str(OUT/'expanded.py')};exec(compile(prefix,'build_loop_recipe','exec'),ns)
source=ns['source']
source=source.replace("ROOT/'out/astronaut_reply_v1/base.mp4'","ROOT/'out/meaning_exchange_live_v5/astronaut_24.mp4'")
old="listener=cv2.imread(str(ROOT/'out/meaning_thread_trial_v1/listener_still.jpg'));assert listener is not None"
assert old in source
source=source.replace(old,"listener_cap=cv2.VideoCapture(str(ROOT/'out/meaning_exchange_handoff_v1/astronomer/base.mp4'))\nlistener_cap.set(cv2.CAP_PROP_POS_FRAMES,12)\nlistener=np.zeros((720,1280,3),np.uint8)")
source=source.replace('    incoming=listener','    if sf>=2786:\n        ok,listener=listener_cap.read();assert ok\n    incoming=listener')
# Position the arrival in the new wider listener's receptive desk-side space.
source=source.replace('center=np.array([680-420*q,555-90*q])','center=np.array([680-340*q,555-25*q])')
exec(compile(source,str(OUT/'expanded.py'),'exec'),{'__name__':'__main__','__file__':str(OUT/'expanded.py')})
verified.update(astronaut_song_origin=2646,astronaut_visible=[2658,2826],astronaut_source=[12,180],astronomer_song_origin=2774,astronomer_visible=[2786,2881],astronomer_source=[12,107],preview=[2620,2881])
(OUT/'verification.json').write_text(json.dumps(verified,indent=2))
print('Live message handoff verified; guide correlation',corr,flush=True)
