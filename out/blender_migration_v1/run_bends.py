"""Render and validate this isolated native migration, then export context."""
from pathlib import Path
import subprocess,json,hashlib,sys
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'bends'
BL='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
for width,frames in [(1280,None),(1920,'1,35,70,100,120,137')]:
    args=[BL,'-b','--python-exit-code','1','-P',str(O/'bends_native.py'),'--','bends',str(width)]
    if frames:args.append(frames)
    with (O/f'bends_{width}.log').open('w') as log:subprocess.run(args,cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
    print('Rendered',width,flush=True)
clean=D/'native_clean.mp4'
subprocess.run(['ffmpeg','-v','error','-n','-framerate','24','-i',str(D/'native_1280/%04d.png'),'-frames:v','137','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(clean)],check=True)
edl=json.loads((O/'batch3_shotlist.json').read_text())
for ident,offset in [('s045',0),('s046',69)]:
    shot=next(s for s in edl['shots'] if s['id']==ident)
    shot['clip']={'file':str(clean.relative_to(R)).replace('\\','/'),'in_sec':offset/24,'speed':1}
(O/'bends_shotlist.json').write_text(json.dumps(edl,indent=2))
raw=O/'bends_context_raw.mp4'; output=O/'bends_context.mp4'; start,end=3438,3710
with (O/'bends_preview.log').open('w') as log:
    subprocess.run([BL,'-b','--python-exit-code','1','-P',str(O/'batch3_preview.py'),'--','--proxy','--start',str(start),'--end',str(end-1),'--shotlist',str(O/'bends_shotlist.json'),'--lyric-flat','shots/lyric_motion_full.json','--out',str(raw)],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(raw),'-i',str(R/'audio/song.wav'),'-filter_complex',f'[1:a]atrim=start={start/24}:end={end/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v',str(end-start),'-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',str(output)],check=True)
receipts=[]
for file,frames in [(clean,137),(output,272)]:
    subprocess.run(['ffmpeg','-v','error','-i',str(file),'-f','null','-'],check=True)
    v=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,nb_frames,r_frame_rate','-of','json',str(file)]))['streams']
    video=next(s for s in v if s['codec_type']=='video'); assert int(video['nb_frames'])==frames and video['r_frame_rate']=='24/1'
    assert len(v)==(1 if file==clean else 2)
    receipts.append({'file':str(file),'frames':frames,'fps':24,'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(D/'receipts.json').write_text(json.dumps(receipts,indent=2))
subprocess.run(['ffmpeg','-v','error','-n','-i',str(output),'-vf','select=not(mod(n\\,34)),scale=480:-1,tile=4x2','-frames:v','1',str(O/'bends_contact.jpg')],check=True)
print('Bends native context ready',flush=True)
