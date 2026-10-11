import json
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import encode, load, probe, run, save

base = Path('projects/a-right-little-something').resolve()
out = base/'generated/storyboard/lab-verse-v02'
register = load(base/'shots/shotlist.json')
shots = [s for s in register['storyboardProposals'] if s.get('batch') == 'lab-verse-v02']
manifest = []
prompt_files = list(out.glob('*prompt*'))
for shot in shots:
    image = base/shot['startingFrameDraft']['image']
    assert image.stat().st_size > 0
    with Image.open(image) as im:
        shot['startingFrameDraft'].update(nativeWidth=im.width,nativeHeight=im.height)
    prompts = [p for p in prompt_files if shot['id'] in p.name]
    # Exterior worker stores a combined prompt manifest.
    prompt = ''
    for p in prompts:
        if p.suffix == '.txt':
            prompt = p.read_text(encoding='utf-8')
        elif p.suffix == '.json':
            v = load(p)
            if isinstance(v,dict):
                prompt = v.get('prompt','')
    if not prompt:
        for p in prompt_files:
            if p.suffix != '.json':
                continue
            value = load(p)
            values = value if isinstance(value,list) else value.get('shots',value.get('items',[]))
            for item in values:
                if item.get('id') == shot['id']:
                    prompt = item.get('prompt','')
    assert prompt and shot['promptLock'] in prompt, shot['id']
    shot['imagePrompt'] = prompt
    manifest.append(dict(id=shot['id'],src=Path(__import__('os').path.relpath(image,out)).as_posix(),href=Path(__import__('os').path.relpath(image,out)).as_posix(),
        title=f"{(shot['startFrame']-1)/24:.2f}s · {shot['title']} · Motion: {shot['motionDirection']}",
        prompt=prompt,route='Built-in ImageGen · draft still'))
save(base/'shots/shotlist.json',register)
save(out/'review-manifest.json',manifest)
save(out/'shot-directions.json',dict(promptLock=shots[0]['promptLock'],shots=shots))
renderer = Path('C:/Users/arneg/.codex/plugins/cache/openai-curated-remote/creative-production/0.1.25/scripts/review_renderer.py')
subprocess.run([sys.executable,str(renderer),'--out-dir',str(out),'--manifest',str(out/'review-manifest.json'),
    '--preset','detail-review','--show-captions'],check=True)

final = base/'generated/animatic/A-Right-Little-Something-selected-motion-v27.mp4'
source = base/'generated/animatic/A-Right-Little-Something-selected-motion-v26.mp4'
info = probe(final)
assert (int(info['nb_frames']),info['width'],info['height'],info['r_frame_rate']) == (5265,1920,1080,'24/1')
hashes = [subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0',
    '-c','copy','-f','hash','-hash','sha256','-']).decode().strip() for p in (source,final)]
assert hashes[0] == hashes[1]
# The review stops exactly at the next phrase, after the bright-night hold.
run(['-reinit_filter','0','-i',str(final),'-vf','trim=start_frame=0:end_frame=1957,setpts=N/(24*TB)',
    '-af','atrim=start=0:end=81.5416666667,asetpts=PTS-STARTPTS','-frames:v','1957',
    '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
    '-movflags','+faststart',str(out/'animatic-through-bright-night.mp4')])
assert int(probe(out/'animatic-through-bright-night.mp4')['nb_frames']) == 1957
frames = [1549,1554,1573,1610,1650,1715,1752,1785,1820,1850,1910,1957]
proof = out/'proof-frames'
proof.mkdir(exist_ok=True)
select = '+'.join(f'eq(n\\,{n-1})' for n in frames)
run(['-reinit_filter','0','-i',str(final),'-vf',f'select={select},scale=480:270',
    '-fps_mode','passthrough',str(proof/'%02d.png')])
sheet = Image.new('RGB',(1440,4*302),'#111111')
draw = ImageDraw.Draw(sheet)
for i,n in enumerate(frames):
    image = Image.open(proof/f'{i+1:02d}.png').convert('RGB')
    x,y = (i%3)*480,(i//3)*302
    sheet.paste(image,(x,y))
    draw.text((x+8,y+275),f'Frame {n} · {(n-1)/24:.2f}s',fill='white')
sheet.save(out/'animatic-proof.png')
register = load(base/'shots/shotlist.json')

for shot in register['storyboardProposals']:
    if shot.get('batch')=='lab-verse-v02':
        shot['continuityConstraints']='The chamber stays sealed. Human hands, forearms and virtual interfaces remain inside culture fluid behind uninterrupted upper glass. Robots and their physical controls remain outside. Do not introduce a human service port, cuff, hole or limb crossing the wall.'
    if shot.get('batch')=='lab-verse-v02' and shot['id'] not in ('lab2-03','lab2-04'):
        for key in ('startingFrameDraft','startingFrameSelection','animaticPlacement'):
            shot[key]['userSelected']=True
        for key in ('startingFrameDraft','startingFrameSelection'):
            shot[key]['status']='User accepted v26 still, retained in v27'
        shot['status']='User accepted v26 still, retained in v27'
register['reviewEdits']['v26']['userReview'] = 'User liked lab verse and submarine-like ark; requested hand/interface inside sealed tank on shots03/04, rest accepted.'
register['reviewEdits']['v27'].update(draftForReview=True,reviewUrl='http://127.0.0.1:8768/storyboard/lab-verse-v02/animatic-through-bright-night.mp4',
    extraKlingCredits=0,reviewEndFrameExclusive=1958)
save(base/'shots/shotlist.json',register)
project = load(base/'project.json')
project['production']['labVerseReview'] = register['reviewEdits']['v27']['reviewUrl']
save(base/'project.json',project)
save(out/'verification.json',dict(fullFrames=5265,reviewFrames=1957,newVerseFrames=408,
    fps=24,width=1920,height=1080,masterAudioHash=hashes[1],audioPreserved=True,
    imagery='Nine generated stills, native animation pending',cumulativeKlingCredits=1784,extraKlingCredits=0))
print('V27 verified; all prompts preserve identical lock; nine images present.')
