from pathlib import Path
import json,subprocess
O=Path(__file__).resolve().parent;R=O.parents[1]
result=[]
for name,start,end in [('receiver',670,911),('specimen',1973,2122)]:
    out=O/f'lights2_{name}_context.mp4'
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(O/f'lights2_{name}_raw.mp4'),'-i',str(R/'audio/song.wav'),'-filter_complex',f'[1:a]atrim=start={start/24}:end={end/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v',str(end-start),'-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',str(out)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(out)]))['streams'][0]
    assert int(info['nb_frames'])==end-start and info['r_frame_rate']=='24/1'
    subprocess.run(['ffmpeg','-v','error','-n','-i',str(out),'-vf',f'select=eq(n\\,{150 if name=="receiver" else 110})','-frames:v','1',str(O/f'lights2_{name}_check.jpg')],check=True)
    result.append({'file':str(out),'song_frames':[start,end],'frames':end-start})
(O/'lights2_previews.json').write_text(json.dumps(result,indent=2))
