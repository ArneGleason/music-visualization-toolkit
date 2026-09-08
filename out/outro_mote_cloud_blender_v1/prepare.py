from pathlib import Path
import subprocess
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
(OUT/'plate').mkdir(exist_ok=True);(OUT/'frames').mkdir(exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(ROOT/'out/outro_additive_green_v1/preview_numbered.mp4'),'-vf','trim=start_frame=260:end_frame=282,setpts=PTS-STARTPTS','-fps_mode','passthrough',str(OUT/'plate/%04d.png')],check=True)
