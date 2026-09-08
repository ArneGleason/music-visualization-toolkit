"""Native transition render and isolated numbered contextual assembly."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,hashlib,sys
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'screen'
BL='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
def run(name,args):
    with (O/f'{name}.log').open('w') as log:subprocess.run(args,cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
    print(name,'finished',flush=True)
jobs=[(f'screen_{a}',[BL,'-b',str(D/'screen_1280.blend'),'--python-exit-code','1','-P',str(O/'render_saved_frames.py'),'--',str(D/'native_1280'),str(a),str(z)]) for a,z in [(13,65),(65,116)]]
with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda job:run(*job),jobs))
run('screen_1920',[BL,'-b','--python-exit-code','1','-P',str(O/'screen_native.py'),'--','screen','1920','13,25,57,64,69,70,115'])
clean=D/'native_clean.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-start_number','13','-i',str(D/'native_1280/%04d.png'),'-frames:v','103','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(clean)],check=True)
edl=json.loads((O/'message_shotlist.json').read_text())
for ident,file in [('screen_reply',clean),('garden_entry',R/'clips/raw/forest_threshold_v6.mp4')]:
    shot=next(s for s in edl['shots'] if s['id']==ident)
    shot['clip']={'file':str(file.relative_to(R)).replace('\\','/'),'in_sec':0,'speed':1}
(O/'screen_shotlist.json').write_text(json.dumps(edl,indent=2))
raw=O/'screen_context_raw.mp4'; output=O/'screen_context.mp4'
run('screen_preview',[BL,'-b','-t','8','--python-exit-code','1','-P',str(O/'batch3_preview.py'),'--','--proxy','--start','1137','--end','1411','--shotlist',str(O/'screen_shotlist.json'),'--lyric-flat','shots/lyric_motion_full.json','--out',str(raw)])
subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-i',str(R/'audio/song.wav'),'-filter_complex','[1:a]atrim=start=47.375:end=58.833333333333,asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','275','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',str(output)],check=True)
receipts=[]
for file,count in [(clean,103),(output,275)]:
    subprocess.run(['ffmpeg','-v','error','-i',str(file),'-f','null','-'],check=True)
    streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,nb_frames,r_frame_rate','-of','json',str(file)]))['streams']; v=next(s for s in streams if s['codec_type']=='video')
    assert v['r_frame_rate']=='24/1' and int(v['nb_frames'])==count
    assert len(streams)==(2 if file==output else 1)
    receipts.append({'file':str(file.relative_to(R)),'frames':count,'fps':24,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(D/'receipts.json').write_text(json.dumps(receipts,indent=2))
run('screen_audit',[BL,'-b','--python-exit-code','1','-P',str(O/'audit_screen.py')])
subprocess.run([sys.executable,str(O/'check_screen.py')],cwd=R,check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(output),'-vf','select=not(mod(n\\,34)),scale=480:-1,tile=4x2','-frames:v','1',str(O/'screen_contact.jpg')],check=True)
print('Screen contextual preview and checks complete',flush=True)
