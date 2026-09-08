"""Review new purposeful handling between accepted table and planetary reveal."""
import json,subprocess,copy,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
h=json.loads((ROOT/'out/specimen_discovery_v1/handoff.json').read_text())
base=ROOT/h['claude_result']['base']['file']
assert hashlib.sha256(base.read_bytes()).hexdigest().upper()==h['claude_result']['base']['sha256']
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=r_frame_rate,nb_frames','-of','json',str(base)]))['streams'][0]
assert info['r_frame_rate']=='24/1' and int(info['nb_frames'])>=118
edl=json.loads((ROOT/'out/next_exchange_timing_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/next_exchange_timing_v1/overlay_cues.json').read_text())
for shot in edl['shots']:
    if shot['id']=='garden_begin_bloom_audition':
        shot['clip']={'file':'out/garden_bloom_synced_v5/clean.mp4','in_sec':0,'speed':1}
    if shot['id']=='exchange_listener_audition':
        shot['clip']={'file':'out/specimen_discovery_v1/base.mp4','in_sec':.5,'speed':1}
        shot['description']='New listening discovery: tilt/regrip, stop and study, then look up. No added glimmer yet.'
planet=json.loads((ROOT/'out/world_nebula_v3/shotlist.json').read_text())['shots'][-1]
planetcue=json.loads((ROOT/'out/world_nebula_v3/overlay_cues.json').read_text())['shots'][-1]
edl['shots'].append(copy.deepcopy(planet));cues['shots'].append(copy.deepcopy(planetcue))
edl['duration_sec']=cues['duration_sec']=2199/24;cues['frames']=2199
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','1973','--end','2198','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start={1973/24}:end={2199/24},asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','226','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'recipe.json').write_text(json.dumps({'status':'new_specimen_owner_review_pending','preview_song_frames':[1973,2199],'frames':226,'new_take_song_frames':[2016,2122],'new_take_source_frames':[12,118],'source_origin':2004,'source_sha256':h['claude_result']['base']['sha256'],'source_fps':24,'audio':'master only','glimmer_added':False,'cautions':'Two handling actions and open-mouth amazement, then purposeful steady hold and smile. No retiming; judge in context.','production_merged':False},indent=2))
print('Discovery context preview ready:226frames.')
