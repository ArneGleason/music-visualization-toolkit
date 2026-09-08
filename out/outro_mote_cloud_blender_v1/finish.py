from pathlib import Path
import subprocess,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
assert len(list((OUT/'frames').glob('*.png')))==22
subprocess.run(['ffmpeg','-v','error','-n','-i',str(ROOT/'out/outro_additive_green_v1/preview_numbered.mp4'),'-framerate','24','-i',str(OUT/'frames/%04d.png'),'-filter_complex','[0:v]trim=end_frame=260,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=282,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]','-map','[v]','-map','0:a','-c:v','libx264','-crf','18','-c:a','copy','-movflags','+faststart',str(OUT/'preview_numbered.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview_numbered.mp4'),'-f','null','-'],check=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(OUT/'preview_numbered.mp4')]))
assert int(info['streams'][0]['nb_frames'])==492
print('Verified full numbered preview, 492 frames. Blender composite replaces shot8 only.')
