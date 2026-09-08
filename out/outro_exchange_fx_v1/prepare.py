from pathlib import Path
import sys,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from assembly_timebase import conform_clip
items=[('A1take','out/outro_A2_v2/take1/synced.mp4','50f8dac28f5a9fdf98108e49077b98985027873229627d39e6df8a13cc01ecf8'),('A2take','out/outro_A2_v2/synced.mp4','67f343cff2e78837e8150c4494608575e178c61fa91ad734c0de04f31da3b618'),('B1take','out/outro_B2_take1_kling_v1/synced.mp4','744f1789b92e1de8e4df72a6fc6d88c61cb602deb0109a076b96df934e8edf3d'),('B2take','out/outro_B2_v2/synced.mp4','26ed64c2dec16db98ccb15877a24e57d826a290ffd58ecd199e597e393ef494f')]
paths={}
for key,path,sha in items:
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha
    paths[key]=conform_clip(ROOT,{'file':path,'speed':1},24,prepare=True)['file']
(OUT/'sources.json').write_text(json.dumps(paths,indent=2))
# Change B take only while she is offscreen. Continuous source/song clock remains.
subprocess.run(['ffmpeg','-v','error','-n','-i',paths['B1take'],'-i',paths['B2take'],'-filter_complex','[0:v]trim=start_frame=0:end_frame=111,setpts=PTS-STARTPTS[a];[1:v]trim=start_frame=111:end_frame=191,setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0[v]','-map','[v]','-an','-c:v','libx264','-crf','16',str(OUT/'b_selected.mp4')],check=True)
print('Four hashes verified; CFR sources prepared; B takes switch offscreen.')
