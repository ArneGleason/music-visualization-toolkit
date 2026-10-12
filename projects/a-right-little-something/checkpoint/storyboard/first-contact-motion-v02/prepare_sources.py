"""Prepare frame-exact sources and handles for the V63 local effects."""
import argparse
import json
from pathlib import Path
import subprocess
from PIL import Image,ImageDraw

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--available',action='store_true');parser.add_argument('--refresh-plates',action='store_true');args=parser.parse_args()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def run(a):subprocess.run(['ffmpeg','-y','-v','error',*a],check=True)
def frames(path):
    return int(json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(path)]))['streams'][0]['nb_frames'])
plan=read(BASE/'kling-first-contact-motion-v02.json')
prior={m['shotId']:m for m in read(OUT.parent/'first-contact-motion-v01/media-manifest.json') if m['plate']=='main'}
tasks=[]
for sid,count in [('contact-017',41),('contact-020',122),('contact-022',53)]:
    m=prior[sid];tasks.append(dict(id=sid,source=BASE/m['motionRef'],lead=m['sourceEditStartFrame']-1,count=count,editFrames=count-8))
for s in plan['shots']:
    raw=BASE/plan['output']/s['id']/(s['id']+'-01-clean.mp4')
    if not raw.exists() and args.available:continue
    assert raw.exists(),raw
    tasks.append(dict(id=s['id'],source=raw,lead=s['sourceEditStartFrame']-1,count=s['editFrames']+8,editFrames=s['editFrames']))
manifest=[]
for t in tasks:
    suffix=f"-source{t['lead']+1}" if t['lead']!=24 else ''
    out=OUT/'sources'/(t['id']+suffix);out.mkdir(parents=True,exist_ok=True)
    assert frames(t['source'])>=t['lead']+t['count'],t
    plate='plate' in t['id']
    if len(list(out.glob('frame_*.png')))!=t['count'] or (plate and args.refresh_plates):
        color='magenta' if plate else 'black'
        run(['-i',str(t['source']),'-vf',f"trim=start_frame={t['lead']}:end_frame={t['lead']+t['count']},setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:0:color={color},setsar=1",'-frames:v',str(t['count']),str(out/'frame_%04d.png')])
    manifest.append(dict(id=t['id'],source=str(t['source']),sourceEditStartFrame=t['lead']+1,editFrames=t['editFrames'],frames=t['count'],sequence=out.relative_to(BASE).as_posix()))
    print('Prepared',t['id'],t['count'],'frames',flush=True)
(OUT/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
new=[m for m in manifest if m['id'] in {s['id'] for s in plan['shots']}]
if new:
    canvas=Image.new('RGB',(1440,len(new)*294),(16,21,29));draw=ImageDraw.Draw(canvas)
    for row,m in enumerate(new):
        draw.text((8,row*294+5),f"{m['id']} / first, midpoint, last selected frame",fill='white')
        for col,f in enumerate([1,m['editFrames']//2+1,m['editFrames']]):
            with Image.open(BASE/m['sequence']/f'frame_{f:04}.png') as im:canvas.paste(im.resize((480,270)),(col*480,row*294+24))
    canvas.save(OUT/'replacement-qa.jpg',quality=94)

# Track known stars in the existing native night shot for attached twinkles.
star_sources=OUT/'sources/contact-020'
seeds=[(1233,205),(1158,64),(1028,206),(1287,86),(1359,144),(1138,213)]
tracks=[]
for x,y in seeds:
    points=[]
    for f in range(1,123):
        with Image.open(star_sources/f'frame_{f:04}.png') as im:
            candidates=[]
            for yy in range(max(0,round(y)-5),min(im.height,round(y)+6)):
                for xx in range(max(0,round(x)-5),min(im.width,round(x)+6)):
                    r,g,b=im.getpixel((xx,yy))[:3]
                    candidates.append((r+g+b-1.8*((xx-x)**2+(yy-y)**2),xx,yy))
            _,x,y=max(candidates)
        points.append([x,y])
    tracks.append(points)
(OUT/'star-tracks.json').write_text(json.dumps(tracks),encoding='utf-8')
