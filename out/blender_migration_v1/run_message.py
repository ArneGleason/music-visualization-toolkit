"""Independent native render ranges, then resolver-aware numbered review."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,hashlib,sys
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'message'; BL='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
def execute(name,args):
    with (O/f'{name}.log').open('w') as log:subprocess.run(args,cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
    print(name,'finished',flush=True)
jobs=[]
repair='--repair' in sys.argv
for first,last in ([(167,199),(199,231)] if repair else [(1,116),(116,231)]):
    jobs.append((f'message_{first}',[BL,'-b',str(D/'message_1280.blend'),'--python-exit-code','1','-P',str(O/'render_saved_frames.py'),'--',str(D/'native_1280'),str(first),str(last)]))
with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(lambda job:execute(*job),jobs))
if not repair:execute('message_1920',[BL,'-b','--python-exit-code','1','-P',str(O/'message_native.py'),'--','message','1920','1,70,100,112,155,211,230'])
clean=D/'native_clean.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(D/'native_1280/%04d.png'),'-frames:v','230','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(clean)],check=True)
edl=json.loads((O/'bends_shotlist.json').read_text())
# This isolated preview begins partway through s012. Preserve canonical clocks;
# map the full performance into a native cache with its first60 untouched frames.
full=D/'performance_clean.mp4'
source=json.loads((D/'controls.json').read_text())['sources'][0]['file']
subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/source),'-i',str(clean),'-filter_complex','[0:v]trim=start_frame=12:end_frame=72,setpts=PTS-STARTPTS[a];[1:v]trim=start_frame=0:end_frame=111,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-frames:v','171','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p',str(full)],check=True)
for ident,file,offset in [('s012',full,0),('receiver_reply_arrival',clean,111)]:
    shot=next(s for s in edl['shots'] if s['id']==ident); shot['clip']={'file':str(file.relative_to(R)).replace('\\','/'),'in_sec':offset/24,'speed':1}
(O/'message_shotlist.json').write_text(json.dumps(edl,indent=2))
raw=O/'message_context_raw.mp4'; output=O/'message_context.mp4'
execute('message_preview',[BL,'-b','-t','8','--python-exit-code','1','-P',str(O/'batch3_preview.py'),'--','--proxy','--start','971','--end','1200','--shotlist',str(O/'message_shotlist.json'),'--lyric-flat','shots/lyric_motion_full.json','--out',str(raw)])
subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-i',str(R/'audio/song.wav'),'-filter_complex','[1:a]atrim=start=40.458333333333:end=50.041666666667,asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','230','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',str(output)],check=True)
receipts=[]
for file,count in [(clean,230),(full,171),(output,230)]:
    subprocess.run(['ffmpeg','-v','error','-i',str(file),'-f','null','-'],check=True)
    streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,nb_frames,r_frame_rate','-of','json',str(file)]))['streams']; video=next(s for s in streams if s['codec_type']=='video')
    assert video['r_frame_rate']=='24/1' and int(video['nb_frames'])==count; assert len(streams)==(2 if file==output else 1)
    receipts.append({'file':str(file),'frames':count,'fps':24,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(D/'receipts.json').write_text(json.dumps(receipts,indent=2))
subprocess.run(['ffmpeg','-v','error','-y','-i',str(output),'-vf','select=not(mod(n\\,28)),scale=480:-1,tile=4x2','-frames:v','1',str(O/'message_contact.jpg')],check=True)
execute('message_audit',[BL,'-b','--python-exit-code','1','-P',str(O/'audit_message.py')])
subprocess.run([sys.executable,str(O/'check_message.py')],cwd=R,check=True)
print('Message preview ready, verification passed',flush=True)
