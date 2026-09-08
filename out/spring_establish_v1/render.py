"""Audition a scenic spring insert using distinct passages of existing footage."""
import copy
import json
import subprocess
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
def run(args,**kw):
    subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=r_frame_rate,nb_frames,width,height','-of','json',str(path)]))['streams'][0]
spring=ROOT/'clips/raw/rain_to_canal_v6.mp4'
p=probe(spring)
assert p['r_frame_rate']=='24/1' and int(p['nb_frames'])>=177
run(['ffmpeg','-v','error','-i',spring,'-f','null','-'])
edl=json.loads((ROOT/'out/message_into_rockets_v4/shotlist.json').read_text())
cues=json.loads((ROOT/'out/message_into_rockets_v4/overlay_cues.json').read_text())
prod=json.loads((ROOT/'shots/shotlist.json').read_text())
def add(template,ident,start,end,file,src,lyric,description):
    s=copy.deepcopy(template)
    s.update(id=ident,start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start,lyric=lyric,description=description,clip={'file':file,'in_sec':src/24,'speed':1},transition={'type':'cut','dur_sec':0})
    edl['shots'].append(s)
    cues['shots'].append({'id':ident,'setup':s['setup'],'section':s['section'],'start':start,'end':end,'lyric':lyric})
landing=next(s for s in edl['shots'] if s['id']=='landing_retry_s036')
add(landing,'landing_tail_s038',3027,3100,'out/message_into_rockets_v3/conformed.mp4',111,"Can't tell you / if they're",'Continuous returned lip-sync tail; ends before true')
sp=next(s for s in prod['shots'] if s['id']=='s040')
add(sp,'spring_wide_insert',3100,3165,'clips/raw/rain_to_canal_v6.mp4',112,'true.','Scenic waterway introduction, editorial insert from later source passage')
add(sp,'spring_close_s040',3165,3229,'clips/raw/rain_to_canal_v6.mp4',0,'Elsewhere, under a smaller moon','Closer spring reveal on Elsewhere; distinct early source passage')
edl['duration_sec']=cues['duration_sec']=3229/24
cues['frames']=3229
for name,value in [('shotlist.json',edl),('overlay_cues.json',cues)]:
    (OUT/name).write_text(json.dumps(value,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"spring_establish_v1"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2928','--end','3228','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={2928/24}:end={3229/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','301','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
q=probe(OUT/'preview.mp4')
assert int(q['nb_frames'])==301 and q['r_frame_rate']=='24/1'
(OUT/'verification.json').write_text(json.dumps({'preview':q,'source':p,'source_sha256':hashlib.sha256(spring.read_bytes()).hexdigest(),'song_frames':[2928,3229],'landing_tail_source_frames':[111,184],'wide_source_frames':[112,177],'wide_song_frames':[3100,3165],'close_source_frames':[0,64],'close_song_frames':[3165,3229],'speed':1,'status':'owner review pending; no generation or production merge'},indent=2))
print('Preview ready: 301 frames, 24 fps.',flush=True)
