"""Owner-requested audition of quality-gated new landing, without new generation."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(a,**kw):subprocess.run([str(x) for x in a],cwd=ROOT,check=True,**kw)
base=ROOT/'out/rocket_landing_retry_v1/base.mp4'
assert hashlib.sha256(base.read_bytes()).hexdigest()=='653071bad0731275f5f21a681c544e8bbff742d52ae1f145ab2b29b49c468d81'
run(['ffmpeg','-v','error','-i',base,'-f','null','-'])
# Reapply the approved pressure lens to new source42..111 at song2958..3027.
tool=ROOT/'tools/pressure_lens_pilot.py';code=tool.read_text()
line="    shot=next(s for s in json.loads((ROOT/'shots/shotlist.json').read_text())['shots'] if s['id']=='s037')"
assert line in code
code=code.replace(line,line+"\n    shot['clip']={'file':'out/rocket_landing_retry_v1/base.mp4','in_sec':42/24,'speed':1}")
code=code.replace("OUT=ROOT/'out/pressure_lens_rockets_exaggerated'","OUT=ROOT/'out/message_into_rockets_v2/fx'")
(OUT/'fx_wrapper.py').write_text("from pathlib import Path\np=Path("+repr(str(tool))+")\ns="+repr(code)+"\nexec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})\n")
with (OUT/'fx.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'fx_wrapper.py','--','--exaggerated'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'fx/pressure_lens.mp4','-map','0:v','-c:v','copy','-an',OUT/'fx/clean.mp4'])
edl=json.loads((ROOT/'out/message_into_rockets_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/message_into_rockets_v1/overlay_cues.json').read_text())
for s in edl['shots']:
    if s['id'] in ['s036','s037']:
        old=s['id'];s['id']='landing_retry_'+old
        s['clip']=({'file':'out/rocket_landing_retry_v1/base.mp4','in_sec':.5,'speed':1} if old=='s036' else {'file':'out/message_into_rockets_v2/fx/clean.mp4','in_sec':0,'speed':1})
        next(c for c in cues['shots'] if c['id']==old)['id']=s['id']
for name,d in [('shotlist.json',edl),('overlay_cues.json',cues)]: (OUT/name).write_text(json.dumps(d,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"message_into_rockets_v2"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2786','--end','3026','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={2786/24}:end={3027/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','241','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
(OUT/'verification.json').write_text(json.dumps({'hash_verified':True,'preview_song_frames':[2786,3027],'landing_source_frames':[12,111],'source_origin':2916,'kling_done':False,'fx_reapplied_song_frames':[2958,3027],'status':'owner audition pending; no production changes'},indent=2))
print('New landing in same preview ready; no Kling yet.',flush=True)
