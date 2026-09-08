"""Eleven-frame artifact insert, preserving vocal and preceding face timing."""
import copy,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)
run(['ffmpeg','-v','error','-y','-i',ROOT/'out/archaeology_discovery_v1/base.mp4',
 '-vf','trim=start_frame=120:end_frame=131,setpts=PTS-STARTPTS,crop=640:360:320:290,scale=1280:720:flags=lanczos',
 '-frames:v','11','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'insert.mp4'])
edl=json.loads((ROOT/'out/excavation_reply_synced_v2/shotlist.json').read_text())
cues=json.loads((ROOT/'out/excavation_reply_synced_v2/overlay_cues.json').read_text())
face=edl['shots'][-1]
face.update(end_sec=2647/24,dur_sec=83/24,frames=83)
cues['shots'][-1]['end']=2647
shot=copy.deepcopy(edl['shots'][-2])
shot.update(id='meant_artifact_insert',start_sec=2647/24,end_sec=2658/24,dur_sec=11/24,frames=11,
 lyric='meant?',clip={'file':'out/meant_cutaway_v1/insert.mp4','in_sec':0,'speed':1})
edl['shots'].append(shot)
cues['shots'].append({'id':shot['id'],'setup':shot['setup'],'section':shot['section'],'start':2647,'end':2658,'lyric':'meant?'})
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]:
 (OUT/name).write_text(json.dumps(data,indent=2))
p=ROOT/'out/excavation_reply_review_v1/render.py'
tail=p.read_text().split("with (OUT/'assembly.log').open('w') as log:",1)[1].split("(OUT/'verification.json').write_text",1)[0]
exec(compile("with (OUT/'assembly.log').open('w') as log:"+tail,str(p),'exec'),globals())
(OUT/'verification.json').write_text(json.dumps({'status':'owner_review_pending','preview_song_frames':[2484,2658],
 'insert_song_frames':[2647,2658],'original_insert_source_frames':[120,131],'crop_xywh':[320,290,640,360],
 'picture_only_change':True,'audio':'unchanged master, once','production_merged':False},indent=2))
print('Meant cutaway preview ready.')
