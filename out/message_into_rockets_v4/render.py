"""Replace only orbital s035 with the returned matching-rocket take two."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
OLD = ROOT / 'out/message_into_rockets_v3'
def run(args, **kwargs):
    subprocess.run([str(x) for x in args], cwd=ROOT, check=True, **kwargs)
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames,start_time','-of','json',str(path)]))['streams'][0]

h = json.loads((ROOT / 'out/orbital_continuity_v1/handoff.json').read_text())
t = h['claude_result']['take2']
for item in list(h['inputs'].values()) + [t['base'], t['original'], h['approved_landing']['source']]:
    assert hashlib.sha256((ROOT / item['file']).read_bytes()).hexdigest() == item['sha256']
base = ROOT / t['base']['file']
p = probe(base)
assert p['r_frame_rate'] == '24/1' and int(p['nb_frames']) == 192 and float(p['start_time']) == 0
run(['ffmpeg','-v','error','-i',base,'-f','null','-'])
edl = json.loads((OLD / 'shotlist.json').read_text())
original = json.loads((OLD / 'shotlist.json').read_text())
s = next(s for s in edl['shots'] if s['id'] == 's035')
assert round(s['start_sec']*24) == 2881 and round(s['end_sec']*24) == 2928 and s['frames'] == 47
s['clip'] = {'file':t['base']['file'], 'in_sec':12/24, 'speed':1}
assert all(a == b for a,b in zip(edl['shots'],original['shots']) if a['id'] != 's035')
(OUT / 'shotlist.json').write_text(json.dumps(edl,indent=2))
(OUT / 'overlay_cues.json').write_bytes((OLD / 'overlay_cues.json').read_bytes())
adapter = (ROOT / 'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"message_into_rockets_v4"')
(OUT / 'blender_review.py').write_text(adapter)
with (OUT / 'assembly.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','2786','--end','3026','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={2786/24}:end={3027/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','241','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
q = probe(OUT/'preview.mp4')
assert int(q['nb_frames']) == 241 and q['r_frame_rate'] == '24/1'
(OUT/'verification.json').write_text(json.dumps({'input_hashes_verified':True,'source_probe':p,'preview_probe':q,'preview_song_frames':[2786,3027],'orbital_source':t['base'],'orbital_song_frames':[2881,2928],'orbital_source_frames':[12,59],'only_s035_clip_changed':True,'landing_and_fx_unchanged':True,'status':'rendered for owner review; no production merge'},indent=2))
print('Preview ready: 241 frames, only orbital source changed.',flush=True)
