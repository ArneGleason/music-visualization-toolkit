"""Receiver settles into screen imagery, then garden; no new generated footage."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
p=ROOT/'out/receiver_now_v3/render.py'
wrapper=p.read_text().split("exec(compile(code,str(p),'exec')")[0]
ns={'__file__':str(p)}
exec(compile(wrapper,str(p),'exec'),ns)
code=ns['code'].split("edl=json.loads")[0]
code=code.replace('receiver_now_v3','screen_garden_trial')
code=code.replace('range(1,131)','range(1,188)').replace('assert len(records)==119','assert len(records)==176')
code=code.replace('1201/24, .001','1258/24, .001')
code=code.replace("'song_frames':[1082,1201]", "'song_frames':[1082,1258]")
needle='records=[]\nfor f in range(1,188):'
fx=(OUT/'screen.py').read_text()
assert needle in code
code=code.replace(needle,fx+'\n'+needle)
code=code.replace(" cv2.imwrite(str(outframes/f'{f-12:04d}.png'),np.rint(result*255).astype(np.uint8))",
 " result=screen_transition(result,songframe,matrix)\n cv2.imwrite(str(outframes/f'{f-12:04d}.png'),np.rint(result*255).astype(np.uint8))")
# Existing optical effect settles as attention moves to the screen.
code=code.replace('  result+=np.clip(lit+glow,0,1)*.5',
 '  glow*=1-ns[\'smooth\']((songframe-1201)/24)\n  result+=np.clip(lit+glow,0,1)*.5')
# Finish image sequence before encoding, preserving source time, no frozen frames.
code=code.replace('cap.release()\nassert len(records)==176', '''cap.release()
for sf in range(1258,1304):
 frame=texture(sf)
 cv2.imwrite(str(outframes/f'{sf-1082:04d}.png'),np.rint(frame*255).astype(np.uint8))
garden=cv2.VideoCapture(str(ROOT/'clips/raw/forest_threshold_v6.mp4'))
for sf in range(1304,1412):
 ok,frame=garden.read();assert ok
 cv2.imwrite(str(outframes/f'{sf-1082:04d}.png'),frame)
garden.release()
assert len(records)==176''')
exec(compile(code,str(p),'exec'),{'__file__':str(p),'__name__':'screen_pass'})

import json
import subprocess
def run(args,**kw):subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
edl=json.loads((ROOT/'out/receiver_now_v3/shotlist.json').read_text())
cues=json.loads((ROOT/'out/receiver_now_v3/overlay_cues.json').read_text())
for ident,setup,start,end in [('screen_reply','receiver_dial_macro',1201,1304),('garden_entry','forest_threshold',1304,1412)]:
 shot=dict(edl['shots'][-1]);shot.update(id=ident,setup=setup,start_sec=start/24,end_sec=end/24,
   dur_sec=(end-start)/24,frames=end-start,clip={'file':'out/screen_garden_trial/clean.mp4','in_sec':(start-1082)/24,'speed':1})
 edl['shots'].append(shot)
 cue=dict(cues['shots'][-1]);cue.update(id=ident,setup=setup,start=start,end=end);cues['shots'].append(cue)
edl['duration_sec']=cues['duration_sec']=1412/24;cues['frames']=1412
(OUT/'shotlist.json').write_text(json.dumps(edl,indent=2));(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
with (OUT/'blender.log').open('w') as log:
 run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--',
 '--proxy','--start','1137','--end','1411','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
 '[0:v]setpts=N/(24*TB)[v];[1:a]atrim=start=47.375:end=58.833333333333,asetpts=PTS-STARTPTS[a]',
 '-map','[v]','-map','[a]','-frames:v','275','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
print('Screen to garden preview ready: song1137..1412,275frames.')
