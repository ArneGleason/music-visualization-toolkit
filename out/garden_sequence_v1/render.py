"""Approved moth/eyes, new walk return, approved strong bird FX in context."""
import json,hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
OUT.mkdir(exist_ok=True)
edl=json.loads((ROOT/'out/garden_waking_v3/shotlist.json').read_text())
cues=json.loads((ROOT/'out/garden_waking_v3/overlay_cues.json').read_text())
h=json.loads((ROOT/'out/garden_walk_return_v1/handoff.json').read_text())
assert hashlib.sha256((ROOT/h['output']['base']).read_bytes()).hexdigest().upper()==h['claude_result']['base']['sha256']
bird=json.loads((ROOT/'out/garden_birds_fx_v2/shotlist.json').read_text())['shots'][0]
walk=dict(bird)
walk.update(id='garden_walk_return_review',setup='forest_walk_track',start_sec=1650/24,end_sec=1710/24,dur_sec=60/24,frames=60,
 lyric='in the psychedelic garden',description='Continue screen-right through the garden; later lantern approach preserved for possible return.',
 prompt='',still='Later garden walk, same woman and lantern.',clip={'file':h['output']['base'],'in_sec':12/24,'speed':1})
edl['shots'].extend([walk,bird])
for shot,start,end in [(walk,1650,1710),(bird,1710,1786)]:
 cues['shots'].append({'id':shot['id'],'setup':shot['setup'],'section':'scene-04','start':start,'end':end,'lyric':shot['lyric']})
edl['duration_sec']=cues['duration_sec']=1786/24;cues['frames']=1786
# Correct inherited descriptive boilerplate in this new snapshot only.
for shot in edl['shots']:
 if shot['setup']=='forest_fauna_moth':
  shot.update(lyric='through the psychedelic garden',description='Spectral ghost wings around the garden moth',prompt='',still='Garden moth')
 if shot['setup']=='forest_fauna_eyes':
  shot.update(lyric='Something with no name is waking',description='Staggered eye openings, three-depth airflow and leaf phosphor',prompt='',still='Dark waking fauna')
 if shot['setup'] in ('forest_fauna_moth','forest_fauna_eyes'):shot.pop('start_barbeat',None)
by_id={s['id']:s for s in edl['shots']}
for cue in cues['shots']:
 if cue['id'] in by_id:cue['lyric']=by_id[cue['id']]['lyric']
part=[s for s in edl['shots'] if s['start_sec']>=1514/24]
assert sum(s['frames'] for s in part)==272
for a,b in zip(part,part[1:]):assert round(a['end_sec']*24)==round(b['start_sec']*24)
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)
with (OUT/'assembly.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','1514','--end','1785','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex','[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start=63.083333333333:end=74.416666666667,asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','272','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'review.json').write_text(json.dumps({'status':'owner_review_pending','song_frames':[1514,1786],'fps':24,'frames':272,'walk_song_frames':[1650,1710],'walk_source_frames':[12,72],'walk_source_origin':1638,'master_audio_once':True,'source_audio_used':False,'retiming':False,'new_walk_fx':False,'later_walk_policy':'Retain full192frames. Return must advance its source clock; no restart. With origin1638 the source ends at song1830; do not silently extend to1841. Later lantern approach not inserted yet.','full_film_updated':False},indent=2))
print('Rendered272frames: moth, waking eyes, walk return, strong bird FX.')
