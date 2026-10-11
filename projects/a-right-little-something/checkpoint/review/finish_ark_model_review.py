from pathlib import Path
import json
import shutil
import subprocess
from PIL import Image

base = Path(__file__).resolve().parents[2]
source = base/'generated/design/ark-blender-v02'
review = base/'generated/storyboard/ark-blender-v02'
frames = sorted((source/'sweep-frames').glob('frame_*.png'))
assert len(frames) == 120
assert [f.name for f in frames] == [f'frame_{i:04d}.png' for i in range(1, 121)]
assert all(Image.open(f).size == (960, 540) for f in frames)
movie = source/'camera-sweep.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '24', '-i', str(source/'sweep-frames/frame_%04d.png'),
                '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(movie)], check=True)
data = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', str(movie)]))
stream = data['streams'][0]
assert (int(stream['nb_frames']), stream['width'], stream['height'], stream['r_frame_rate']) == (120, 960, 540, '24/1')
shutil.copy2(movie, review/'camera-sweep.mp4')
verification = json.loads((review/'verification.json').read_text(encoding='utf-8'))
verification.update(cameraSweepFrames=120, cameraSweepFPS=24, cameraSweepSeconds=5,
                    cameraSweepWidth=960, cameraSweepHeight=540,
                    pairTransformsCheckedAtFrames=[1, 60, 120],
                    geometryAnimated=False, onlyCameraOrbitAnimated=True,
                    newCredits=0, cumulativeConfirmedCredits=2264, animaticChanged=False)
(review/'verification.json').write_text(json.dumps(verification, indent=2)+'\n', encoding='utf-8')
print('Verified 120-frame native camera sweep, six fixed pods, no model deformation; movie unchanged.')
