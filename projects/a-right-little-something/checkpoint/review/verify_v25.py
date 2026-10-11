from pathlib import Path
import json, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import probe

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/chorus-revision-v05'
final=base/'generated/animatic/A-Right-Little-Something-selected-motion-v25.mp4'
source=base/'generated/animatic/A-Right-Little-Something-selected-motion-v24.mp4'
info=probe(final)
assert (info['nb_frames'],info['width'],info['height'],info['r_frame_rate'])==('5265',1920,1080,'24/1')
assert probe(out/'fade-review.mp4')['nb_frames']=='813'
def audio_hash(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
master=audio_hash(final)
assert master==audio_hash(source)
subprocess.run(['ffmpeg','-y','-v','error','-reinit_filter','0','-i',str(final),
                '-filter_complex','[0:v]trim=start_frame=1411:end_frame=1549,setpts=N/(24*TB)[v];[0:a]atrim=start=58.7916666667:end=64.5416666667,asetpts=PTS-STARTPTS[a]',
                '-map','[v]','-map','[a]','-frames:v','138','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'orbit-review.mp4')],check=True)
assert probe(out/'orbit-review.mp4')['nb_frames']=='138'
frames=(1412,1417,1430,1450,1470,1485,1500,1515,1535,1544,1549,1550)
selection='+'.join(f'eq(n\\,{frame-1})' for frame in frames)
subprocess.run(['ffmpeg','-y','-v','error','-reinit_filter','0','-i',str(final),'-vf','select='+selection,'-fps_mode','passthrough','-frames:v',str(len(frames)),str(out/'qa-%02d.png')],check=True)
sheet=Image.new('RGB',(1440,1080),(10,14,22))
for i,frame in enumerate(frames):
    target=out/f'proof-{frame:04}.png'
    (out/f'qa-{i+1:02d}.png').replace(target)
    image=Image.open(target).resize((480,270))
    sheet.paste(image,((i%3)*480,(i//3)*270))
    ImageDraw.Draw(sheet).text(((i%3)*480+8,(i//3)*270+8),f'Song frame {frame}',fill='white',stroke_width=1,stroke_fill='black')
sheet.save(out/'v25-proof.png')
q=base/'generated/review/chorus-revision-v05-ledger.json'
d=json.loads(q.read_text(encoding='utf-8'))
native=base/'generated/storyboard/orbit-blender-v03/hybrid'
d['verification'].update(status='Full-film technical checks passed; visual proof ready',fullSong={k:info[k] for k in ('width','height','r_frame_rate','nb_frames')},masterAudioHash=master,previewFrames=813,pictureQAFrames=list(frames),nativeMotion=json.loads((native/'native-motion-check.json').read_text(encoding='utf-8')),velocityChecks=json.loads((native/'velocity-check.json').read_text(encoding='utf-8')))
q.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('V25: 5265 frames at 24fps, 1920x1080; exact master audio; native blur and variable speed verified; proof ready')
