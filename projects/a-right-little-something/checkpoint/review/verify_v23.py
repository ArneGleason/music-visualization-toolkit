from pathlib import Path
import json, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import probe

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/chorus-revision-v03'
final=base/'generated/animatic/A-Right-Little-Something-selected-motion-v23.mp4'
source=base/'generated/animatic/A-Right-Little-Something-selected-motion-v22.mp4'
info=probe(final)
assert (info['nb_frames'],info['width'],info['height'],info['r_frame_rate'])==('5265',1920,1080,'24/1')
assert probe(out/'fade-review.mp4')['nb_frames']=='813'
def audio_hash(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
master=audio_hash(final)
assert master==audio_hash(source)
frames=(784,789,794,849,854,859,907,912,917,1041,1046,1051,1430,1465,1500,1530,1544,1549)
sheet=Image.new('RGB',(1440,1620),(10,14,22))
selection='+'.join(f'eq(n\\,{frame-1})' for frame in frames)
# Decode the film once, with a continuous counter across color-metadata changes.
subprocess.run(['ffmpeg','-y','-v','error','-reinit_filter','0','-i',str(final),
                '-vf','select='+selection,'-fps_mode','passthrough','-frames:v',str(len(frames)),str(out/'qa-%02d.png')],check=True)
for i,frame in enumerate(frames):
    target=out/f'proof-{frame:04}.png'
    (out/f'qa-{i+1:02d}.png').replace(target)
    image=Image.open(target).resize((480,270))
    sheet.paste(image,((i%3)*480,(i//3)*270))
    ImageDraw.Draw(sheet).text(((i%3)*480+8,(i//3)*270+8),f'Song frame {frame}',fill='white',stroke_width=1,stroke_fill='black')
sheet.save(out/'v23-proof.png')
ledger_path=base/'generated/review/chorus-revision-v03-ledger.json'
ledger=json.loads(ledger_path.read_text())
ledger['verification'].update(status='Technical checks passed; composite proof sheet ready for visual inspection',fullSong=info,masterAudioHash=master,pictureQAFrames=list(frames))
ledger_path.write_text(json.dumps(ledger,indent=2)+'\n')
print('V23: 5265 frames; 24fps; 1920x1080; 813-frame preview; exact master audio; proof sheet ready')
