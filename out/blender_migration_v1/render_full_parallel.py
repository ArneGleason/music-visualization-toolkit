"""Native Blender interval renders, lossless stream join, master audio once."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,hashlib
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'full_parts';D.mkdir(exist_ok=True)
B='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
cuts=[0,856,1650,2484,3300,4177,4854]
def render(job):
 i,a,z=job;p=D/f'part{i}.mp4'
 with (D/f'part{i}.log').open('w') as log:
  subprocess.run([B,'-b',str(O/'full_native_assembly.blend'),'-t','4','--python-exit-code','1','-P',str(O/'render_full_fragment.py'),'--',str(a),str(z),str(p)],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
 v=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(p)]))['streams'][0]
 assert int(v['nb_frames'])==z-a and v['r_frame_rate']=='24/1',(i,v)
 return {'part':i,'song_frames':[a,z],'file':str(p),'frames':z-a}
with ThreadPoolExecutor(max_workers=3) as pool:records=list(pool.map(render,[(i,cuts[i],cuts[i+1]) for i in range(len(cuts)-1)]))
# This only packages already-rendered frames, with no external compositing.
(D/'concat.txt').write_text(''.join("file '"+Path(v['file']).as_posix()+"'\n" for v in records))
raw=O/'full_native_raw.mp4';out=O/'full_native_context.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(D/'concat.txt'),'-c','copy',str(raw)],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-i',str(R/'audio/song.wav'),'-filter_complex','[1:a]atrim=start=0:end=199.25,asetpts=PTS-STARTPTS,apad=whole_dur=202.25[a]','-map','0:v','-map','[a]','-frames:v','4854','-c:v','copy','-c:a','aac','-b:a','256k',str(out)],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
(O/'full_render_receipt.json').write_text(json.dumps({'status':'render_complete_pending_full_visual_check','parts':records,'frames':4854,'fps':24,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2))
