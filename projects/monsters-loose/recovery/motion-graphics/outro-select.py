import json,subprocess
from pathlib import Path
r=Path(__file__).resolve().parent.parent
plan=json.loads((r/'shots/SCN-014-015-production-plan.json').read_text())
out=r/'motion-graphics/OUTRO-001';out.mkdir(exist_ok=True)
# Native source in-points selected after contact-sheet performance review.
ins={s['name']:12 for s in plan['shots']}
ins.update(DISPLAY=22,SCIENTISTS=30,INSPECTOR=30,PLAY=36)
selections=[]
for s in plan['shots']:
 name=s['name'];folder=r/'video-tests'/('KLING-SCENE14-'+name+'-001');src=folder/(folder.name+'-01.mp4')
 start=ins[name];length=s['duration_frames'];dest=out/(name+'-timed-v001.mp4')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(src)]))['streams'][0]
 assert probe['r_frame_rate']=='24/1'
 native_frames=int(probe['nb_frames'])
 assert start+length<=native_frames
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-vf',f'trim=start_frame={start}:end_frame={start+length},setpts=PTS-STARTPTS,scale=1920:1080:flags=lanczos,setsar=1','-an','-r','24','-frames:v',str(length),'-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',str(dest)],check=True)
 n=int(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','csv=p=0',str(dest)]))
 assert n==length,(name,n,length)
 selections.append(dict(id=s['id'],name=name,start_frame=s['start_frame'],end_frame_exclusive=s['end_frame_exclusive'],source=str(dest.relative_to(r)).replace('\\','/'),source_in_frame=0,original_video_source=str(src.relative_to(r)).replace('\\','/'),native_source_in_frame=start,native_source_end_frame_exclusive=start+length,duration_frames=length,generation_fps=24,generation_seconds=s['generation_seconds'],assumed_pre_roll_frames=12,assumed_pre_roll_seconds=.5,assumed_post_roll_frames=s['post_roll_frames'],assumed_post_roll_seconds=s['post_roll_frames']/24,assumed_master_frame_at_source_zero=s['start_frame']-12,actual_leading_handle_frames=start,actual_trailing_handle_frames=native_frames-start-length,generation_record=s['generation_record']))
 print(name,n,flush=True)
(out/'selections.json').write_text(json.dumps(dict(fps=24,selections=selections),indent=2)+'\n')
