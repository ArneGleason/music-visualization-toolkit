import subprocess
from pathlib import Path
o=Path(__file__).resolve().parent;r=o.parent.parent
vf="[0:v]split=2[a][b];[a]trim=start_frame=0:end_frame=60,setpts=PTS-STARTPTS[a0];[b]trim=start_frame=92:end_frame=144,setpts=PTS-STARTPTS[b0];[1:v]fps=24,scale=1916:1080,setsar=1,trim=start_frame=18:end_frame=50,setpts=PTS-STARTPTS,drawbox=x=650:y=65:w=616:h=94:color=0x18201d:t=fill,drawbox=x=655:y=70:w=606:h=84:color=0xf2e6c3:t=fill,drawtext=fontfile='../HARPER-THOUGHT-001/fonts/Bangers-Regular.ttf':text='WE BRING THEM HERE.':fontsize=49:fontcolor=0x18201d:x=(w-text_w)/2:y=90[c];[a0][c][b0]concat=n=3:v=1:a=0[v]"
subprocess.run(['ffmpeg','-y','-v','error','-i',str(r/'motion-graphics/HARPER-SPEECH-001/Harper-speech-v004.mp4'),'-i',str(r/'video-tests/KLING-ARCTIC-001/KLING-ARCTIC-001-01.mp4'),'-filter_complex',vf,'-map','[v]','-map','0:a','-c:v','libx264','-crf','17','-preset','fast','-c:a','copy','-movflags','+faststart',str(o/'Harper-arctic-cutaway-v001.mp4')],check=True,cwd=o)
