"""Keep crop/reframe operations native instead of upscaling baked 720 inserts."""
from pathlib import Path
import json,subprocess
O=Path(__file__).resolve().parent;R=O.parents[1]
for family,source,start,n,song,crop in [('pieces','clips/raw/canal_map_macro_v6.mp4',24,48,562,[160,180,960,540]),('meant','out/archaeology_discovery_v1/base.mp4',120,11,2647,[320,290,640,360])]:
    D=O/family;(D/'plates').mkdir(parents=True,exist_ok=True)
    if not (D/f'plates/{n:04d}.png').exists():subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/source),'-vf',f'trim=start_frame={start}:end_frame={start+n},setpts=PTS-STARTPTS','-frames:v',str(n),str(D/'plates/%04d.png')],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(D/'plates/0001.png')]))['streams'][0]
    (D/'controls.json').write_text(json.dumps({'frames':[{'song_frame':song+i} for i in range(n)],'song_frames':[song,song+n],'source':source,'source_frames':[start,start+n],'crop_xywh':crop,'source_dimensions':[probe['width'],probe['height']]},indent=2))
