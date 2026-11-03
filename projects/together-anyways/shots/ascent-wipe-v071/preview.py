import json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tools'))
from animatic_media import Artwork
p=Path('projects/together-anyways');score=json.loads((p/'shots/shotlist.json').read_text());shots=[s for s in score['shots'] if s['id'] in ['S13-SH01','S13-SH02']];a=Artwork(p,shots,24);boundary=shots[1]['startFrame'];start=boundary-36;end=boundary+48;project=json.loads((p/'project.json').read_text());out=p/'generated/ascent-wipe-v071/wipe-preview.mp4';proc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1008','-r','24','-i','pipe:0','-ss',str(start/24),'-i',str(p/project['sources']['audio']),'-frames:v',str(end-start),'-t',str((end-start)/24),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac',str(out)],stdin=subprocess.PIPE)
for frame in range(start,end):proc.stdin.write(a.at(shots[0] if frame<boundary else shots[1],frame).tobytes())
proc.stdin.close();assert proc.wait()==0
print(out)
