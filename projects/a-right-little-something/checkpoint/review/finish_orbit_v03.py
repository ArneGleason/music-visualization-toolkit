from pathlib import Path
import json, subprocess, sys
sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import encode, probe

base=Path('projects/a-right-little-something').resolve()
plan=json.loads((base/'orbit-blender-v03.json').read_text())
out=base/plan['output']/'hybrid'
frames=out/'frames'
expected=plan['sourceFrames']
assert all((frames/f'frame_{i:04}.png').exists() for i in range(1,expected+1))
sequence=['-framerate','24','-start_number','1','-i',str(frames/'frame_%04d.png')]
encode(sequence,expected,out/'effects-handles.mp4')
# Work in RGB; Screen on YUV chroma produces an unwanted magenta shift.
graph='[0:v]pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,format=gbrp[plate];[1:v]format=gbrp[fx];[plate][fx]blend=all_mode=screen:shortest=1,format=yuv420p[v]'
encode(['-i',str(base/plan['source']),*sequence,'-filter_complex_threads','2','-filter_complex',graph,'-map','[v]'],expected,out/'orbit-composite-handles.mp4')
assert int(probe(out/'orbit-composite-handles.mp4')['nb_frames'])==expected
print('Orbit composite ready:',expected,'frames')
