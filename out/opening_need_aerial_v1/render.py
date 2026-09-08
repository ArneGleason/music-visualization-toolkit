"""Short aerial still-motion timing test over need, preserving face source clock."""
import copy,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_sources import inspect_video
def run(args,**kw):subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
lock=(ROOT/'out/astronaut_reply_v1/style_lock_v2.txt').read_bytes()
(OUT/'image_prompt.txt').write_bytes((OUT/'image_direction.txt').read_bytes().rstrip()+b'\n\n'+lock)
run(['ffmpeg','-v','error','-y','-i',OUT/'first_frame.png','-vf',"scale=3344:1882,zoompan=z=1.08:x='(iw-iw/zoom)*(0.1+0.8*on/41)':y='(ih-ih/zoom)*0.5':d=42:s=1280x720:fps=24",'-frames:v','42','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'clean.mp4'])
edl=json.loads((ROOT/'out/full_review_20260907/shotlist.json').read_text())
cues=json.loads((ROOT/'out/full_review_20260907/overlay_cues.json').read_text())
original=next(s for s in edl['shots'] if round(s['start_sec']*24)==155)
assert round(original['end_sec']*24)==334
oldcue=next(c for c in cues['shots'] if c['id']==original['id'])
shots=[];newcues=[]
for ident,start,end in [('opening_before_need',155,183),('opening_need_landscape',183,225),('opening_after_need',225,334)]:
    s=copy.deepcopy(original);s.update(id=ident,start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start)
    if start==183:
        s['clip']={'file':'out/opening_need_aerial_v1/clean.mp4','in_sec':0,'speed':1}
        s['description']='High river-region aerial preview, simulated lateral move over new reference still'
    else:s['clip']['in_sec']=original['clip']['in_sec']+(start-155)/24
    shots.append(s);c=copy.deepcopy(oldcue);c.update(id=ident,start=start,end=end);newcues.append(c)
i=edl['shots'].index(original);edl['shots'][i:i+1]=shots
i=cues['shots'].index(oldcue);cues['shots'][i:i+1]=newcues
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]: (OUT/name).write_text(json.dumps(data,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"opening_need_aerial_v1"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','155','--end','333','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={155/24}:end={334/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','179','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
assert inspect_video(str(OUT/'preview.mp4'))==(24.,179)
(OUT/'verification.json').write_text(json.dumps({'preview_song_frames':[155,334],'insert_song_frames':[183,225],'insert_frames':42,'duration_seconds':1.75,'face_source_clock_preserved':True,'motion':'2D lateral motion over built-in generated aerial still, not Flow footage','status':'owner timing/image review pending'},indent=2))
print('Opening aerial cutaway preview ready.',flush=True)
