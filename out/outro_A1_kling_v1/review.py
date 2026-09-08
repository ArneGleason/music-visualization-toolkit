"""Verify the return and preview two assigned cuts with a B still placeholder."""
import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_timebase import conform_clip
source=OUT/'synced.mp4'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='4878c1a15925030d58bdc44ce2120b8906fd1e5f99de40e39716a13b0202cf48'
subprocess.run(['ffmpeg','-v','error','-i',str(source),'-f','null','-'],check=True)
def samples(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype='<f4').astype(float)
a=samples(OUT/'guide.wav'); b=samples(source)
scores=[]
for lag in range(-800,801):
    x=a[max(0,-lag):]; y=b[max(0,lag):]; n=min(len(x),len(y)); x=x[:n]; y=y[:n]
    scores.append(float(np.sum(x*y)/np.sqrt(np.sum(x*x)*np.sum(y*y))))
lag=(int(np.argmax(scores))-800)/8000
cfr=conform_clip(ROOT,{'file':source.relative_to(ROOT).as_posix(),'speed':1},24,prepare=True)
filtergraph='[0:v]trim=start_frame=12:end_frame=67,setpts=PTS-STARTPTS[a];[1:v]scale=1280:720,setsar=1,trim=end_frame=30,setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=97:end_frame=166,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v];[2:a]atrim=start='+str(4177/24)+':end='+str(4331/24)+',asetpts=PTS-STARTPTS[sound]'
subprocess.run(['ffmpeg','-v','error','-n','-i',cfr['file'],'-loop','1','-framerate','24','-i',str(ROOT/'out/outro_anchors_v2/exobiologist.png'),'-i',str(ROOT/'audio/song.wav'),'-filter_complex',filtergraph,'-map','[v]','-map','[sound]','-frames:v','154','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(154/24),'-movflags','+faststart',str(OUT/'exchange_review.mp4')],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,r_frame_rate','-of','json',str(OUT/'exchange_review.mp4')]))
assert int(probe['streams'][0]['nb_read_frames'])==154
report={'source_hash_matches':True,'source_full_decode':True,'returned_audio_best_lag_seconds':lag,'returned_audio_correlation_at_zero':scores[800],'returned_audio_best_correlation':max(scores),'audio_check_limit':'Audio alignment is not proof of mouth alignment.','conformed':cfr,'preview_song_frames':[4177,4331],'preview_frames':154,'middle_B':'Approved static anchor, not generated/lipsynced B1','boundary_note':'Claude reports other-speaker mouth onset around2.7s, which overlaps end of source12..67 (2.7917s) by about2frames. Do not claim entirely outside first cut. Leave unchanged for review; original listening tail is possible local fix.'}
(OUT/'codex_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
