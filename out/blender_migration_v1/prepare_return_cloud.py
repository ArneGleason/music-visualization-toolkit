"""Keep the room-return and light-down source frames on one particle clock."""
import json,subprocess,shutil,numpy as np
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'return_cloud';(D/'plates').mkdir(parents=True,exist_ok=True)
for folder,file,first,last in [('return','out/outro_closing_generations_v1/B3/base.mp4',122,144),('exit','out/outro_closing_generations_v1/B3/take1/base.mp4',153,192)]:
 dest=D/folder;dest.mkdir(exist_ok=True)
 if not (dest/f'{last-first:04d}.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/file),'-vf',f'fps=24,trim=start_frame={first}:end_frame={last},setpts=PTS-STARTPTS',str(dest/'%04d.png')],check=True)
for f in range(1,89):
 source=D/'return'/f'{min(f,22):04d}.png' if f<50 else D/'exit'/f'{f-49:04d}.png'
 shutil.copyfile(source,D/'plates'/f'{f:04d}.png')
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'audio/song.wav'),'-ac','1','-ar','24000','-f','f32le','-']),dtype='<f4')
env=np.array([np.sqrt(np.mean(audio[i*1000:(i+1)*1000]**2)) for i in range(4782)]);env=np.clip(env/(np.percentile(env[4362:4782],85)+1e-8),0,1)
(D/'controls.json').write_text(json.dumps({'frames':[{'song_frame':4622+i,'env':float(env[4622+i]),'base_fx':int(i<22)} for i in range(88)],'visible_intervals':[[4622,4644],[4671,4710]],'hidden_hold':[4644,4671]},indent=2))
