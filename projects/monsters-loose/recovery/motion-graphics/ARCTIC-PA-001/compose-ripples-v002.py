import json, subprocess
from pathlib import Path

o=Path(__file__).resolve().parent
r=o.parent.parent
def run(args):
    subprocess.run(['ffmpeg','-y','-v','error',*args],check=True)

patrol=r/'video-tests/KLING-PATROL-001/KLING-PATROL-001-01.mp4'
reaction=o/'Harper-reaction-eyes-v001.mp4'
pa=o/'Arctic-PA-ripples-v002.mp4'
inputs=[]
for p in (patrol,pa,reaction,r/'master.wav'):
    inputs+=['-i',str(p)]
graph=(
    '[0:v]trim=start_frame=12:end_frame=151,setpts=PTS-STARTPTS,scale=1280:720,setsar=1[a];'
    '[1:v]trim=start_frame=0:end_frame=108,setpts=PTS-STARTPTS,setsar=1[b];'
    '[2:v]trim=start_frame=12:end_frame=171,setpts=PTS-STARTPTS,scale=1280:720,setsar=1[c];'
    '[a][b][c]concat=n=3:v=1:a=0[v];'
    '[3:a]atrim=start_sample=1252000:end_sample=2064000,asetpts=PTS-STARTPTS[audio]'
)
# Master WAV sample rate is queried; frame-derived boundaries remain authoritative.
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=sample_rate','-of','json',str(r/'master.wav')]))
sr=int(info['streams'][0]['sample_rate'])
graph=graph.replace('1252000',str(round(626*sr/24))).replace('2064000',str(round(1032*sr/24)))
run([*inputs,'-filter_complex',graph,'-map','[v]','-map','[audio]','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','320k','-movflags','+faststart',str(o/'Arctic-patrol-announcement-reaction-v004.mp4')])

