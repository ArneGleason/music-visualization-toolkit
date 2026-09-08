"""Render and validate the green-light walk, then numbered native context."""
from pathlib import Path
import subprocess,json,sys,hashlib
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'walk'; BL='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
def run(name,args):
    with (O/f'{name}.log').open('w') as log:subprocess.run(args,cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
    print(name,'finished',flush=True)
run('walk_render',[BL,'-b',str(D/'walk_1280.blend'),'--python-exit-code','1','-P',str(O/'render_saved_frames.py'),'--',str(D/'native_1280'),'1','103'])
run('walk_1920',[BL,'-b','--python-exit-code','1','-P',str(O/'walk_native.py'),'--','walk','1920','1,25,40,65,78,102'])
clean=D/'native_clean.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(D/'native_1280/%04d.png'),'-frames:v','102','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(clean)],check=True)
edl=json.loads((O/'screen_shotlist.json').read_text());shot=next(s for s in edl['shots'] if s['id']=='garden_walk')
shot['clip']={'file':str(clean.relative_to(R)).replace('\\','/'),'in_sec':0,'speed':1};(O/'walk_shotlist.json').write_text(json.dumps(edl,indent=2))
raw=O/'walk_context_raw.mp4';output=O/'walk_context.mp4'
run('walk_preview',[BL,'-b','-t','8','--python-exit-code','1','-P',str(O/'batch3_preview.py'),'--','--proxy','--start','1374','--end','1513','--shotlist',str(O/'walk_shotlist.json'),'--lyric-flat','shots/lyric_motion_full.json','--out',str(raw)])
subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-i',str(R/'audio/song.wav'),'-filter_complex','[1:a]atrim=start=57.25:end=63.083333333333,asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','140','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',str(output)],check=True)
receipts=[]
for file,count in [(clean,102),(output,140)]:
    subprocess.run(['ffmpeg','-v','error','-i',str(file),'-f','null','-'],check=True)
    streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,nb_frames,r_frame_rate','-of','json',str(file)]))['streams'];v=next(s for s in streams if s['codec_type']=='video')
    assert v['r_frame_rate']=='24/1' and int(v['nb_frames'])==count and len(streams)==(2 if file==output else 1)
    receipts.append({'file':str(file.relative_to(R)),'frames':count,'fps':24,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(D/'receipts.json').write_text(json.dumps(receipts,indent=2))
run('walk_audit',[BL,'-b','--python-exit-code','1','-P',str(O/'audit_walk.py')])
subprocess.run([sys.executable,str(O/'check_walk.py')],cwd=R,check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(output),'-vf','select=not(mod(n\\,20)),scale=480:-1,tile=4x2','-frames:v','1',str(O/'walk_contact.jpg')],check=True)
print('Walk preview ready, checks passed',flush=True)
