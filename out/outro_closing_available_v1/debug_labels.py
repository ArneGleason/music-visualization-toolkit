"""Label the exact current preview without changing its cuts, picture or audio timing."""
from pathlib import Path
import sys,json,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
rows=[
 (4362,4400,'Astronomer','Thought I heard something.','A2 take 1 + TV graphics'),
 (4400,4431,'Exobiologist','You did.','B2 take 1 + afterglow'),
 (4431,4461,'Astronomer','Was it you?','A2 take 1 + TV graphics'),
 (4461,4504,'Exobiologist',"Da-da-dum / Could have been.",'B2 take 2 + afterglow'),
 (4504,4557,'Astronomer','Say goodnight.','A3 Kling / closer crop'),
 (4557,4574,'Exobiologist (offscreen)','To who?','Artifact insert'),
 (4574,4622,'Astronomer','La-la-la-la-la','A3 Kling / reaches toward TV'),
 (4622,4644,'Exobiologist','You first.','B3 take 2 / NOT lip-synced'),
 (4644,4671,'Astronomer','Night.','A3 Kling / TV shutdown SKETCH'),
 (4671,4689,'Exobiologist','Night.','B3 take 2 / NOT lip-synced / dimming SKETCH'),
 (4689,4782,'Mars night vista','Offscreen Night, then musical tail','One continuous shot / iris at song frame 4754'),
 (4782,4854,'Closing title','No dialogue','Placeholder title / 3-second silent hold')]
cap=cv2.VideoCapture(str(OUT/'preview.mp4'))
w=cv2.VideoWriter(str(OUT/'debug_silent.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),24,(1280,720));assert w.isOpened()
i=0
while True:
    ok,f=cap.read()
    if not ok:break
    song=4362+i
    k,(a,b,who,line,note)=next((k,r) for k,r in enumerate(rows) if r[0]<=song<r[1])
    # Replace the old review-caption band with an explicit debug header.
    cv2.rectangle(f,(0,0),(1280,95),(12,12,12),-1)
    cv2.putText(f,f'{who}: {line}',(18,30),cv2.FONT_HERSHEY_SIMPLEX,.78,(245,245,245),2,cv2.LINE_AA)
    cv2.putText(f,note,(18,59),cv2.FONT_HERSHEY_SIMPLEX,.55,(175,215,240),1,cv2.LINE_AA)
    cv2.putText(f,f'Song frame {song} | {song/24:.3f}s | cut [{a}, {b})',(18,83),cv2.FONT_HERSHEY_SIMPLEX,.48,(180,180,180),1,cv2.LINE_AA)
    cv2.circle(f,(1228,46),34,(0,0,0),-1,cv2.LINE_AA)
    s=str(k+1);sz=cv2.getTextSize(s,cv2.FONT_HERSHEY_SIMPLEX,1,2)[0]
    cv2.putText(f,s,(1228-sz[0]//2,57),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
    w.write(f)
    if i==0:cv2.imwrite(str(OUT/'debug_check.jpg'),f)
    i+=1
cap.release();w.release();assert i==492
subprocess.run(['ffmpeg','-v','error','-n','-i',str(OUT/'debug_silent.mp4'),'-i',str(OUT/'preview.mp4'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','18','-c:a','copy','-frames:v','492','-movflags','+faststart',str(OUT/'preview_numbered.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'preview_numbered.mp4'),'-f','null','-'],check=True)
(OUT/'debug_shot_map.json').write_text(json.dumps([{'number':k+1,'song_frames':[a,b],'who':who,'line':line,'note':note} for k,(a,b,who,line,note) in enumerate(rows)],indent=2))
print('Numbered debug preview ready,492 frames. Original audio copied unchanged.')
