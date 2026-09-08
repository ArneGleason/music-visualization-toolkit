"""Pacing audition from mind-bend through the first outro exchange."""
from pathlib import Path
import copy,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_sources import load_decisions,resolve_clip,inspect_video
def run(args,**kw):subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
edl=json.loads((ROOT/'out/spring_geyser_review_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/spring_geyser_review_v1/overlay_cues.json').read_text())
production=json.loads((ROOT/'shots/shotlist.json').read_text())
globalcues=json.loads((ROOT/'generated/overlay_cues.json').read_text())
spec=[('s050','chorus_plunge_continuous',3897,4030,0),('s052','turn_phrase',4030,4073,24),('s053','follow_phrase',4073,4120,72),('o01','o01',4120,4177,None),('o02','o02',4177,4232,None),('o03','o03',4232,4262,None)]
decisions=load_decisions(ROOT);checks=[]
for oldid,ident,start,end,inframe in spec:
    s=copy.deepcopy(next(s for s in production['shots'] if s['id']==oldid))
    s.update(id=ident,start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start)
    if inframe is not None:s['clip']['in_sec']=inframe/24
    if ident=='chorus_plunge_continuous':s['lyric']='No one has ever been / In / in the rivers of Mars.'
    if ident=='follow_phrase':s['lyric']='Then follows. / Then answers.'
    cue=copy.deepcopy(next(c for c in globalcues['shots'] if c['id']==oldid))
    cue.update(id=ident,start=start,end=end)
    clip=resolve_clip(ROOT,s,24,decisions,start,end)
    fps,count=inspect_video(ROOT/clip['file']);assert fps==24,(ident,fps)
    first=round(clip.get('in_sec',0)*24);assert first+end-start<=count,(ident,first,count)
    checks.append({'shot':ident,'song_frames':[start,end],'source':clip['file'],'source_frames':[first,first+end-start],'available_frames':count})
    edl['shots'].append(s);cues['shots'].append(cue)
ordered=[s for s in edl['shots'] if 3505<=round(s['start_sec']*24)<4262]
for a,b in zip(ordered,ordered[1:]):assert round(a['end_sec']*24)==round(b['start_sec']*24),(a['id'],b['id'])
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]: (OUT/name).write_text(json.dumps(data,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"swimming_to_outro_review_v1"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'render.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','3505','--end','4261','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={3505/24}:end={4262/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','757','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
assert inspect_video(OUT/'preview.mp4')==(24.,757)
(OUT/'verification.json').write_text(json.dumps({'preview_song_frames':[3505,4262],'frames':757,'new_source_coverage':checks,'unchanged_approved_through':3897,'speed':1,'status':'new continuation pacing review pending'},indent=2))
