from pathlib import Path
import subprocess
import sys
from PIL import Image,ImageDraw

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,probe,run,save

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/lab-silver-v01'
source=base/'generated/animatic/A-Right-Little-Something-selected-motion-v28.mp4'
final=base/'generated/animatic/A-Right-Little-Something-selected-motion-v29.mp4'
info=probe(final)
assert (int(info['nb_frames']),info['width'],info['height'],info['r_frame_rate'])==(5265,1920,1080,'24/1')
hashes=[subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip() for p in (source,final)]
assert hashes[0]==hashes[1]
for name,a,b in [('animatic-through-bright-night',0,1957),('spacecraft-passage',1761,1957)]:
    run(['-reinit_filter','0','-i',str(final),'-vf',f'trim=start_frame={a}:end_frame={b},setpts=N/(24*TB)',
        '-af',f'atrim=start={a/24}:end={b/24},asetpts=PTS-STARTPTS','-frames:v',str(b-a),
        '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
        '-movflags','+faststart',str(out/(name+'.mp4'))])
    assert int(probe(out/(name+'.mp4'))['nb_frames'])==b-a
frames=[1573,1610,1650,1715,1752,1785,1820,1840,1850,1867,1910,1957]
proof=out/'proof-frames'
proof.mkdir(exist_ok=True)
select='+'.join(f'eq(n\\,{n-1})' for n in frames)
run(['-reinit_filter','0','-i',str(final),'-vf',f'select={select},scale=480:270',
     '-fps_mode','passthrough',str(proof/'%02d.png')])
sheet=Image.new('RGB',(1920,3*302),'#111111')
draw=ImageDraw.Draw(sheet)
for i,n in enumerate(frames):
    x,y=(i%4)*480,(i//4)*302
    sheet.paste(Image.open(proof/f'{i+1:02d}.png').convert('RGB'),(x,y))
    draw.text((x+8,y+275),f'Frame{n} · {(n-1)/24:.2f}s',fill='white')
sheet.save(out/'animatic-proof.png')
register=load(base/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='lab-silver-v01']
save(out/'shot-directions.json',dict(promptLock=shots[0]['promptLock'],shots=shots))
manifest=[]
for shot in shots[:5]:
    manifest.append(dict(src=shot['id']+'.png',title=shot['title']+' · '+shot['motionDirection'],
                         prompt=shot['imagePrompt'],route='Built-in ImageGen silver wardrobe edit'))
save(out/'review-manifest.json',manifest)
renderer='C:/Users/arneg/.codex/plugins/cache/openai-curated-remote/creative-production/0.1.25/scripts/review_renderer.py'
subprocess.run([sys.executable,renderer,'--out-dir',str(out),'--manifest',str(out/'review-manifest.json'),'--preset','detail-review'],check=True)
register['reviewEdits']['v29'].update(draftForReview=True,newNativeShots=4,wardrobeStillDrafts=5,
    reviewUrl='http://127.0.0.1:8768/storyboard/lab-silver-v01/animatic-through-bright-night.mp4')
save(base/'shots/shotlist.json',register)
project=load(base/'project.json')
project['production']['labVerseReview']=register['reviewEdits']['v29']['reviewUrl']
save(base/'project.json',project)
save(out/'verification.json',dict(fullFrames=5265,reviewFrames=1957,fps=24,width=1920,height=1080,
    masterAudioHash=hashes[1],audioPreserved=True,newNativeShots=4,wardrobeStillDrafts=5,
    confirmedNewCredits=192,cumulativeConfirmedCredits=1976,pendingJobs=[]))
print('V29 ready; silver wardrobe stills +4native ark clips; master audio/grid verified.')
