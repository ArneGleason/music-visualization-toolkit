"""Validate collected takes, trim exact source frames, and make motion QA sheets."""
import argparse
import json
from pathlib import Path
import subprocess
import time
from PIL import Image, ImageDraw

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--available',action='store_true')
args=parser.parse_args()
plan=json.loads((BASE/'kling-first-contact-motion-v01.json').read_text(encoding='utf-8'))
overrides_path=OUT/'selection-overrides.json'
overrides=json.loads(overrides_path.read_text(encoding='utf-8')) if overrides_path.exists() else {}
(OUT/'edits').mkdir(exist_ok=True)
(OUT/'qa').mkdir(exist_ok=True)


def run(args):
    subprocess.run(['ffmpeg','-y','-v','error',*args],check=True)


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
        '-show_streams','-of','json',str(path)]))['streams'][0]


manifest=[]
for original in plan['shots']:
    shot=original
    source_plan='kling-first-contact-motion-v01.json'
    source_output=plan['output']
    if original['id'] in overrides:
        override=overrides[original['id']]
        source_plan=override['plan']
        alternate=json.loads((BASE/source_plan).read_text(encoding='utf-8'))
        shot=next(s for s in alternate['shots'] if s['id']==override['take'])
        source_output=alternate['output']
    folder=BASE/source_output/shot['id']
    raw=folder/(shot['id']+'-01-clean.mp4')
    if not raw.exists() and args.available:
        continue
    assert raw.is_file(), raw
    if args.available and time.time()-raw.stat().st_mtime<10:
        continue
    info=probe(raw)
    assert info['height']==1080 and 1900<=info['width']<=1920, info
    assert info['r_frame_rate']=='24/1', info
    count=int(info['nb_frames'])
    lead,length=shot.get('sourceEditStartFrame',25)-1,shot['editFrames']
    assert count>=lead+length+24, (shot['id'],count,lead,length)
    suffix=f'-source{lead+1}' if lead!=24 else ''
    edit=OUT/'edits'/(shot['id']+suffix+'.mp4')
    if not edit.exists():
        run(['-i',str(raw),'-vf',f'trim=start_frame={lead}:end_frame={lead+length},setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1',
            '-frames:v',str(length),'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(edit)])
    assert int(probe(edit)['nb_frames'])==length
    samples=[]
    for name,local in [('in',0),('mid',length//2),('out',length-1)]:
        png=OUT/'qa'/(shot['id']+suffix+'-'+name+'.png')
        if not png.exists():
            run(['-ss',str(local/24),'-i',str(edit),'-frames:v','1',str(png)])
        samples.append(png.relative_to(BASE).as_posix())
    item=dict(id=original['id'],takeId=shot['id'],planRef=source_plan,
        submissionRef=(folder/'submission.json').relative_to(BASE).as_posix(),
        editorialNotes=shot.get('editorialNotes','First-pass native motion; exact V61 timing retained.'),
        shotId=shot['shotId'],plate=shot['plate'],title=shot['title'],
        motionRef=raw.relative_to(BASE).as_posix(),editRef=edit.relative_to(BASE).as_posix(),
        nativeFrames=count,nativeWidth=info['width'],nativeHeight=info['height'],fps=24,
        startFrame=shot['startFrame'],editFrames=length,sourceEditStartFrame=lead+1,
        availableLeadOutFrames=count-lead-length,qaImages=samples)
    manifest.append(item)
    print('Validated',shot['id'],count,'source frames',length,'edit frames',flush=True)
    if shot['plate'] in ('cosmic-background','harper-portrait'):
        frames=OUT/('finale-'+shot['plate'])
        frames.mkdir(exist_ok=True)
        if len(list(frames.glob('frame_*.png')))!=length:
            run(['-i',str(edit),'-frames:v',str(length),str(frames/'frame_%04d.png')])
for page,start in enumerate(range(0,len(manifest),5),1):
    batch=manifest[start:start+5]
    canvas=Image.new('RGB',(1280,len(batch)*267),(16,21,29))
    draw=ImageDraw.Draw(canvas)
    for row,item in enumerate(batch):
        draw.text((8,row*267+5),f"{item['takeId']} | {item['editFrames']}f | edit in / middle / out",fill='white')
        for col,ref in enumerate(item['qaImages']):
            with Image.open(BASE/ref) as im:
                canvas.paste(im.resize((426,240)),(col*426,row*267+25))
    canvas.save(OUT/'qa'/f'page-{page:02d}.jpg',quality=93)
(OUT/'media-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Prepared',len(manifest),'takes for motion review.',flush=True)
