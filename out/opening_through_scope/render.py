"""Review existing opening and protected scope without editing production."""
import hashlib
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
shotlist = ROOT / 'shots/shotlist.json'
before = hashlib.sha256(shotlist.read_bytes()).hexdigest()
with (OUT / 'render.log').open('w') as log:
    subprocess.run([sys.executable, 'tools/blender_comp.py', '--proxy',
        '--start', '0', '--end', '154', '--out', str(OUT / 'raw.mp4')],
        cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(OUT / 'raw.mp4'),
    '-i', str(ROOT / 'audio/song.wav'), '-filter_complex',
    '[0:v]setpts=PTS-STARTPTS[v];[1:a]atrim=start=0:end=6.458333333333,asetpts=PTS-STARTPTS[a]',
    '-map', '[v]', '-map', '[a]', '-frames:v', '155', '-c:v', 'libx264',
    '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
    '-b:a', '256k', '-movflags', '+faststart', str(OUT / 'preview.mp4')], check=True)
assert before == hashlib.sha256(shotlist.read_bytes()).hexdigest()
print('Rendered 155 frames; production shotlist unchanged.')
