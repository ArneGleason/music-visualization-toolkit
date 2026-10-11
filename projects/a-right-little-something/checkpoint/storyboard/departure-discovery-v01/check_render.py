"""Inspect exact edited cut frames, including the magnification ladder."""
from pathlib import Path
import io
import subprocess
from PIL import Image, ImageDraw

out = Path(__file__).resolve().parent
video = out.parents[1] / 'animatic/A-Right-Little-Something-selected-motion-v51.mp4'
frames = [2595,2665,2759,2805,2873,2887,2891,2894,2899,2903,2908,2912,2915,2945,2946,2994,3039,3081]
sheet = Image.new('RGB',(1280,6*205),'#171d28')
draw = ImageDraw.Draw(sheet)
for index, frame in enumerate(frames):
    data = subprocess.check_output(['ffmpeg','-v','error','-ss',str((frame-1)/24),'-i',str(video),'-frames:v','1','-vf','scale=400:225','-f','image2pipe','-vcodec','png','-'])
    with Image.open(io.BytesIO(data)) as im:
        im.thumbnail((410,180))
        x,y = (index%3)*426,(index//3)*205
        sheet.paste(im,(x,y))
        draw.text((x+5,y+183),f'Frame {frame} / {(frame-1)/24:.3f}s',fill='white')
sheet.save(out/'render-qa.jpg')
print('Saved 18 exact rendered frame samples')
