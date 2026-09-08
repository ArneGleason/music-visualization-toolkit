from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
fg='[0:v]trim=start_frame=12:end_frame=67,setpts=PTS-STARTPTS[a];[1:v]trim=start_frame=67:end_frame=97,setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=97:end_frame=166,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v];[2:a]atrim=start='+str(4177/24)+':end='+str(4331/24)+',asetpts=PTS-STARTPTS[sound]'
subprocess.run(['ffmpeg','-v','error','-n','-i',str(ROOT/'out/outro_tv_map_v2/clean.mp4'),'-i',str(OUT/'clean.mp4'),'-i',str(ROOT/'audio/song.wav'),'-filter_complex',fg,'-map','[v]','-map','[sound]','-frames:v','154','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(154/24),'-movflags','+faststart',str(OUT/'preview.mp4')],check=True)
checks={}
for name,n in [('clean.mp4',191),('preview.mp4',154)]:
    subprocess.run(['ffmpeg','-v','error','-i',str(OUT/name),'-f','null','-'],check=True)
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,r_frame_rate,nb_read_frames','-of','json',str(OUT/name)]))
    v=next(s for s in data['streams'] if s['codec_type']=='video')
    assert int(v['nb_read_frames'])==n and v['r_frame_rate']=='24/1'
    if name=='clean.mp4':assert len(data['streams'])==1
    checks[name]=data
(OUT/'verification.json').write_text(json.dumps(checks,indent=2))
subprocess.run(['ffmpeg','-v','error','-n','-i',str(OUT/'clean.mp4'),'-vf',r'select=eq(n\,77)','-frames:v','1',str(OUT/'render_check77.png')],check=True)
print('Verified191frame clean and154frame combined preview.')
