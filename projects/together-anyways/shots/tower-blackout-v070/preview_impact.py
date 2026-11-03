import json, subprocess, sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tools'))
from animatic_media import Artwork
p=Path('projects/together-anyways');score=json.loads((p/'shots/shotlist.json').read_text());shots=[s for s in score['shots'] if s['id'] in ['S14-SH01','S14-SH02']]; a=Artwork(p,shots,24); boundary=shots[1]['startFrame']
assert a.at(shots[0],boundary-1).getextrema()==((255,255),)*3
assert a.at(shots[1],boundary+3).getextrema()==((0,0),)*3
assert a.at(shots[1],boundary+7).getextrema()==((0,0),)*3
assert a.at(shots[1],boundary+21).tobytes()==a.frame(shots[1],boundary+21).tobytes()
project=json.loads((p/'project.json').read_text());out=p/'generated/tower-blackout-v070/impact-preview.mp4';cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1008','-r','24','-i','pipe:0','-ss',str(shots[0]['startFrame']/24),'-i',str(p/project['sources']['audio']),'-frames:v',str(sum(s['frames'] for s in shots)),'-t',str(sum(s['frames'] for s in shots)/24),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac',str(out)];proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for shot in shots:
 for frame in range(shot['startFrame'],shot['endFrameExclusive']): proc.stdin.write(a.at(shot,frame).tobytes())
proc.stdin.close();assert proc.wait()==0
print(out)
