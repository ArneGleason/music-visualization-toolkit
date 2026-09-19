import subprocess
from pathlib import Path
r=Path(r"C:\audio\shared\amtw-runtime\jobs\monsters-loose-word-timing-20260913")
o=Path(__file__).resolve().parent
args=['ffmpeg','-y','-v','error','-i',str(r/'video-tests/KLING-SIGN-001/KLING-SIGN-001-01.mp4'),'-i',str(r/'video-tests/KLING-SIGN-002/KLING-SIGN-002-01.mp4'),'-i',str(r/'video-tests/KLING-SIGN-001/Harper-sign-master-6s.wav'),'-filter_complex',"[0:v][1:v]blend=all_expr='if(lte(X,1110),A,if(gte(X,1130),B,A*(1130-X)/20+B*(X-1110)/20))'[v]",'-map','[v]','-map','2:a:0','-t','6','-r','24','-c:v','libx264','-crf','17','-preset','fast','-c:a','aac','-b:a','256k','-movflags','+faststart',str(o/'Harper-sign-composite-v001.mp4')]
subprocess.run(args,check=True)
