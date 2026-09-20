from pathlib import Path
import json,subprocess
r=Path(__file__).resolve().parents[2];o=Path(__file__).resolve().parent
for sh in json.loads((o/'selections.json').read_text()):
 start=sh['source_in_frame'];count=sh['edit_frames']
 vf=f"trim=start_frame={start}:end_frame={start+count},setpts=PTS-STARTPTS,scale=3840:-2,zoompan=z='1+0.04*on/{count-1}':x='iw*0.52-iw*0.52/zoom':y='ih*0.36-ih*0.36/zoom':d=1:s=1916x1080:fps=24,setsar=1"
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(r/sh['source']),'-vf',vf,'-frames:v',str(count),'-an','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-movflags','+faststart',str(o/(sh['name']+'-push-v001.mp4'))],check=True)
