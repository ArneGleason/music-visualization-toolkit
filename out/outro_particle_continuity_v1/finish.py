from pathlib import Path
import subprocess,json
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
assert len(list((OUT/'close').glob('*.png')))==84
assert len(list((OUT/'cloud').glob('*.png')))==61
cmd=['ffmpeg','-v','error','-n','-i',str(ROOT/'out/outro_depth_timing_v1/preview_numbered.mp4')]
for folder,start in [('close',4538),('cloud',4622),('cloud',4671)]:
    cmd+=['-framerate','24','-start_number',str(start),'-i',str(OUT/folder/'%04d.png')]
cmd+=['-filter_complex','[0:v]trim=end_frame=176,setpts=PTS-STARTPTS[a];[1:v]trim=end_frame=84,setpts=PTS-STARTPTS[b];[2:v]trim=end_frame=22,setpts=PTS-STARTPTS[c];[0:v]trim=start_frame=282:end_frame=309,setpts=PTS-STARTPTS[d];[3:v]trim=end_frame=39,setpts=PTS-STARTPTS[e];[0:v]trim=start_frame=348,setpts=PTS-STARTPTS[f];[a][b][c][d][e][f]concat=n=6:v=1:a=0[v]','-map','[v]','-map','0:a','-c:v','libx264','-crf','18','-c:a','copy','-movflags','+faststart',str(OUT/'preview_numbered.mp4')]
subprocess.run(cmd,check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview_numbered.mp4'),'-f','null','-'],check=True)
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(OUT/'preview_numbered.mp4')]))
assert int(info['streams'][0]['nb_frames'])==492
(OUT/'verification.json').write_text(json.dumps(info,indent=2));print('492frames verified, music/cuts unchanged.')
