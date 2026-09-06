"""Isolated four-shot, phrase-contained opening using the shared assembler."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from assembly_timebase import conform_clip

def run(args, **kw):
    subprocess.run([str(a) for a in args], cwd=ROOT, check=True, **kw)

tracked = [ROOT/'shots/shotlist.json', ROOT/'generated/overlay_cues.json']
before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
edl = json.loads(tracked[0].read_text())
cues = json.loads(tracked[1].read_text())
cuts = {'s001': (0,86), 's002': (86,155), 's003': (155,334), 's004': (334,476)}
edl['shots'] = [s for s in edl['shots'] if s['id'] in cuts]
edl['duration_sec'] = 476/24
for s in edl['shots']:
    start, end = cuts[s['id']]
    s.update(start_sec=start/24, end_sec=end/24, dur_sec=(end-start)/24, frames=end-start)
    if s['id'] in ('s003','s004'):
        file = ('out/opening_performance_v3/synced.mp4' if s['id']=='s003'
                else 'out/opening_specimen_v2/base.mp4')
        s['clip'] = conform_clip(ROOT, {'file':file,'in_sec':.5,'speed':1},24,prepare=True)
cues['shots'] = [s for s in cues['shots'] if s['id'] in cuts]
for s in cues['shots']:
    s['start'], s['end'] = cuts[s['id']]
cues['frames'], cues['duration_sec'] = 476, 476/24
assert cuts['s003'][1] >= 332
assert cuts['s004'][0] <= 387 and cuts['s004'][1] >= 464
for a,b in zip(edl['shots'],edl['shots'][1:]):
    assert round(a['end_sec']*24)==round(b['start_sec']*24)
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'render.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe', '-b',
         '--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy',
         '--start','0','--end','475','--shotlist',OUT/'shotlist.json',
         '--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],
        stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav',
     '-filter_complex','[0:v]setpts=PTS-STARTPTS[v];[1:a]atrim=start=0:end=19.833333333333,asetpts=PTS-STARTPTS[a]',
     '-map','[v]','-map','[a]','-frames:v','476','-c:v','libx264','-preset','fast',
     '-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k',
     '-movflags','+faststart',OUT/'preview.mp4'])
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in before.items())
print('476 frames rendered; production shotlist and cues unchanged.')
