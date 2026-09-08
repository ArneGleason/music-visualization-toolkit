"""Short face entrance, early overhead cutaway, freshly timed accepted FX."""
import copy,hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_sources import inspect_video
def run(args,**kw): subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
h=json.loads((ROOT/'out/swimmer_shore_lipsync_v1/handoff.json').read_text())
for ref in [*h['inputs'].values(),h['claude_result']['synced'],h['claude_result']['original']]:
    assert hashlib.sha256((ROOT/ref['file']).read_bytes()).hexdigest()==ref['sha256']
source=ROOT/h['claude_result']['synced']['file']
def samples(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
a,b=samples(source),samples(ROOT/h['inputs']['guide']['file']);n=min(len(a),len(b))
corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.98
run(['ffmpeg','-v','error','-y','-i',source,'-vf','setpts=PTS-STARTPTS,fps=24','-an','-c:v','libx264','-crf','16',OUT/'synced_24.mp4'])
edl=json.loads((ROOT/'out/spring_into_swimmers_v1/shotlist.json').read_text())
cues=json.loads((ROOT/'out/spring_into_swimmers_v1/overlay_cues.json').read_text())
face=next(s for s in edl['shots'] if s['id']=='s042')
face.update(end_sec=3322/24,dur_sec=20/24,frames=20)
face['clip']={'file':'out/swimmer_cutaway_v2/synced_24.mp4','in_sec':2.84,'speed':1}
next(c for c in cues['shots'] if c['id']=='s042')['end']=3322
over=next(s for s in edl['shots'] if s['id']=='s043')
over.update(start_sec=3322/24,dur_sec=116/24,frames=116)
over['clip']={'file':'clips/raw/basin_kaleidoscope_top_v6.mp4','in_sec':0,'speed':1}
cue=next(c for c in cues['shots'] if c['id']=='s043');cue['start']=3322
# Render the original approved algorithm against the extended source and new song time.
(OUT/'fx_shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT/'overlay_cues.json').write_text(json.dumps(cues,indent=2))
tool=ROOT/'tools/swimmer_palette_pilot.py';code=tool.read_text()
code=code.replace("ROOT/'shots/shotlist.json'","ROOT/'out/swimmer_cutaway_v2/fx_shotlist.json'")
code=code.replace("ROOT/'generated/overlay_cues.json'","ROOT/'out/swimmer_cutaway_v2/overlay_cues.json'")
code=code.replace("ROOT/'out/swimmer_fx_full'/SHOT","ROOT/'out/swimmer_cutaway_v2/fx'/SHOT")
(OUT/'fx_wrapper.py').write_text("import sys\nsys.path.insert(0,"+repr(str(ROOT/'tools'))+")\nexec(compile("+repr(code)+","+repr(str(tool)) +",'exec'),{'__name__':'__main__','__file__':"+repr(str(tool))+"})\n")
with (OUT/'fx.log').open('w') as log:
    run(['python',OUT/'fx_wrapper.py','--shot','s043','--full'],stdout=log,stderr=subprocess.STDOUT)
assert inspect_video(str(OUT/'fx/s043/clean.mp4'))==(24.0,116)
# Explicit new-timing delivery; old s043 protection remains intact for old edit.
over['id']='swimming_overhead_early'
over['clip']={'file':'out/swimmer_cutaway_v2/fx/s043/clean.mp4','in_sec':0,'speed':1}
cue['id']=over['id']
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]: (OUT/name).write_text(json.dumps(data,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"swimmer_cutaway_v2"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','3165','--end','3504','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={3165/24}:end={3505/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','340','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
assert inspect_video(str(OUT/'preview.mp4'))==(24.0,340)
(OUT/'verification.json').write_text(json.dumps({'hashes_verified':True,'guide_zero_lag_correlation':corr,'preview_song_frames':[3165,3505],'face_song_frames':[3302,3322],'overhead_song_frames':[3322,3438],'overhead_source_frames':[0,116],'fx_recomputed':True,'s044_unchanged':True,'status':'owner review pending'},indent=2))
print('Cutaway preview ready.',flush=True)
