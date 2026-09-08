from pathlib import Path
import subprocess
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
(OUT/'plates').mkdir(exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(ROOT/'out/outro_depth_timing_v1/preview_numbered.mp4'),'-vf','trim=start_frame=176:end_frame=348,setpts=PTS-STARTPTS','-fps_mode','passthrough',str(OUT/'plates/%04d.png')],check=True)
(OUT/'cleanplates').mkdir(exist_ok=True)
subprocess.run(['ffmpeg','-v','error','-n','-i',str(ROOT/'out/outro_additive_green_v1/preview_numbered.mp4'),'-vf','trim=start_frame=176:end_frame=348,setpts=PTS-STARTPTS','-fps_mode','passthrough',str(OUT/'cleanplates/%04d.png')],check=True)
