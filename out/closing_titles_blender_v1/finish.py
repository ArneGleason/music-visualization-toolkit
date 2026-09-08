from pathlib import Path
import subprocess, json
O = Path(__file__).resolve().parent
assert len(list((O/'frames').glob('*.png'))) == 72
prior = O.parent/'outro_particle_continuity_v1/preview_numbered.mp4'
subprocess.run(['ffmpeg','-v','error','-n','-framerate','24','-start_number','1','-i',str(O/'frames/%04d.png'),'-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(O/'closing_titles.mp4')], check=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(prior),'-i',str(O/'closing_titles.mp4'),'-filter_complex','[0:v]trim=end_frame=420,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-map','0:a','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(O/'preview_numbered.mp4')], check=True)
p = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate,width,height','-of','json',str(O/'preview_numbered.mp4')]))
assert int(p['streams'][0]['nb_frames']) == 492
subprocess.run(['ffmpeg','-v','error','-i',str(O/'preview_numbered.mp4'),'-f','null','-'], check=True)
(O/'verification.json').write_text(json.dumps(p,indent=2))
