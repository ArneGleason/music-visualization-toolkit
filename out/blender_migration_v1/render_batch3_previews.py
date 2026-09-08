"""Context reviews. Adjacent unmigrated shots remain honest look references."""
from pathlib import Path
import subprocess,json
O=Path(__file__).resolve().parent;R=O.parents[1];BL='C:/Program Files/Blender Foundation/Blender 5.2/blender.exe';records=[]
for name,start,end,shots in [('opening',0,155,[1]),('garden',1650,1854,[21,22,23]),('rockets',2928,3072,[37]),('swimmers',3376,3710,[43,44,47]),('tunnel',4060,4177,[54]),('pieces',538,634,[8]),('meant',2611,2658,[32])]:
    raw=O/f'batch3_{name}_raw.mp4';output=O/f'batch3_{name}_context.mp4'
    if not output.exists():
        with (O/f'batch3_{name}_preview.log').open('w') as log:
            subprocess.run([BL,'-b','--python-exit-code','1','-P',str(O/'batch3_preview.py'),'--','--proxy','--start',str(start),'--end',str(end-1),'--shotlist',str(O/'batch3_shotlist.json'),'--lyric-flat','shots/lyric_motion_full.json','--out',str(raw)],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(raw),'-i',str(R/'audio/song.wav'),'-filter_complex',f'[1:a]atrim=start={start/24}:end={end/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v',str(end-start),'-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',str(output)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
    v=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(output)]))['streams'][0]
    assert int(v['nb_frames'])==end-start and v['r_frame_rate']=='24/1'
    still=O/f'batch3_{name}_check.jpg'
    if not still.exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(output),'-vf',f'select=eq(n\\,{(end-start)//2})','-frames:v','1',str(still)],check=True)
    records.append({'name':name,'file':str(output),'song_frames':[start,end],'new_native_shots':shots,'adjacent_shots':'May include accepted pre-migration references; not a full-native movie.'});(O/'batch3_previews.json').write_text(json.dumps(records,indent=2));print(name,'ready',flush=True)
title=O/'batch3_titles_context.mp4'
if not title.exists():
    with (O/'batch3_titles_preview.log').open('w') as log:subprocess.run([BL,'-b','--python-exit-code','1','-P',str(O/'title_review.py')],cwd=R,stdout=log,stderr=subprocess.STDOUT,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(title),'-f','null','-'],check=True)
v=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(title)]))['streams'][0]
assert int(v['nb_frames'])==72 and v['r_frame_rate']=='24/1'
records.append({'name':'titles','file':str(title),'song_frames':[4782,4854],'new_native_shots':[70]});(O/'batch3_previews.json').write_text(json.dumps(records,indent=2))
