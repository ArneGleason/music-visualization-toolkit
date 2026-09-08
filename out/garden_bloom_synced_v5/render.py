"""Verify the returned bloom sync, preserve timestamps, rebuild accepted FX."""
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
handoff=ROOT/'out/garden_bloom_lipsync_v2'
h=json.loads((handoff/'handoff.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()
checks={}
for name in ('base','guide'):
    entry=h['inputs'][name]
    checks[name]=sha(ROOT/entry['file'])==entry['sha256']
for name in ('synced','original'):
    entry=h['claude_result'][name]
    checks[name]=sha(ROOT/entry['file'])==entry['sha256']
assert all(checks.values()),checks
source=handoff/'synced.mp4'
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
                                       '-of','json',str(source)]))
video=next(s for s in info['streams'] if s['codec_type']=='video')
assert video['r_frame_rate']=='30/1' and float(video['duration'])>=134/24
def mono(p):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),
        '-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32)
a,b=mono(source),mono(handoff/'guide.wav')
n=min(len(a),len(b)); correlation=float(np.corrcoef(a[:n],b[:n])[0,1])
assert correlation>.95,correlation
subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-map','0:v:0',
    '-vf','fps=24','-an','-c:v','libx264','-crf','15','-pix_fmt','yuv420p',
    str(OUT/'plate24.mp4')],check=True)
(OUT/'verification.json').write_text(json.dumps({'hash_checks':checks,
    'native_video':{k:video[k] for k in ('width','height','r_frame_rate','nb_frames','duration')},
    'audio_guide_correlation_zero_lag':correlation,
    'conform':'Timestamp-resampled fps=24, no reinterpretation, no speed change, no added offset.',
    'source_song_origin':1720,'source_frames_24fps':[66,134],'song_frames':[1786,1854],
    'articulation':'Claude reports partial/weak articulation, not corrected by assembly. Owner review required.'},indent=2))

p=ROOT/'out/garden_begin_bloom_v3/render.py'
s=p.read_text()
start=s.index('# Reuse the approved green guide')
end=s.index('source_path = ROOT /',start)
s=s[:start]+"namespace = {'__file__': str(ROOT/'out/garden_guide_conductor_v4/guide.py')}\nexec(compile((ROOT/'out/garden_guide_conductor_v4/guide.py').read_text(), 'guide.py', 'exec'), namespace)\n\n"+s[end:]
s=s.replace('garden_begin_bloom_v3','garden_bloom_synced_v5')
old="s = source_path.read_text().replace('garden_begin_light_v1', 'garden_bloom_synced_v5')"
assert old in s
s=s.replace(old,old+"\ns = s.replace('clips/raw/forest_awakening_frontal_v6.mp4', 'out/garden_bloom_synced_v5/plate24.mp4')")
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
r=json.loads((OUT/'recipe.json').read_text())
r.update(lip_sync_used=True,lip_sync_source='out/garden_bloom_lipsync_v2/synced.mp4',
         green_guide='Approved above-head conductor, garden_guide_conductor_v4/guide.py',
         source='out/garden_bloom_synced_v5/plate24.mp4',
         method='New verified synced plate timestamp-conformed to24fps; exact source66..134, original song-timed lantern response and approved above-head conductor rebuilt once.',
         status='owner_review_pending; weak_articulation_reported')
(OUT/'recipe.json').write_text(json.dumps(r,indent=2))
