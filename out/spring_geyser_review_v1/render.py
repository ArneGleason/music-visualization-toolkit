"""Verify and audition returned geyser, without corrective edits or retiming."""
from pathlib import Path
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
m=json.loads((ROOT/'out/spring_geyser_flow_v1/handoff.json').read_text())
for item in list(m['inputs'].values())+[m['claude_result']['base'],m['claude_result']['original']]:
    assert hashlib.sha256((ROOT/item['file']).read_bytes()).hexdigest()==item['sha256'],item['file']
src=ROOT/m['claude_result']['base']['file']
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(src)]))['streams'][0]
assert int(info['nb_frames'])==192 and info['r_frame_rate']=='24/1'
subprocess.run(['ffmpeg','-v','error','-i',str(src),'-f','null','-'],check=True)
code=(ROOT/'out/springs_splash_review_v1/render.py').read_text()
a=code.index("run(['ffmpeg'");b=code.index('edl=json.loads')
code=code[:a]+code[b:]
code=code.replace('springs_splash_review_v1','spring_geyser_review_v1')
code=code.replace('out/spring_geyser_review_v1/still.mp4','out/spring_geyser_flow_v1/base.mp4')
code=code.replace('STATIC CONCEPT: natural geothermal spray falling into familiar spring pool','Returned Flow geyser pressure collapse and splash, unretimed source0..78')
code=code.replace("'spring_static_song_frames'","'spring_video_song_frames'").replace("'none, still only'","'Flow source0..78 at native24fps; no timing change'")
exec(compile(code,str(OUT/'inherited.py'),'exec'),{'__file__':str(OUT/'inherited.py'),'__name__':'__main__'})
v=json.loads((OUT/'verification.json').read_text());v.update(hashes_verified=True,source_frames=192,source_used=[0,78],unused_tail_frames=114,generated_audio_excluded=True,known_deviations=m['claude_result']['defects']+m['claude_result']['gross_failures'])
(OUT/'verification.json').write_text(json.dumps(v,indent=2))
