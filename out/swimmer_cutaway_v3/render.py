"""Owner-adjusted face window: just before go through in the."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_sources import inspect_video
def run(args,**kw):subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
previous=ROOT/'out/swimmer_cutaway_v2'
edl=json.loads((previous/'shotlist.json').read_text())
cues=json.loads((previous/'overlay_cues.json').read_text())
def change(ident,start,end,in_sec=None):
    s=next(s for s in edl['shots'] if s['id']==ident)
    s.update(start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start)
    if in_sec is not None:s['clip']['in_sec']=in_sec
    c=next(c for c in cues['shots'] if c['id']==ident);c.update(start=start,end=end)
    return s
change('s041',3229,3300)
face=change('s042',3300,3400,2.84-2/24)
change('swimming_overhead_early',3400,3438,78/24)
assert round(face['clip']['in_sec']*24)+100 <= inspect_video(str(ROOT/face['clip']['file']))[1]
# Existing FX source0 corresponds to song3322: source78 still corresponds to3400.
assert 3322+78==3400
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]: (OUT/name).write_text(json.dumps(data,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"swimmer_cutaway_v3"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','3165','--end','3504','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={3165/24}:end={3505/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','340','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
assert inspect_video(str(OUT/'preview.mp4'))==(24.0,340)
(OUT/'verification.json').write_text(json.dumps({'preview_song_frames':[3165,3505],'face_song_frames':[3300,3400],'face_source_in_seconds':face['clip']['in_sec'],'source_origin_seconds':3300/24-face['clip']['in_sec'],'overhead_song_frames':[3400,3438],'overhead_fx_source_frames':[78,116],'effects_song_alignment_preserved':True,'status':'owner review pending'},indent=2))
print('Revised preview ready.',flush=True)
