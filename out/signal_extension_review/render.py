"""Extend the short accepted review through the signal phrase, no paid work."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
START,END=500,805
def run(args,**kw):
    subprocess.run([str(a) for a in args],cwd=ROOT,check=True,**kw)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
tracked=[ROOT/'shots/shotlist.json',ROOT/'generated/overlay_cues.json',ROOT/'shots/assembly_decisions.json']
before={str(p):sha(p) for p in tracked}
edl=json.loads((ROOT/'out/specimen_mismatch_review/shotlist.json').read_text())
cues=json.loads((ROOT/'out/specimen_mismatch_review/overlay_cues.json').read_text())
original=json.loads(tracked[0].read_text())
oc=json.loads(tracked[1].read_text())
shot=copy.deepcopy(next(s for s in original['shots'] if s['id']=='s009'))
shot.update(start_sec=719/24,end_sec=805/24,dur_sec=86/24,frames=86)
shot['clip']={'file':'clips/raw/signal_crossing_space_v6.mp4','in_sec':0,'speed':1}
edl['shots'].append(shot)
cue=copy.deepcopy(next(s for s in oc['shots'] if s['id']=='s009'))
cue.update(start=719,end=805)
cues['shots'].append(cue)
edl['duration_sec']=cues['duration_sec']=END/24
cues['frames']=END
for a,b in zip(edl['shots'],edl['shots'][1:]):
    assert round(a['end_sec']*24)==round(b['start_sec']*24)
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'render.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1',
         '-P',OUT/'blender_review.py','--','--proxy','--start',START,'--end',END-1,
         '--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],
         stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
     f'[0:v]setpts=PTS-STARTPTS[v];[1:a]atrim=start={START/24:.12f}:end={END/24:.12f},asetpts=PTS-STARTPTS[a]',
     '-map','[v]','-map','[a]','-frames:v',END-START,'-c:v','libx264','-preset','fast',
     '-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
    'stream=codec_type,nb_frames,duration,width,height','-of','json',str(OUT/'preview.mp4')]))
assert int(next(s for s in probe['streams'] if s['codec_type']=='video')['nb_frames'])==305
assert all(sha(Path(p))==v for p,v in before.items())
(OUT/'verification.json').write_text(json.dumps({'probe':probe,'production_unchanged':True,
    'song_frames':[500,805],'signal_source_frames':[0,86],
    'signal_source_sha256':sha(ROOT/'clips/raw/signal_crossing_space_v6.mp4')},indent=2))
print('305-frame short preview complete; stopped before receiver FX requiring rebuild.')
