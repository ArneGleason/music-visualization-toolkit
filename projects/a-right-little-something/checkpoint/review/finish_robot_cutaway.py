from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path('tools').resolve()))
from build_chorus_revision import load, probe, run, save

base = Path('projects/a-right-little-something').resolve()
out = base/'generated/storyboard/lab-robot-cutaway-v01'
source = base/'generated/animatic/A-Right-Little-Something-selected-motion-v30.mp4'
final = base/'generated/animatic/A-Right-Little-Something-selected-motion-v31.mp4'
info = probe(final)
assert (int(info['nb_frames']),info['width'],info['height'],info['r_frame_rate']) == (5265,1920,1080,'24/1')
hashes = [subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip() for p in (source,final)]
assert hashes[0] == hashes[1]
for name,a,b in [('animatic-through-bright-night',0,1957),('robot-cutaway-in-context',1595,1742)]:
    run(['-reinit_filter','0','-i',str(final),'-vf',f'trim=start_frame={a}:end_frame={b},setpts=N/(24*TB)',
        '-af',f'atrim=start={a/24}:end={b/24},asetpts=PTS-STARTPTS','-frames:v',str(b-a),
        '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
        '-movflags','+faststart',str(out/(name+'.mp4'))])
    assert int(probe(out/(name+'.mp4'))['nb_frames']) == b-a
frames = [1610,1630,1660,1690,1710,1735]
proof = out/'proof-frames'
proof.mkdir(exist_ok=True)
select = '+'.join(f'eq(n\\,{n-1})' for n in frames)
run(['-reinit_filter','0','-i',str(final),'-vf',f'select={select},scale=640:360','-fps_mode','passthrough',str(proof/'%02d.png')])
sheet = Image.new('RGB',(1920,2*392),'#111111')
draw = ImageDraw.Draw(sheet)
for i,n in enumerate(frames):
    x,y = (i%3)*640,(i//3)*392
    sheet.paste(Image.open(proof/f'{i+1:02d}.png').convert('RGB'),(x,y))
    draw.text((x+8,y+365),f'Frame {n} · {(n-1)/24:.2f}s',fill='white')
sheet.save(out/'animatic-proof.png')
register = load(base/'shots/shotlist.json')
shots = [s for s in register['storyboardProposals'] if s.get('batch') == 'lab-robot-cutaway-v01']
assert len(shots) == 9 and len({s['promptLock'] for s in shots}) == 1
replacement = next(s for s in shots if s['id'] == 'lab2-03')
assert replacement['animaticPlacement']['kind'] == 'still with editorial pan'
assert replacement['startFrame'] == 1624 and replacement['endFrameExclusive'] == 1698
register['reviewEdits']['v31'].update(draftForReview=True,type='Robot-only replacement still preview',
    nativeLabAndArkShots=8,pendingReplacement='lab2-03',
    reviewUrl='http://127.0.0.1:8768/storyboard/lab-robot-cutaway-v01/animatic-through-bright-night.mp4')
save(base/'shots/shotlist.json',register)
project = load(base/'project.json')
project['production']['labVerseReview'] = register['reviewEdits']['v31']['reviewUrl']
save(base/'project.json',project)
save(out/'shot-directions.json',dict(promptLock=shots[0]['promptLock'],shots=shots))
save(out/'verification.json',dict(fullFrames=5265,reviewFrames=1957,fps=24,width=1920,height=1080,
    masterAudioHash=hashes[1],audioPreserved=True,replacementFrames=74,replacementStartFrame=1624,
    replacementEndFrameExclusive=1698,nativeLabAndArkShots=8,newCredits=0,cumulativeConfirmedCredits=2216,
    replacementMotionStatus='Prepared, not submitted; reviewed-source and 48-credit approval pending'))
print('V31 verified: robot cutaway still,74 exact frames,original audio preserved,no new Kling charge.')
