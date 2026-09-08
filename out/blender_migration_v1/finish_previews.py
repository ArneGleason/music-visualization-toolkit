from pathlib import Path
import json,subprocess
O=Path(__file__).resolve().parent;R=O.parents[1]
checks=[]
for name,start,end in [('aerial',155,334),('probe',670,911)]:
    raw=O/f'{name}_context_raw.mp4';dest=O/f'{name}_context.mp4'
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(raw),'-i',str(R/'audio/song.wav'),'-filter_complex',f'[1:a]atrim=start={start/24}:end={end/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v',str(end-start),'-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',str(dest)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,width,height','-of','json',str(dest)]))['streams'][0]
    assert int(info['nb_frames'])==end-start and info['r_frame_rate']=='24/1'
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(dest),'-vf','select=eq(n\\,80)','-frames:v','1',str(O/f'{name}_context_check.jpg')],check=True)
    checks.append({'file':str(dest),'song_frames':[start,end],'metadata':info})
(O/'context_previews.json').write_text(json.dumps(checks,indent=2))
