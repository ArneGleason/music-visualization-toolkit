"""Isolated preview: retain singer clock, cover missed 'pieces' with prop insert."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_timebase import conform_clip

def run(args, **kw):
    return subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

tracked=[ROOT/'shots/shotlist.json',ROOT/'generated/overlay_cues.json']
before={str(p):sha(p) for p in tracked}
h=json.loads((ROOT/'out/pieces_performance_v1/handoff.json').read_text())
for key in ('base','synced'):
    item=h['claude_result'][key]
    assert sha(ROOT/item['file'])==item['sha256']
def audio(p):
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ac','1','-ar','48000','-f','s16le','-'])
    return np.frombuffer(data,dtype='<i2').astype(float)
a=audio(ROOT/'out/pieces_performance_v1/guide.wav')
b=audio(ROOT/'out/pieces_performance_v1/synced.mp4')
n=min(len(a),len(b))
corr=float(np.corrcoef(a[:n],b[:n])[0,1])
assert corr>.99,corr
# Different spare take, tightly framed on the hands. Source24..72 stays before
# the known unwanted viewpoint morph around86. No reused frames from v2.
run(['ffmpeg','-v','error','-y','-i',ROOT/'clips/raw/canal_map_macro_v6.mp4',
     '-vf','trim=start_frame=24:end_frame=72,setpts=PTS-STARTPTS,crop=960:540:160:180,scale=1280:720',
     '-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',OUT/'insert.mp4'])
edl=json.loads((ROOT/'out/opening_phrase_cut/shotlist.json').read_text())
cues=json.loads((ROOT/'out/opening_phrase_cut/overlay_cues.json').read_text())
original=json.loads(tracked[0].read_text())
original_cues=json.loads(tracked[1].read_text())
face=next(s for s in original['shots'] if s['id']=='s005')
facecue=next(s for s in original_cues['shots'] if s['id']=='s005')
prop=copy.deepcopy(edl['shots'][-1])
propcue=copy.deepcopy(cues['shots'][-1])
edl['shots'][-1].update(end_sec=500/24,dur_sec=(500-334)/24,frames=166)
cues['shots'][-1]['end']=500
specs=[('pieces_face_in',500,562,face,facecue,'out/pieces_performance_v1/synced.mp4',12),
       ('pieces_insert',562,610,prop,propcue,'out/pieces_cutaway_review/insert.mp4',0),
       ('pieces_face_return',610,670,face,facecue,'out/pieces_performance_v1/synced.mp4',122)]
for sid,start,end,template,ct,file,source_in in specs:
    shot=copy.deepcopy(template)
    shot.update(id=sid,start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start)
    shot['clip']=conform_clip(ROOT,{'file':file,'in_sec':source_in/24,'speed':1},24,prepare=True)
    edl['shots'].append(shot)
    cue=copy.deepcopy(ct)
    cue.update(id=sid,start=start,end=end)
    cues['shots'].append(cue)
edl['duration_sec']=cues['duration_sec']=670/24
cues['frames']=670
for left,right in zip(edl['shots'],edl['shots'][1:]):
    assert round(left['end_sec']*24)==round(right['start_sec']*24)
assert 610-488==122
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'render.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1',
         '-P',OUT/'blender_review.py','--','--proxy','--start','0','--end','669',
         '--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
     '[0:v]setpts=PTS-STARTPTS[v];[1:a]atrim=start=0:end=27.916666666667,asetpts=PTS-STARTPTS[a]',
     '-map','[v]','-map','[a]','-frames:v','670','-c:v','libx264','-preset','fast','-crf','17',
     '-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-y','-i',OUT/'preview.mp4','-ss',str(500/24),'-t',str(170/24),
     '-c:v','libx264','-crf','17','-c:a','aac','-movflags','+faststart',OUT/'detail.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
assert all(sha(Path(p))==v for p,v in before.items())
(OUT/'verification.json').write_text(json.dumps({'zero_lag_guide_correlation':corr,
    'source_hashes_verified':True,'production_unchanged':True,'frames':670,
    'insert_song_frames':[562,610],'insert_original_source_frames':[24,72],
    'singer_source_origin':488,'singer_return_source_frame':122},indent=2))
print('Preview ready, no production modifications. Guide correlation:',corr)
