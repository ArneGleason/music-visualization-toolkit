import json,subprocess
from pathlib import Path
r=Path(__file__).resolve().parent.parent;o=r/'motion-graphics/OUTRO-003';o.mkdir(exist_ok=True)
src=r/'video-tests/KLING-SCENE14-FINALE-003/KLING-SCENE14-FINALE-003-01.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(src)]))['streams'][0]
assert probe['r_frame_rate']=='24/1' and int(probe['nb_frames'])>=352
dest=o/'FINALE-timed-v003.mp4'
subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-vf','trim=start_frame=12:end_frame=352,setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,setsar=1','-an','-frames:v','340','-r','24','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',str(dest)],check=True)
(o/'selection.json').write_text(json.dumps(dict(source=str(src.relative_to(r)),native_source_in_frame=12,native_source_end_frame_exclusive=352,master_start=4951,master_end_exclusive=5291,fps=24,requested_duration_seconds=15,assumed_leading_frames=12,assumed_trailing_frames=8,actual_trailing_frames=int(probe['nb_frames'])-352,character_reference='assets/SCN-015-FINALE-v002.png',credits=120),indent=2)+'\n')
review=(r/'video-tests/review-outro.py').read_text().replace("+s['name']+'-001'","+s['name']+'-003'").replace('OUTRO-001','OUTRO-003')
(r/'video-tests/review-finale3.py').write_text(review)
print('Trimmed340frames with12frame lead-in')
