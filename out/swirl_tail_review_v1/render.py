"""Owner-requested end-aligned selection, retaining all neighboring cuts."""
from pathlib import Path
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
m=json.loads((ROOT/'out/swirl_springs_flow_v1/handoff.json').read_text())
for item in [m['claude_result']['base'],m['claude_result']['original']]:
    assert hashlib.sha256((ROOT/item['file']).read_bytes()).hexdigest()==item['sha256']
src=ROOT/m['claude_result']['base']['file']
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(src)]))['streams'][0]
assert info['r_frame_rate']=='24/1' and int(info['nb_frames'])==192
subprocess.run(['ffmpeg','-v','error','-i',str(src),'-f','null','-'],check=True)
code=(ROOT/'out/swimming_to_outro_review_v1/render.py').read_text()
code=code.replace("ROOT/'out/spring_geyser_review_v1/shotlist.json'","ROOT/'out/swimming_to_outro_review_v1/shotlist.json'")
code=code.replace("ROOT/'out/spring_geyser_review_v1/overlay_cues.json'","ROOT/'out/swimming_to_outro_review_v1/overlay_cues.json'")
a=code.index('production=json.loads');b=code.index('ordered=')
replacement="""s=next(s for s in edl['shots'] if s['id']=='turn_phrase')
assert round(s['start_sec']*24)==4030 and round(s['end_sec']*24)==4073
s['clip']={'file':'out/swirl_springs_flow_v1/base.mp4','in_sec':149/24,'speed':1}
s['description']='Owner-requested final43frames of new take, steam and oblique pool reveal rather than spiral'
checks=[{'shot':'turn_phrase','song_frames':[4030,4073],'source':'out/swirl_springs_flow_v1/base.mp4','source_frames':[149,192],'available_frames':192,'exit_handle_frames':0}]
"""
code=code[:a]+replacement+code[b:]
# Only change adapter folder, leaving prior snapshot reads intact.
code=code.replace("'\"swimming_to_outro_review_v1\"'","'\"swirl_tail_review_v1\"'")
exec(compile(code,str(OUT/'inherited.py'),'exec'),{'__file__':str(OUT/'inherited.py'),'__name__':'__main__'})
