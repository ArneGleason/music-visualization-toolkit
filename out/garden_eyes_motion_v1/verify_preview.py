import hashlib
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'out/garden_eyes_motion_review'
OUT.mkdir(exist_ok=True)
hp=ROOT/'out/garden_eyes_motion_v1/handoff.json';h=json.loads(hp.read_text())
base=ROOT/h['output']['base']
assert hashlib.sha256(base.read_bytes()).hexdigest().upper()==h['claude_result']['base']['sha256']
edl=json.loads((ROOT/'out/garden_ghost_wings_v3/shotlist.json').read_text())
cues=json.loads((ROOT/'out/garden_ghost_wings_v3/overlay_cues.json').read_text())
shot=dict(edl['shots'][-1]);shot.update(id='garden_eyes_motion_audition',setup='forest_fauna_eyes',start_sec=1569/24,end_sec=1650/24,
 dur_sec=81/24,frames=81,clip={'file':h['output']['base'],'in_sec':0,'speed':1})
edl['shots'].append(shot);cue=dict(cues['shots'][-1]);cue.update(id=shot['id'],setup=shot['setup'],start=1569,end=1650);cues['shots'].append(cue)
edl['duration_sec']=cues['duration_sec']=1650/24;cues['frames']=1650
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
def run(args,**kw):subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
with (OUT/'blender.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',ROOT/'out/garden_eyes_motion_v1/blender_review.py',
 '--','--proxy','--start','1514','--end','1649','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
 '[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start=63.083333333333:end=68.75,asetpts=PTS-STARTPTS[a]',
 '-map','[v]','-map','[a]','-frames:v','136','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
h['status']='codex_verified_ready_for_owner_review'
h['codex_result']={'hash_verified':True,'preview':'out/garden_eyes_motion_review/preview.mp4',
 'source_frames':[0,81],'song_frames':[1569,1650],'revised_visual_source_origin':1569,
 'lead_handle_frames':0,'reason':'No lip sync; earlier visual in-point avoids late amber exit without shortening lyric or retiming video.',
 'fx_status':'Base-motion audition only, particles not yet rebuilt; protected static production selection unchanged.',
 'handles':'At most one extra frame before reported clean cutoff82; later footage unsuitable. Do not claim requested99 clean exit frames.',
 'owner_approval':'pending'}
hp.write_text(json.dumps(h,indent=2)+'\n');print('Verified base-motion audition,136frames.')
