"""Assemble exact-frame native takes with stationary-image right-to-left wipes."""
import argparse
import copy
from functools import lru_cache
import html
import json
from pathlib import Path
import shutil
import subprocess
import sys
from PIL import Image

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from lyric_overlay import write_lyrics

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def run(args):
    subprocess.run(['ffmpeg','-y','-v','error',*args],check=True,cwd=OUT)

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
        '-show_streams','-of','json',str(p)]))['streams'][0]

parser=argparse.ArgumentParser()
parser.add_argument('--stills',action='store_true')
args=parser.parse_args()
plan=read(BASE/'kling-station-concourse-v01.json')
register=read(BASE/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='station-concourse-v01']
entries={s['shotId']:s for s in plan['shots']}
fps=24
width,height=1920,1080
start,end=shots[0]['startFrame'],shots[-1]['endFrameExclusive']
assert end-start==490
mode='stills' if args.stills else 'native'

@lru_cache(maxsize=2)
def frames(index):
    shot=shots[index]
    if args.stills:
        source=BASE/shot['startingFrameDraft']['image']
        vf='scale=1920:1080,setsar=1'
        count=1
    else:
        take=entries[shot['id']]
        folder=BASE/plan['output']/take['id']
        source=BASE/take['motionRef'] if take.get('motionRef') else next(folder.glob('*-clean.mp4'),None)
        assert source, f'Clean native output missing: {take["id"]}'
        lead=take.get('sourceEditStartFrame',25)-1
        info=probe(source)
        assert int(info['nb_frames'])>=lead+shot['frames']+24
        assert int(info['height'])==1080 and int(info['width'])<=1920
        vf=f'fps=24,trim=start_frame={lead-2}:end_frame={lead+shot["frames"]+2},setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1'
        count=shot['frames']+4
    raw=subprocess.check_output(['ffmpeg','-v','error','-threads','2','-i',str(source),
        '-vf',vf,'-frames:v',str(count),'-f','rawvideo','-pix_fmt','rgb24','-'])
    assert len(raw)==count*width*height*3
    return raw

def frame(index,global_frame):
    n=0 if args.stills else global_frame-shots[index]['startFrame']+2
    size=width*height*3
    raw=frames(index)
    return Image.frombytes('RGB',(width,height),raw[n*size:(n+1)*size])

picture=OUT/(mode+'-picture.mp4')
encoder=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24',
    '-s','1920x1080','-r','24','-i','-','-an','-frames:v',str(end-start),
    '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(picture)],stdin=subprocess.PIPE)
index=0
try:
    for g in range(start,end):
        while index+1<len(shots) and g>=shots[index+1]['startFrame']:
            index+=1
        transition=next((t for t in plan['transitions'] if t['startFrame']<=g<t['endFrameExclusive']),None)
        if transition:
            incoming=next(i for i,s in enumerate(shots) if s['id']==transition['incomingShot'])
            progress=(g-transition['startFrame']+.5)/transition['frames']
            edge=width*(1-progress)
            values=[min(1,max(0,(x-edge)/transition['featherPixels']+.5)) for x in range(width)]
            mask=Image.new('L',(width,1))
            mask.putdata([round(255*t*t*(3-2*t)) for t in values])
            mask=mask.resize((width,height))
            result=Image.composite(frame(incoming,g),frame(incoming-1,g),mask)
            accent=Image.new('L',(width,1))
            accent.putdata([round(255*max(0,1-abs(x-edge)/transition['edgeAccentPixels'])*transition['edgeAccentOpacity']) for x in range(width)])
            result=Image.composite(Image.new('RGB',(width,height),(190,220,222)),result,accent.resize((width,height)))
        else:
            result=frame(index,g)
        encoder.stdin.write(result.tobytes())
finally:
    encoder.stdin.close()
assert encoder.wait()==0
assert int(probe(picture)['nb_frames'])==end-start

data=read(BASE/'generated/animatic/animatic-data.json')
captions=copy.deepcopy(data)
captions['phrases']=[p for p in captions['phrases'] if start<=p['startFrame']<end]
for phrase in captions['phrases']:
    for item in [phrase]+phrase['words']:
        item['startFrame']-=start-1
        item['endFrameExclusive']-=start-1
style=read(BASE/'project.json')['production']['lyricPresentation']
write_lyrics(captions,style,OUT/'lyrics.ass')
(OUT/'fonts').mkdir(exist_ok=True)
shutil.copy2(style['fontFile'],OUT/'fonts'/Path(style['fontFile']).name)
source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v44.mp4'
output='wipe-still-preview.mp4' if args.stills else 'timed-still-board.mp4'
run(['-i',str(picture),'-i',str(source),'-filter_complex',
    f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={(start-1)/fps}:end={(end-1)/fps},asetpts=PTS-STARTPTS[a]',
    '-map','[v]','-map','[a]','-frames:v',str(end-start),'-c:v','libx264','-preset','fast',
    '-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',output])
assert int(probe(OUT/output)['nb_frames'])==490
(OUT/'timing-check.json').write_text(json.dumps(dict(mode=mode,frames=490,fps=24,startFrame=start,
    endFrameExclusive=end,transitions=plan['transitions'],imageTranslation=False),indent=2)+'\n')
cards=[]
for shot in shots:
    take=entries[shot['id']]
    image='../station-concourse-v01/'+Path(take['firstImage']).name
    media=f'<img src="{image}">'
    if not args.stills:
        filename=shot['id']+'-clean.mp4'
        shutil.copy2(BASE/take['motionRef'],OUT/filename)
        media=f'<video controls preload="metadata" poster="{image}" src="{filename}"></video>'
    credit_label='estimated' if args.stills else 'charged'
    cards.append(f'<article><h2>{html.escape(shot["title"])}</h2>{media}<p>{take["duration"]} second take; {take["editFrames"]} edit frames; {credit_label} {take.get("actualCredits",take["estimatedCredits"])} credits</p><details><summary>Exact motion prompt</summary><pre>{html.escape(take["prompt"])}</pre></details></article>')
page=f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Concourse motion and flip wipes</title><style>body{{background:#10282e;color:#efdfc0;font:16px/1.5 system-ui;max-width:1100px;margin:auto;padding:24px}}a{{color:#9bd9e9}}video,img{{width:100%;display:block}}article{{margin:24px 0;padding:16px;background:#19343b}}pre{{white-space:pre-wrap}}h2{{font-size:20px}}</style>
<h1>Concourse motion and flip wipes</h1><p>{'STILL TRANSITION PREVIEW — native generation pending' if args.stills else 'CLEAN NATIVE MOTION — assembled review draft'}</p>
<p>Three four-frame vertical reveals sweep right to left; images remain fixed. Narrow soft edge with a restrained pale accent. Exact 490-frame passage, 24 fps. Eleven takes, 49 generated seconds, estimated 392 credits.</p>
<video controls src="{output}"></video><p><a href="/?v={'v44' if args.stills else 'v45'}">Full animatic and notes</a> · <a href="../station-concourse-v01/">Accepted stills</a></p>{''.join(cards)}'''
(OUT/'index.html').write_text(page,encoding='utf-8')
if not args.stills:
    page=page.replace('estimated 392 credits','392 credits charged')
    page=page.replace('<video controls src=', '<p><a href="native-picture.mp4">Clean assembled passage, without lyrics or audio</a></p><video controls src=',1)
    (OUT/'index.html').write_text(page,encoding='utf-8')
print('Built',mode,'review:',OUT/output)
