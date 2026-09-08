import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(a): subprocess.run([str(x) for x in a],check=True,cwd=ROOT)
def samples(p):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
results={}
for name in ['opening','specimen']:
    folder=ROOT/'out/lipsync_review_followup_v1'/name
    h=json.loads((folder/'handoff.json').read_text())
    for key in ['original','synced']:
        r=h['claude_result'][key];assert hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['sha256'].lower()
    a,b=samples(folder/'synced.mp4'),samples(folder/'guide.wav')
    n=min(len(a),len(b));corr=float(np.corrcoef(a[:n],b[:n])[0,1])
    assert corr>.98
    results[name]={'guide_correlation_at_zero_lag':corr,'hashes_verified':True,'approval':'pending owner review'}
    run(['ffmpeg','-v','error','-y','-i',folder/'synced.mp4','-vf','fps=24','-an','-c:v','libx264','-crf','16',OUT/f'{name}_24.mp4'])
    run(['ffmpeg','-v','error','-i',folder/'synced.mp4','-f','null','-'])

# Same music and picture interval for both opening alternatives, without lyrics obscuring comparison.
for name,source in [('opening_new',OUT/'opening_24.mp4'),('opening_current',ROOT/'out/assembly_cfr/synced_a6ed5ea7904f880cb501.mp4')]:
    run(['ffmpeg','-v','error','-y','-i',source,'-i',ROOT/'audio/song.wav','-filter_complex',
        '[0:v]trim=start_frame=12:end_frame=191,setpts=N/(24*TB)[v];[1:a]atrim=start=6.458333333333:end=13.916666666667,asetpts=PTS-STARTPTS[a]',
        '-map','[v]','-map','[a]','-frames:v','179','-c:v','libx264','-crf','17','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/f'{name}.mp4'])

# Preserve the original listening performance before source55 (song2059).
run(['ffmpeg','-v','error','-y','-i',ROOT/'out/specimen_discovery_v1/base.mp4','-i',OUT/'specimen_24.mp4',
    '-filter_complex','[0:v]trim=end_frame=55,setpts=N/(24*TB)[a];[1:v]trim=start_frame=55,setpts=N/(24*TB)[b];[a][b]concat=n=2:v=1:a=0[v]',
    '-map','[v]','-an','-c:v','libx264','-crf','16',OUT/'specimen_combined.mp4'])
source=(ROOT/'out/specimen_signal_v1/render.py').read_text().split('edl=json.loads',1)[0]
source=source.replace("ROOT/'out/specimen_discovery_v1/base.mp4'","ROOT/'out/lipsync_followup_review_v1/specimen_combined.mp4'")
exec(compile(source,'specimen_fx_reapply','exec'),{'__name__':'__main__','__file__':str(OUT/'fx.py')})
run(['ffmpeg','-v','error','-y','-i',OUT/'clean.mp4','-i',ROOT/'audio/song.wav','-filter_complex',
    '[1:a]atrim=start=84:end=88.416666666667,asetpts=PTS-STARTPTS[a]',
    '-map','0:v','-map','[a]','-frames:v','106','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'specimen_preview.mp4'])
for name in ['opening_new','opening_current','specimen_preview']:
    run(['ffmpeg','-v','error','-i',OUT/f'{name}.mp4','-f','null','-'])
(OUT/'verification.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results),flush=True)
