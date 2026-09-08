"""Preview existing swimmer edit after the accepted spring transition."""
import copy,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_sources import load_decisions,resolve_clip,inspect_video
from assembly_timebase import conform_clip
def run(args,**kw):subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
edl=json.loads((ROOT/'out/spring_establish_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/spring_establish_v1/overlay_cues.json').read_text())
prod=json.loads((ROOT/'shots/shotlist.json').read_text())
decisions=load_decisions(ROOT);checks=[]
for ident,start,end in [('s041',3229,3302),('s042',3302,3370),('s043',3370,3438),('s044',3438,3505)]:
    s=copy.deepcopy(next(s for s in prod['shots'] if s['id']==ident))
    s.update(start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start)
    selected=resolve_clip(ROOT,s,24,decisions,start=start,end=end)
    conformed=conform_clip(ROOT,selected,24,prepare=True)
    rate,frames=inspect_video(str(ROOT/conformed['file']))
    assert round(conformed.get('in_sec',0)*24)+end-start<=frames
    checks.append({'shot':ident,'song_frames':[start,end],'selected':conformed,'source_frames':frames})
    edl['shots'].append(s)
    cues['shots'].append({'id':ident,'setup':s['setup'],'section':s['section'],'start':start,'end':end,'lyric':s['lyric']})
edl['duration_sec']=cues['duration_sec']=3505/24;cues['frames']=3505
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]: (OUT/name).write_text(json.dumps(data,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"spring_into_swimmers_v1"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','3100','--end','3504','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={3100/24}:end={3505/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','405','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
rate,frames=inspect_video(str(OUT/'preview.mp4'));assert rate==24 and frames==405
(OUT/'verification.json').write_text(json.dumps({'frames':frames,'fps':rate,'song_frames':[3100,3505],'source_checks':checks,'status':'existing edit audition; owner review pending'},indent=2))
print('Preview ready:405frames.',flush=True)
