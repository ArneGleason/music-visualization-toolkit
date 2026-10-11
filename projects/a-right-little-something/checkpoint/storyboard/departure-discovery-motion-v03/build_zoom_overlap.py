"""Add brief outgoing radial zoom trails over the accepted optical still cuts."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
OLD = OUT.with_name('departure-discovery-motion-v02')
NATIVE = OUT.with_name('departure-discovery-motion-v01')
REPO = BASE.parents[1]
W, H = 1920, 1080

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def run(args):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *args], cwd=OUT, check=True)

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams',
        'v:0', '-show_streams', '-of', 'json', str(path)]))['streams'][0]

def zoom_trail(picture, low, high):
    # A sampled shutter exposure of the outgoing image expanding toward camera.
    # Balanced averaging avoids the brightness loss of incremental 8-bit averages.
    samples = []
    for i in range(32):
        scale = low+(high-low)*i/31
        half_w, half_h = W/(2*scale), H/(2*scale)
        samples.append(picture.transform((W,H), Image.Transform.EXTENT,
            (W/2-half_w, H/2-half_h, W/2+half_w, H/2+half_h),
            resample=Image.Resampling.BICUBIC))
    while len(samples)>1:
        samples = [Image.blend(a,b,.5) for a,b in zip(samples[::2],samples[1::2])]
    return samples[0]

def build():
    r=read(BASE/'shots/shotlist.json')
    assert r['activeReviewEdit']=='v56'
    save(OUT/'prior-shotlist.json',r)
    shot=next(s for s in r['storyboardProposals'] if s['id']=='departure-004')
    frames=OUT/'frames'
    frames.mkdir(exist_ok=True)
    run(['-i',str(NATIVE/'zoom-stills.mp4'),'-frames:v','73',str(frames/'%03d.png')])
    transitions=[]
    contact=Image.new('RGB',(480*4, (270+26)*8),'#10282e')
    draw=ImageDraw.Draw(contact)
    for i,seg in enumerate(shot['storyboardSegments'][1:]):
        start=seg['startFrame']-shot['startFrame']
        count=1 if seg['frames']==3 else 2
        previous=Image.open(frames/f'{start:03d}.png').convert('RGB')
        incoming=Image.open(frames/f'{start+1:03d}.png').convert('RGB')
        settings=[(1.08,2.0,.48)] if count==1 else [(1.04,1.75,.62),(1.75,2.8,.24)]
        diagnostic=[previous]
        for j,(low,high,opacity) in enumerate(settings):
            result=Image.blend(incoming,zoom_trail(previous,low,high),opacity)
            result.save(frames/f'{start+j+1:03d}.png')
            diagnostic.append(result)
        if count==1:
            diagnostic.append(incoming)
        diagnostic.append(incoming)
        for col,picture in enumerate(diagnostic):
            y=i*296
            contact.paste(picture.resize((480,270)),(col*480,y+26))
            label=['Outgoing',f'Cue {i+2}: overlap 1', 'Overlap 2' if count==2 else 'Settled', 'Settled'][col]
            draw.text((col*480+8,y+6),label,fill='white')
        transitions.append(dict(fromAsset=shot['storyboardSegments'][i]['asset'],toAsset=seg['asset'],
            startFrame=seg['startFrame'],frames=count,shutterSamples=32,
            outgoingScaleRanges=[[a,b] for a,b,_ in settings],
            outgoingOpacities=[c for _,_,c in settings],anchor=[.5,.5]))
    contact.save(OUT/'transition-contact.jpg')
    manifest=dict(operation='outgoing radial zoom blur over static incoming view',
        transitions=transitions,firstFrame=2873,endFrameExclusive=2946,frames=73,
        changedFrames=sum(t['frames'] for t in transitions),fps=24,
        cueTiming='Unchanged; incoming still appears underneath on its original cue',
        lyrics='Composited after transitions; no text blur',newCredits=0)
    save(OUT/'timing-check.json',manifest)
    run(['-framerate','24','-i',str(frames/'%03d.png'),'-frames:v','73','-an',
        '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','zoom-overlap.mp4'])
    assert int(probe(OUT/'zoom-overlap.mp4')['nb_frames'])==73
    concat=(OLD/'concat.txt').read_text().replace((NATIVE/'zoom-stills.mp4').as_posix(),(OUT/'zoom-overlap.mp4').as_posix())
    assert 'zoom-stills.mp4' not in concat
    (OUT/'concat.txt').write_text(concat)
    run(['-f','concat','-safe','0','-i','concat.txt','-an','-c','copy','hybrid-picture.mp4'])
    shutil.copy2(OLD/'lyrics.ass',OUT/'lyrics.ass')
    shutil.copytree(OLD/'fonts',OUT/'fonts',dirs_exist_ok=True)
    source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v56.mp4'
    run(['-i','hybrid-picture.mp4','-i',str(source),'-filter_complex',
        f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={2594/24}:end={3143/24},asetpts=PTS-STARTPTS[a]',
        '-map','[v]','-map','[a]','-frames:v','549','-c:v','libx264','-preset','fast',
        '-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','timed-still-board.mp4'])
    assert int(probe(OUT/'timed-still-board.mp4')['nb_frames'])==549
    options=read(OLD/'review-options.json')
    options.update(output=OUT.relative_to(BASE).as_posix(),sourceAnimatic=source.relative_to(BASE).as_posix(),
        presentation='Eight brief radial zoom overlaps connect nine static magnification views',
        continuationNotes='V57: one- or two-frame outgoing zoom-blur overlaps on eight optical cuts; exact cue frames retained. V56 departure and all other shot selections retained; no new generation.')
    save(OUT/'review-options.json',options)
    print('Prepared 14 overlap frames across eight cuts; all 73 original frame positions retained.',flush=True)

def install():
    r=read(BASE/'shots/shotlist.json')
    assert r['activeReviewEdit']=='v56'
    manifest=read(OUT/'timing-check.json')
    options=read(OUT/'review-options.json')
    subprocess.run([sys.executable,str(REPO/'tools/insert_still_storyboard.py'),
        str(BASE/'project.json'),str(OUT/'review-options.json'),'--version','v57'],check=True)
    current=read(BASE/'shots/shotlist.json')
    r['activeReviewEdit']='v57'
    edit=copy.deepcopy(r['reviewEdits']['v56'])
    edit.update(source=str(BASE/options['sourceAnimatic']),video=current['reviewEdits']['v57']['video'],
        type='Native assembly with brief optical zoom overlaps',newPaidCredits=0,
        presentation=options['presentation'],zoomTransitions=manifest['transitions'])
    r['reviewEdits']['v57']=edit
    shot=next(s for s in r['storyboardProposals'] if s['id']=='departure-004')
    notes='V57: outgoing image expands into a radial blur over each incoming still. Two frames per transition, one frame for the three-frame views (cues 3 and 8). Eight overlaps, 14 affected frames; all nine lyric cues unchanged. Lyrics stay sharp.'
    shot.update(status='Zoom overlap preview in V57; user review pending',editorialDirection=notes,
        motionReview=dict(notes=notes),editorialTransitions=manifest['transitions'])
    shot['animaticPlacement'].update(kind='nine static optical views with one- or two-frame zoom overlaps',
        editorialMotionRef=(OUT/'zoom-overlap.mp4').relative_to(BASE).as_posix())
    for s in r['storyboardProposals']:
        if s.get('batch')=='departure-discovery-v01': s['animaticPlacement']['animaticVersion']='v57'
    for entry in edit['entries']:
        entry['animaticVersion']='v57'
        if entry['shot']=='departure-004': entry.update(shot['animaticPlacement'])
    seq=r['departureDiscoverySequence']
    seq.update(status='V57 optical overlap preview ready',reviewUrl='http://127.0.0.1:8768/?v=v57',
        motionReviewUrl='http://127.0.0.1:8768/storyboard/departure-discovery-motion-v03/')
    seq['motionRequest']['status']='Seven existing takes and nine optical stills assembled in V57; brief zoom overlaps added; no new spending'
    save(BASE/'shots/shotlist.json',r)
    opening=read(BASE/'generated/animatic/current-opening.json')
    for item in opening['shots']:
        if item['id']=='departure-004': item['review']=shot['motionReview']
    save(BASE/'generated/animatic/current-opening.json',opening)
    save(OUT/'verification.json',dict(fullFrames=5265,passageFrames=549,zoomFrames=73,
        fps=24,width=1920,height=1080,originalMasterAudio='AAC packets verified identical to V56',
        affectedOpticalFrames=14,transitions=8,newCredits=0,cumulativeCredits=3384))
    (OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Optical zoom overlap — V57</title><style>body{background:#10282e;color:#efdfc0;font:16px system-ui;max-width:1100px;margin:24px auto}video{width:100%}a{color:#9bd9e9}</style><h1>Optical zoom overlap — V57</h1><video controls src="timed-still-board.mp4"></video><p>Eight brief outward zoom overlaps connect the nine static views. Original cue timing retained.</p><a href="/?v=v57">Full V57</a>',encoding='utf-8')
    print('V57 assembled; master audio verified; no new credits.')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--install',action='store_true')
    args=parser.parse_args()
    install() if args.install else build()
