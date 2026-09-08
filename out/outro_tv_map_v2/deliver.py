from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(args): subprocess.run(['ffmpeg','-v','error','-n']+[str(a) for a in args],check=True)
fg='[0:v]trim=start_frame=12:end_frame=67,setpts=PTS-STARTPTS[a];[1:v]scale=1280:720,setsar=1,trim=end_frame=30,setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=97:end_frame=166,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v];[2:a]atrim=start='+str(4177/24)+':end='+str(4331/24)+',asetpts=PTS-STARTPTS[sound]'
run(['-i',OUT/'clean.mp4','-loop','1','-framerate','24','-i',ROOT/'out/outro_anchors_v2/exobiologist.png','-i',ROOT/'audio/song.wav','-filter_complex',fg,'-map','[v]','-map','[sound]','-frames:v','154','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',154/24,'-movflags','+faststart',OUT/'preview.mp4'])
run(['-i',OUT/'clean.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={4165/24}:end={4356/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',191/24,'-movflags','+faststart',OUT/'full_take_review.mp4'])
info={}
for name,n in [('clean.mp4',191),('preview.mp4',154),('full_take_review.mp4',191)]:
    subprocess.run(['ffmpeg','-v','error','-i',str(OUT/name),'-f','null','-'],check=True)
    p=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,r_frame_rate,nb_read_frames,width,height','-of','json',str(OUT/name)]))
    v=next(s for s in p['streams'] if s['codec_type']=='video')
    assert int(v['nb_read_frames'])==n and v['r_frame_rate']=='24/1'
    if name=='clean.mp4': assert len(p['streams'])==1
    info[name]=p
(OUT/'verification.json').write_text(json.dumps(info,indent=2))
run(['-i',OUT/'clean.mp4','-vf',r'select=eq(n\,155)','-frames:v','1',OUT/'render_check155.png'])
print('Verified clean 191 frames; exchange preview 154 frames; full take 191 frames.')
