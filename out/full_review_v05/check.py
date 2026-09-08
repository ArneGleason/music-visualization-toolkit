import json
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
label = Image.new('RGBA', (345, 34), (0, 0, 0, 190))
draw = ImageDraw.Draw(label)
draw.text((10, 6), 'EARLIER DRAFT / REVISION PENDING',
          font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 17), fill=(255,218,160))
label.save(OUT/'legacy_label.png')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(OUT/'preview.mp4'),
    '-i',str(OUT/'legacy_label.png'),'-filter_complex',
    "[0:v][1:v]overlay=18:18:enable='gte(n,1082)'[v]",
    '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','19',
    '-c:a','copy','-frames:v','4782','-movflags','+faststart',str(OUT/'review.mp4')],check=True)
probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
    '-of','json',str(OUT/'review.mp4')]))
video = next(s for s in probe['streams'] if s['codec_type']=='video')
assert int(video['nb_frames']) == 4782 and video['avg_frame_rate']=='24/1'
assert (video['width'],video['height']) == (1280,720)
assert abs(float(video['start_time'])) < .001
def samples(path):
    return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
        '-ac','1','-ar','12000','-f','f32le','-']),dtype='<f4')
a=samples(ROOT/'audio/song.wav'); b=samples(OUT/'review.mp4')
n=min(len(a),len(b)); corr=float(np.corrcoef(a[:n],b[:n])[0,1])
assert corr > .99, corr
subprocess.run(['ffmpeg','-v','error','-i',str(OUT/'review.mp4'),'-f','null','-'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(OUT/'review.mp4'),'-vf',
    "select='eq(n,820)+eq(n,1070)+eq(n,1100)+eq(n,4140)',scale=640:360,tile=2x2",
    '-frames:v','1',str(OUT/'check.jpg')],check=True)
(OUT/'verification.json').write_text(json.dumps({'frames':4782,'fps':24,
    'master_zero_lag_correlation':corr,'decode':'passed','width':1280,'height':720,
    'legacy_label_start_frame':1082},indent=2))
print('Verified full review',corr)
