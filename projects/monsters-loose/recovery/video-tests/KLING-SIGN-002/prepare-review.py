import subprocess,json
import numpy as np
from pathlib import Path
p=Path(__file__).resolve().parent
def run(args):subprocess.run(['ffmpeg','-y','-v','error',*args],check=True)
def samples(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-vn','-f','f32le','-ac','1','-ar','8000','-']),dtype=np.float32)
a=samples(p/'Harper-sign-vocal-6s.wav');b=samples(p/'KLING-SIGN-002-lipsync.mp4');n=1
while n<len(a)+len(b):n*=2
c=np.fft.irfft(np.fft.rfft(b,n)*np.conj(np.fft.rfft(a,n)),n);ix=int(np.argmax(c));lag=ix if ix<n//2 else ix-n
(p/'lip-sync-audio-check.json').write_text(json.dumps({'returned_audio_lag_seconds':lag/8000,'method':'PCM cross correlation'},indent=2));print('AUDIO_LAG',lag/8000)
run(['-i',str(p/'KLING-SIGN-002-lipsync.mp4'),'-an','-vf','fps=24','-c:v','libx264','-crf','17','-preset','fast','-movflags','+faststart',str(p/'KLING-SIGN-002-lipsync-24fps.mp4')])
for src,dest in [('KLING-SIGN-002-lipsync-24fps.mp4','Harper-sign-retry-lipsync-music-preview.mp4'),('KLING-SIGN-002-01.mp4','Harper-sign-retry-base-music-preview.mp4')]:
 run(['-i',str(p/src),'-i',str(p/'Harper-sign-master-6s.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-shortest','-movflags','+faststart',str(p/dest)])
run(['-i',str(p/'Harper-sign-retry-lipsync-music-preview.mp4'),'-f','null','-'])
f=p/'timing.json';d=json.loads(f.read_text());d.update(status='lip_sync_complete_awaiting_creative_review',edit_source='KLING-SIGN-002-lipsync-24fps.mp4',returned_audio_offset_seconds=lag/8000,edit_conversion='fps24 unchanged playback speed');f.write_text(json.dumps(d,indent=2))
f=p/'lip-sync-request.json';d=json.loads(f.read_text());d['status']='completed_downloaded';f.write_text(json.dumps(d,indent=2))
