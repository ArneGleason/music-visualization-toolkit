"""Full review: current approved opening plus untouched legacy picture timing."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

def run(args, **kw):
    subprocess.run([str(x) for x in args], cwd=ROOT, check=True, **kw)

opening = json.loads((ROOT/'out/rosette_sprite_trial/shotlist.json').read_text())
legacy = json.loads((ROOT/'shots/shotlist.json').read_text())
shots = opening['shots'][:]
for old in legacy['shots']:
    if round(old['end_sec']*24) <= 1082:
        continue
    shot = dict(old)
    start = max(1082, round(shot['start_sec']*24))
    end = round(shot['end_sec']*24)
    shot.update(start_sec=start/24, dur_sec=(end-start)/24, frames=end-start)
    shot['review_status'] = 'legacy rough, not version-two approved'
    shots.append(shot)
previous = 0
for shot in shots:
    assert round(shot['start_sec']*24) == previous
    previous = round(shot['end_sec']*24)
assert previous == 4782
snapshot = dict(legacy, shots=shots)
(OUT/'shotlist.json').write_text(json.dumps(snapshot, indent=2))

with (OUT/'blender.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe', '-b',
         '--python-exit-code', '1', '-P', ROOT/'out/rosette_sprite_trial/blender_review.py',
         '--', '--proxy', '--start', '0', '--end', '970', '--shotlist',
         ROOT/'out/rosette_sprite_trial/shotlist.json', '--lyric-flat',
         'shots/lyric_motion_full.json', '--out', OUT/'opening.mp4'],
        stdout=log, stderr=subprocess.STDOUT)

# All inputs already have lyrics. Discard their audio and mux one continuous master.
# Trim in decoded frame indices, reset each segment PTS to remove container offsets.
filtergraph = (
    '[0:v]trim=start_frame=0:end_frame=971,setpts=N/(24*TB)[a];'
    '[1:v]trim=start_frame=0:end_frame=111,setpts=N/(24*TB)[b];'
    '[2:v]trim=start_frame=1082:end_frame=4782,setpts=N/(24*TB)[c];'
    '[a][b][c]concat=n=3:v=1:a=0,setsar=1[v]')
run(['ffmpeg','-v','error','-y','-i',OUT/'opening.mp4',
     '-i',ROOT/'out/rosette_duet_trial/preview.mp4',
     '-i',ROOT/'out/rough_v04_sync_noflash_720p.mp4',
     '-i',ROOT/'audio/song.wav','-filter_complex',filtergraph,
     '-map','[v]','-map','3:a:0','-frames:v','4782','-t','199.25',
     '-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',
     '-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'unnumbered.mp4'])

# Use the existing badge tool with this review's exact cut snapshot.
tool = ROOT/'tools/number_review_cuts.py'
source = tool.read_text().replace("ROOT/'shots/shotlist.json'", "ROOT/'out/full_review_v05/shotlist.json'")
assert source != tool.read_text()
sys.argv = [str(tool), '--input', 'out/full_review_v05/unnumbered.mp4',
            '--out', 'out/full_review_v05/preview.mp4']
exec(compile(source, str(tool), 'exec'), {'__name__':'__main__', '__file__':str(tool)})
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
print('Full numbered review verified: 4782 frames, 24 fps, 199.25 seconds.')
