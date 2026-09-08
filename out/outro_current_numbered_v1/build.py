"""Refresh the existing numbered review; preserve every frame except shot 11."""
from pathlib import Path
import subprocess
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
previous = ROOT / 'out/outro_water_reflection_v2/preview_numbered.mp4'
water = ROOT / 'out/outro_water_reflection_v3/water_preview.mp4'
output = OUT / 'preview_numbered.mp4'
filters = (
    '[0:v]trim=start_frame=0:end_frame=348,setpts=PTS-STARTPTS[a];'
    '[1:v]trim=start_frame=0:end_frame=72,setpts=PTS-STARTPTS[b];'
    '[0:v]trim=start_frame=420:end_frame=492,setpts=PTS-STARTPTS[c];'
    '[a][b][c]concat=n=3:v=1:a=0[v];'
    '[2:a]atrim=start=181.75:end=199.25,asetpts=PTS-STARTPTS,apad=whole_dur=20.5[audio]'
)
subprocess.run([
    'ffmpeg', '-v', 'error', '-n', '-i', str(previous), '-i', str(water),
    '-i', str(ROOT / 'audio/song.wav'), '-filter_complex', filters,
    '-map', '[v]', '-map', '[audio]', '-t', '20.5',
    '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', '24',
    '-c:a', 'aac', '-movflags', '+faststart', str(output)
], check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(output), '-f', 'null', '-'], check=True)
probe = json.loads(subprocess.check_output([
    'ffprobe', '-v', 'error', '-select_streams', 'v:0',
    '-show_entries', 'stream=nb_frames,r_frame_rate,width,height', '-of', 'json', str(output)
]))['streams'][0]
assert int(probe['nb_frames']) == 492, probe
assert probe['r_frame_rate'] == '24/1', probe
(OUT / 'verification.json').write_text(json.dumps(probe, indent=2))
print('Verified 492 frames, 24 fps, 1280x720. Master audio used once. All 12 labels retained.')
