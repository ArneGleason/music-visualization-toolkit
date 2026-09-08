from pathlib import Path
import subprocess,json,sys
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
assert len(list((OUT/'frames').glob('*.png')))==22
assert len(list((OUT/'extension_frames').glob('*.png')))==9
subprocess.run(['ffmpeg','-v','error','-n','-i',str(ROOT/'out/outro_additive_green_v1/preview_numbered.mp4'),'-framerate','24','-i',str(OUT/'extension_frames/%04d.png'),'-framerate','24','-i',str(OUT/'frames/%04d.png'),'-filter_complex','[0:v]trim=end_frame=176,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=185:end_frame=260,setpts=PTS-STARTPTS[c];[2:v]setpts=PTS-STARTPTS[d];[0:v]trim=start_frame=282,setpts=PTS-STARTPTS[e];[a][b][c][d][e]concat=n=5:v=1:a=0[v]','-map','[v]','-map','0:a','-c:v','libx264','-crf','18','-c:a','copy','-movflags','+faststart',str(OUT/'preview_numbered.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview_numbered.mp4'),'-f','null','-'],check=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(OUT/'preview_numbered.mp4')]))
assert int(info['streams'][0]['nb_frames'])==492
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2,numpy as np
low=cv2.imread(str(OUT/'frames/0011.png'));high=cv2.imread(str(OUT/'check_1080_0011.png'))
assert high.shape[:2]==(1080,1920)
small=cv2.resize(high,(1280,720),interpolation=cv2.INTER_AREA)
info['single_frame_resolution_check']={'frame':11,'720_vs_downsampled_1080_mean_abs_code_difference':float(np.mean(np.abs(low.astype(float)-small.astype(float)))),'scope':'single composite frame only; not full animation certification'}
(OUT/'verification.json').write_text(json.dumps(info,indent=2))
print(json.dumps(info))
