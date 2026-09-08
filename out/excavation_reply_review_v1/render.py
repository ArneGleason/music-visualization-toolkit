"""Contextual performance review only; no lip-sync or paid retry."""
import copy,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(a,**kw):subprocess.run([str(v) for v in a],cwd=ROOT,check=True,**kw)
h=json.loads((ROOT/'out/excavation_reply_v1/handoff.json').read_text())
source=ROOT/h['output']['base'];digest=hashlib.sha256(source.read_bytes()).hexdigest()
assert digest==h['claude_result']['base']['sha256']
assert source.read_bytes()==(ROOT/h['claude_result']['original']['file']).read_bytes()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,duration,width,height,start_time','-of','json',str(source)]))['streams'][0]
assert probe['r_frame_rate']=='24/1' and int(probe['nb_frames'])==192
run(['ffmpeg','-v','error','-i',source,'-f','null','-'])
edl=json.loads((ROOT/'out/archaeology_review_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/archaeology_review_v1/overlay_cues.json').read_text())
prod=json.loads((ROOT/'shots/shotlist.json').read_text())
s=copy.deepcopy(next(s for s in prod['shots'] if s['id']=='s031'))
s.update(id='excavation_reply_performance_review',start_sec=2564/24,end_sec=2658/24,dur_sec=94/24,frames=94,
 lyric='Especially stupid. Can you hear what I meant?',clip={'file':h['output']['base'],'in_sec':.5,'speed':1})
edl['shots'].append(s)
cues['shots'].append({'id':s['id'],'setup':s['setup'],'section':s['section'],'start':2564,'end':2658,'lyric':s['lyric']})
edl['duration_sec']=cues['duration_sec']=2658/24;cues['frames']=2658
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]:
 (OUT/name).write_text(json.dumps(data,indent=2))
with (OUT/'assembly.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2484','--end','2657','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start={2484/24}:end={2658/24},asetpts=PTS-STARTPTS[a]','-map','[v]','-map','[a]','-frames:v','174','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'verification.json').write_text(json.dumps({'status':'verified_candidate_with_performance_concerns','sha256':digest,'probe':probe,'preview_song_frames':[2484,2658],'reply_song_frames':[2564,2658],'source_frames':[12,106],'source_origin_frame':2552,'lip_sync_applied':False,'production_merged':False,'concerns':['broad wince and grin rather than small ironic gesture','long unarticulated grin before sincere question','generated singing timing not corrected']},indent=2))
print('Excavation and reply performance preview ready.')
