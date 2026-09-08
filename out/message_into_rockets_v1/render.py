"""Review latest message ending into the two existing rocket setups."""
import copy,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(a,**kw):subprocess.run([str(x) for x in a],cwd=ROOT,check=True,**kw)
edl=json.loads((ROOT/'out/meaning_exchange_dual_sync_v6/shotlist.json').read_text())
cues=json.loads((ROOT/'out/meaning_exchange_dual_sync_v6/overlay_cues.json').read_text())
prod=json.loads((ROOT/'shots/shotlist.json').read_text())
for ident,start,end in [('s035',2881,2928),('s036',2928,2958),('s037',2958,3027)]:
    s=copy.deepcopy(next(s for s in prod['shots'] if s['id']==ident))
    s.update(start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start)
    edl['shots'].append(s)
    cues['shots'].append({'id':ident,'setup':s['setup'],'section':s['section'],'start':start,'end':end,'lyric':s['lyric']})
edl['duration_sec']=cues['duration_sec']=3027/24;cues['frames']=3027
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]:
    (OUT/name).write_text(json.dumps(data,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"message_into_rockets_v1"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2786','--end','3026','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={2786/24}:end={3027/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','241','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,width,height','-of','json',str(OUT/'preview.mp4')]))
assert int(probe['streams'][0]['nb_frames'])==241
(OUT/'verification.json').write_text(json.dumps(probe,indent=2))
print('Message into two rocket setups ready:241frames.',flush=True)
