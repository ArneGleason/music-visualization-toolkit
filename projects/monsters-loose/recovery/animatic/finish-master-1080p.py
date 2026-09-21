import json,subprocess
from pathlib import Path
p=Path(__file__).resolve().parent
src=p/'MonstersUndone-v94-master-1080p-render.mp4';dst=p/'MonstersUndone-v94-master-1080p.mp4';preview=p/'MonstersUndone-v94.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-i',str(preview),'-map','0:v:0','-map','1:a:0','-c','copy','-metadata','title=Monsters Undone','-metadata','artist=Arne Gleason','-metadata','copyright=© 2026 Arne Gleason','-movflags','+faststart',str(dst)],check=True)
d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dst)]));v=next(s for s in d['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'24/1',5290)
def ahash(f):return subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).decode().strip()
assert ahash(dst)==ahash(preview)
subprocess.run(['ffmpeg','-v','error','-i',str(dst),'-f','null','-'],check=True)
record=dict(file=str(dst),width=1920,height=1080,fps=24,frames=5290,audio_identical=True,decode_check='passed',bytes=dst.stat().st_size,note='Timeline render: native 1080 sources retained; 720p baked effects scaled. Layout and keyframes scaled 1.5x; approved edit unchanged.')
(p/'master-1080p-validation.json').write_text(json.dumps(record,indent=2))
shotpath=p.parent/'shots/shotlist.json';shots=json.loads(shotpath.read_text());shots['final_master']='animatic/'+dst.name;shots['final_master_validation']='animatic/master-1080p-validation.json';shotpath.write_text(json.dumps(shots,indent=2)+'\n')
for name in ['HANDOFF.md','README.md']:
 q=Path('projects/monsters-loose')/name;t=q.read_text(encoding='utf-8');q.write_text('Final 1080p master: animatic/MonstersUndone-v94-master-1080p.mp4 (1920x1080,24fps,5290frames). Approved audio copied exactly. Mixed source resolution: native1080 footage and scaled720 baked effects. Preview remains v94 at720p.\n\n'+t,encoding='utf-8')
print(json.dumps(record))
