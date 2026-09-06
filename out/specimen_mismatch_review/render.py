"""Short same-clock review of accepted pieces edits plus new specimen take."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
START,END=500,719
def run(args,**kw):
    subprocess.run([str(a) for a in args],cwd=ROOT,check=True,**kw)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()
tracked=[ROOT/'shots/shotlist.json',ROOT/'generated/overlay_cues.json']
before={str(p):sha(p) for p in tracked}
hpath=ROOT/'out/specimen_mismatch_v2/handoff.json'
h=json.loads(hpath.read_text())
assert sha(ROOT/h['claude_result']['base']['file'])==h['claude_result']['base']['sha256']
edl=json.loads((ROOT/'out/pieces_cutaway_review/shotlist.json').read_text())
cues=json.loads((ROOT/'out/pieces_cutaway_review/overlay_cues.json').read_text())
shot=copy.deepcopy(next(s for s in edl['shots'] if s['id']=='s004'))
shot.update(id='specimen_mismatch',start_sec=670/24,end_sec=719/24,dur_sec=49/24,frames=49,
            lyric="Then they don't quite match.")
shot['clip']={'file':'out/specimen_mismatch_v2/base.mp4','in_sec':54/24,'speed':1}
edl['shots'].append(shot)
cue=copy.deepcopy(next(s for s in cues['shots'] if s['id']=='s004'))
cue.update(id='specimen_mismatch',start=670,end=719)
cues['shots'].append(cue)
edl['duration_sec']=cues['duration_sec']=END/24
cues['frames']=END
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
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,nb_frames,duration,width,height','-of','json',str(OUT/'preview.mp4')]))
v=next(s for s in probe['streams'] if s['codec_type']=='video')
assert int(v['nb_frames'])==219
assert all(sha(Path(p))==v for p,v in before.items())
h['status']='codex_verified_ready_for_owner_review'
h['codex_result']={'preview':'out/specimen_mismatch_review/preview.mp4','song_frames':[500,719],
  'selected_source_frames':[54,103],'editorial_source_origin_song_frame':616,
  'source_hash_verified':True,'production_unchanged':True,'owner_approval':'pending'}
hpath.write_text(json.dumps(h,indent=2)+'\n')
(OUT/'verification.json').write_text(json.dumps(probe,indent=2))
print('219-frame review ready; production unchanged.')
