from pathlib import Path
import json, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import probe

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/chorus-revision-v04'
final=base/'generated/animatic/A-Right-Little-Something-selected-motion-v24.mp4'
source=base/'generated/animatic/A-Right-Little-Something-selected-motion-v23.mp4'
info=probe(final)
assert (info['nb_frames'],info['width'],info['height'],info['r_frame_rate'])==('5265',1920,1080,'24/1')
assert probe(out/'fade-review.mp4')['nb_frames']=='813'
def audio_hash(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
master=audio_hash(final)
assert master==audio_hash(source)
frames=(849,854,859,875,889,903,907,912,917)
selection='+'.join(f'eq(n\\,{frame-1})' for frame in frames)
subprocess.run(['ffmpeg','-y','-v','error','-reinit_filter','0','-i',str(final),'-vf','select='+selection,'-fps_mode','passthrough','-frames:v',str(len(frames)),str(out/'qa-%02d.png')],check=True)
sheet=Image.new('RGB',(1440,810),(10,14,22))
for i,frame in enumerate(frames):
    target=out/f'proof-{frame:04}.png'
    (out/f'qa-{i+1:02d}.png').replace(target)
    image=Image.open(target).resize((480,270))
    sheet.paste(image,((i%3)*480,(i//3)*270))
    ImageDraw.Draw(sheet).text(((i%3)*480+8,(i//3)*270+8),f'Song frame {frame}',fill='white',stroke_width=1,stroke_fill='black')
sheet.save(out/'v24-proof.png')
q=base/'generated/review/chorus-revision-v04-ledger.json'
d=json.loads(q.read_text(encoding='utf-8'))
d['verification'].update(status='Technical checks passed; full-film source proof ready for visual inspection',fullSong={k:info[k] for k in ('width','height','r_frame_rate','nb_frames')},masterAudioHash=master,previewFrames=813,pictureQAFrames=list(frames))
q.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('V24: 5265 frames at 24fps, 1920x1080; original master audio unchanged; scale-reveal proof ready')
