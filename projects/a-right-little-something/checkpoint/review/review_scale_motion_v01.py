from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/kling-tests/scale-motion-v01/scale-reveal-motion-v01'
movie=out/'scale-reveal-motion-v01-01-clean.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)]))
video=next(s for s in probe['streams'] if s['codec_type']=='video')
assert video['r_frame_rate']=='24/1'
assert video['height']==1080
assert int(video['nb_frames'])>=106
frames=(1,25,55,82,110,145)
selection='+'.join(f'eq(n\\,{f-1})' for f in frames)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(movie),'-vf','select='+selection,'-fps_mode','passthrough','-frames:v',str(len(frames)),str(out/'qa-%02d.png')],check=True)
sheet=Image.new('RGB',(1440,540),(10,14,22))
for i,frame in enumerate(frames):
    target=out/f'source-{frame:04}.png'
    (out/f'qa-{i+1:02d}.png').replace(target)
    picture=Image.open(target).resize((480,270))
    sheet.paste(picture,((i%3)*480,(i//3)*270))
    ImageDraw.Draw(sheet).text(((i%3)*480+10,(i//3)*270+10),f'Source frame {frame}',fill='white',stroke_width=1,stroke_fill='black')
sheet.save(out/'source-proof.png')
(out/'media-probe.json').write_text(json.dumps(probe,indent=2)+'\n',encoding='utf-8')
print('Native source:',video['nb_frames'],'frames;',video['width'],'x',video['height'],'at',video['r_frame_rate'])
