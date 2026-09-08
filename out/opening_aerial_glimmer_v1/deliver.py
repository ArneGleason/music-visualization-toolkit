"""Render approved light layer into a silent, lyric-free assembly element."""
from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(args,**kw):subprocess.run([str(a) for a in args],cwd=ROOT,check=True,**kw)
with (OUT/'clean_render.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','205','--end','281','--shotlist',OUT/'shotlist.json','--out',OUT/'clean_raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'clean_raw.mp4','-map','0:v','-c:v','copy','-an','-movflags','+faststart',OUT/'clean.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'clean.mp4','-f','null','-'])
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(OUT/'clean.mp4')]))['streams']
assert len(info)==1 and info[0]['codec_type']=='video' and int(info[0]['nb_frames'])==77 and info[0]['r_frame_rate']=='24/1'
snapshot=json.loads((OUT/'shotlist.json').read_text())
shot=next(s for s in snapshot['shots'] if s['id']=='opening_need_landscape')
assert round(shot['start_sec']*24)==205 and round(shot['end_sec']*24)==282
shot['clip']={'file':'out/opening_aerial_glimmer_v1/clean.mp4','in_sec':0,'speed':1}
shot['description']='Approved generated aerial with tracked green garden signal and music-responsive building lights, baked once'
(OUT/'assembly_shotlist.json').write_text(json.dumps(snapshot,indent=2))
(OUT/'delivery.json').write_text(json.dumps({'status':'owner_approved_clean_delivery_ready','clean':'out/opening_aerial_glimmer_v1/clean.mp4','sha256':hashlib.sha256((OUT/'clean.mp4').read_bytes()).hexdigest(),'fps':24,'frames':77,'song_frames':[205,282],'clean_source_frames':[0,77],'audio':False,'lyrics':False,'fx_baked':True,'snapshot':'out/opening_aerial_glimmer_v1/assembly_shotlist.json','cue_snapshot':'out/opening_aerial_glimmer_v1/overlay_cues.json','warning':'Use normal registry-aware assembler with clean snapshot. Do not use light-injecting blender_review.py with baked snapshot: that would double the FX. Original shotlist.json is for reproducing FX from raw source.'},indent=2))
