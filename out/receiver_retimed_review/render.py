import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
START,END=719,911
def run(args,**kw):
    subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[ROOT/'shots/shotlist.json',ROOT/'generated/overlay_cues.json',ROOT/'shots/assembly_decisions.json']
before={str(p):sha(p) for p in paths}
edl=json.loads((ROOT/'out/signal_extension_review/shotlist.json').read_text())
cues=json.loads((ROOT/'out/signal_extension_review/overlay_cues.json').read_text())
original=json.loads(paths[0].read_text()); oc=json.loads(paths[1].read_text())
for sid,a,b,source_in in [('s010',805,856,0),('s011',856,911,137)]:
    s=copy.deepcopy(next(x for x in original['shots'] if x['id']==sid))
    s.update(start_sec=a/24,end_sec=b/24,dur_sec=(b-a)/24,frames=b-a)
    s['clip']['in_sec']=source_in/24
    edl['shots'].append(s)
    c=copy.deepcopy(next(x for x in oc['shots'] if x['id']==sid));c.update(start=a,end=b)
    cues['shots'].append(c)
edl['duration_sec']=cues['duration_sec']=END/24;cues['frames']=END
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
run([sys.executable,OUT/'rebuild_fx.py'])
run(['ffmpeg','-v','error','-y','-i',OUT/'fx/receiver_light.mp4','-map','0:v:0','-c:v','copy','-an',OUT/'fx/clean.mp4'])
decisions=json.loads(paths[2].read_text())
entry=next(e for e in decisions['decisions'] if e['shot_id']=='s010')
entry.update(delivery_file='out/receiver_retimed_review/fx/clean.mp4',delivery_status='delivery_ready')
entry['timing_snapshot']={'fps':24,'song_start_frame':805,'song_end_frame_exclusive':856,'source_in_frame':0,'source_out_frame_exclusive':51}
(OUT/'receiver_decision.json').write_text(json.dumps({'s010':entry},indent=2))
with (OUT/'render.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--',
         '--proxy','--start',START,'--end',END-1,'--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
 f'[0:v]setpts=PTS-STARTPTS[v];[1:a]atrim=start={START/24:.12f}:end={END/24:.12f},asetpts=PTS-STARTPTS[a]',
 '-map','[v]','-map','[a]','-frames:v',END-START,'-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
assert all(sha(Path(p))==h for p,h in before.items())
print('Receiver rebuilt from stem at805..856; review719..911 complete. Production unchanged.')
