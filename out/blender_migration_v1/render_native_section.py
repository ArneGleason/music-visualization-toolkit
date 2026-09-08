"""Numbered native context with master audio once, no retired flash."""
import sys,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1]
name=sys.argv[1];a,z=map(int,sys.argv[2:4]);B='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
raw=O/f'{name}_raw.mp4'
with (O/f'{name}_preview.log').open('w') as log:
 subprocess.run([B,'-b','-t','6','--python-exit-code','1','-P',str(O/'full_native_preview.py'),'--','--proxy','--start',str(a),'--end',str(z-1),'--shotlist',str(O/'full_native_review_draft.json'),'--lyric-flat','shots/lyric_motion_full.json','--save-blend',str(O/f'{name}_assembly.blend'),'--out',str(raw)],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
audio=f'[1:a]atrim=start={a/24}:end={min(z,4782)/24},asetpts=PTS-STARTPTS,apad=whole_dur={(z-a)/24}[a]'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-i',str(R/'audio/song.wav'),'-filter_complex',audio,'-map','0:v','-map','[a]','-frames:v',str(z-a),'-c:v','copy','-c:a','aac','-b:a','256k',str(O/f'{name}_context.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(O/f'{name}_context.mp4'),'-f','null','-'],check=True)
