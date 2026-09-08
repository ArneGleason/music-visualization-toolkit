from pathlib import Path
import subprocess
OUT=Path(__file__).resolve().parent
source=(OUT/'build.py').read_text().split('w=cv2.VideoWriter')[0]
exec(compile(source,str(OUT/'build.py'),'exec'))
w=cv2.VideoWriter(str(OUT/'night.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),24,(1280,720))
for song in range(4644,4671):
    f=tv(A3[song-4492].copy(),3,song,shutdown=True)
    cv2.rectangle(f,(0,0),(1280,91),(12,12,12),-1)
    cv2.putText(f,'Astronomer: Night.',(16,29),cv2.FONT_HERSHEY_SIMPLEX,.73,(245,245,245),2,cv2.LINE_AA)
    cv2.putText(f,'Additive phosphor collapse / night-shot screen fit',(16,57),cv2.FONT_HERSHEY_SIMPLEX,.51,(170,210,240),1,cv2.LINE_AA)
    cv2.putText(f,f'Song {song} | {song/24:.3f}s',(16,80),cv2.FONT_HERSHEY_SIMPLEX,.46,(175,175,175),1,cv2.LINE_AA)
    cv2.circle(f,(1230,43),32,(0,0,0),-1)
    cv2.putText(f,'9',(1213,54),cv2.FONT_HERSHEY_SIMPLEX,.9,(255,255,255),2,cv2.LINE_AA)
    w.write(f)
    if song==4658:cv2.imwrite(str(OUT/'night_check.jpg'),f)
w.release()
subprocess.run(['ffmpeg','-v','error','-n','-i',str(OUT/'preview_numbered.mp4'),'-i',str(OUT/'night.mp4'),'-filter_complex','[0:v]trim=end_frame=282,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=309,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]','-map','[v]','-map','0:a','-c:v','libx264','-crf','18','-c:a','copy','-movflags','+faststart',str(OUT/'preview_numbered_final.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview_numbered_final.mp4'),'-f','null','-'],check=True)
print('Night-screen fit corrected and final preview decoded.')
