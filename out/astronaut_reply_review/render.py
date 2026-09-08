import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_timebase import conform_clip
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def run(a,**kw):subprocess.run([str(x) for x in a],cwd=ROOT,check=True,**kw)
hpath=ROOT/'out/astronaut_reply_v1/handoff.json';h=json.loads(hpath.read_text())
for k in ('base','synced'):
    item=h['claude_result'][k];assert sha(ROOT/item['file'])==item['sha256']
def pcm(p):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','12000','-f','s16le','-']),dtype='<i2').astype(float)
a=pcm(ROOT/h['inputs']['guide']['file']);b=pcm(ROOT/h['output']['synced'])
n=min(len(a),len(b));corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.99
lags={}
for lag in range(-600,601):
    lo=max(0,-lag);hi=min(len(a),len(b)-lag)
    lags[lag]=float(np.corrcoef(a[lo:hi],b[lo+lag:hi+lag])[0,1])
best=max(lags,key=lags.get);assert abs(best)<=24
tracked=[ROOT/'shots/shotlist.json',ROOT/'generated/overlay_cues.json',ROOT/'shots/assembly_decisions.json']
before={str(p):sha(p) for p in tracked}
edl=json.loads((ROOT/'out/probe_voice_trial/shotlist.json').read_text())
cues=json.loads((ROOT/'out/probe_voice_trial/overlay_cues.json').read_text())
original=json.loads(tracked[0].read_text());oc=json.loads(tracked[1].read_text())
s=copy.deepcopy(next(x for x in original['shots'] if x['id']=='s012'))
s.update(start_sec=911/24,end_sec=1030/24,dur_sec=119/24,frames=119)
s['clip']=conform_clip(ROOT,{'file':h['output']['synced'],'in_sec':.5,'speed':1},24,prepare=True)
edl['shots'].append(s)
c=copy.deepcopy(next(x for x in oc['shots'] if x['id']=='s012'));c.update(start=911,end=1030)
cues['shots'].append(c)
edl['duration_sec']=cues['duration_sec']=1030/24;cues['frames']=1030
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'render.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','856','--end','1029','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
 '[0:v]setpts=PTS-STARTPTS[v];[1:a]atrim=start=35.666666666667:end=42.916666666667,asetpts=PTS-STARTPTS[a]',
 '-map','[v]','-map','[a]','-frames:v','174','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
assert all(sha(Path(p))==v for p,v in before.items())
h['status']='codex_verified_ready_for_owner_review'
h['codex_result']={'preview':'out/astronaut_reply_review/preview.mp4','song_frames':[856,1030],
 'source_in_frame':12,'source_out_frame_exclusive':131,'song_source_origin':899,
 'zero_lag_correlation':corr,'best_lag_ms':best/12,'hashes_verified':True,'production_unchanged':True,
 'note':'Audio clock verified, not a guarantee of every mouth phoneme. Owner to review smiling performance and articulation.'}
hpath.write_text(json.dumps(h,indent=2)+'\n')
print(json.dumps(h['codex_result'],indent=2))
