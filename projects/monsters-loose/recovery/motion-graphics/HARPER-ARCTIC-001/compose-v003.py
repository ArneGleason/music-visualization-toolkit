from pathlib import Path
import subprocess
r=Path(__file__).resolve().parents[2];o=Path(__file__).resolve().parent
vf="[0:v][3:v]overlay=0:0:shortest=1,trim=start_frame=0:end_frame=60,setpts=PTS-STARTPTS[a];[1:v]trim=start_frame=60:end_frame=92,setpts=PTS-STARTPTS[b];[2:v][4:v]overlay=0:0:shortest=1,trim=start_frame=92:end_frame=144,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]"
subprocess.run(['ffmpeg','-y','-v','error','-i',str(r/'motion-graphics/HARPER-SIGN-SPLICE-001/Harper-sign-composite-v001.mp4'),'-i',str(o/'Harper-arctic-cutaway-v002.mp4'),'-i',str(o/'Harper-take2-eye-v001.mp4'),'-framerate','24','-i',str(r/'motion-graphics/HARPER-SPEECH-001/frames-v005/bubble-%04d.png'),'-framerate','24','-i',str(r/'motion-graphics/HARPER-SPEECH-001/frames-v005/bubble-%04d.png'),'-filter_complex',vf,'-map','[v]','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-c:a','copy','-movflags','+faststart',str(o/'Harper-arctic-cutaway-v003.mp4')],check=True)
