"""Assemble three retained takes, five new takes and two still ship flips."""
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
prior=read(BASE/'kling-station-concourse-v01.json')
plan=read(BASE/'kling-station-concourse-v02.json')
spec=read(OUT/'review-options.json')
plan['transitions']=spec['transitions']
register=read(BASE/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='station-concourse-v05']
entries={s['shotId']:s for s in prior['shots']}
for take in plan['shots']:
    for placement in take['placements']:
        entries[placement['shotId']]={**take,**placement}
fps=24
width,height=1920,1080
start,end=shots[0]['startFrame'],shots[-1]['endFrameExclusive']
assert end-start==490
mode='hybrid'

@lru_cache(maxsize=2)
def frames(index):
    shot=shots[index]
    if shot['id'] not in spec['motionShotIds']:
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
        vf=f'fps=24,trim=start_frame={lead-6}:end_frame={lead+shot["frames"]+6},setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1'
        count=shot['frames']+12
    raw=subprocess.check_output(['ffmpeg','-v','error','-threads','2','-i',str(source),
        '-vf',vf,'-frames:v',str(count),'-f','rawvideo','-pix_fmt','rgb24','-'])
    assert len(raw)==count*width*height*3
    return raw

def frame(index,global_frame):
    n=0 if shots[index]['id'] not in spec['motionShotIds'] else global_frame-shots[index]['startFrame']+6
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
            if transition['type']=='dissolve':
                result=Image.blend(frame(incoming-1,g),frame(incoming,g),progress)
                encoder.stdin.write(result.tobytes())
                continue
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
source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v49.mp4'
output='timed-still-board.mp4'
run(['-i',str(picture),'-i',str(source),'-filter_complex',
    f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={(start-1)/fps}:end={(end-1)/fps},asetpts=PTS-STARTPTS[a]',
    '-map','[v]','-map','[a]','-frames:v',str(end-start),'-c:v','libx264','-preset','fast',
    '-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',output])
assert int(probe(OUT/output)['nb_frames'])==490
(OUT/'timing-check.json').write_text(json.dumps(dict(mode=mode,frames=490,fps=24,startFrame=start,
    endFrameExclusive=end,transitions=plan['transitions'],imageTranslation=False),indent=2)+'\n')
cards=[]
for take in plan['shots']:
    name=take['shotId']+'-clean.mp4'
    shutil.copy2(BASE/take['motionRef'],OUT/name)
    cards.append(f'<article><h2>{html.escape(take["title"])}</h2><video controls preload="metadata" src="{name}"></video><p>{take["duration"]} second take · {take["actualCredits"]} credits</p><p>{html.escape(take.get("reviewNotes",""))}</p><details><summary>Motion prompt</summary><pre style="white-space:pre-wrap">{html.escape(take["prompt"])}</pre></details></article>')
page=f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Concourse motion — walk, consider, continue</title><style>body{{background:#10282e;color:#efdfc0;font:16px/1.5 system-ui;max-width:1100px;margin:auto;padding:24px}}a{{color:#9bd9e9}}video,img{{width:100%;display:block}}article{{margin:24px 0;padding:16px;background:#19343b}}h2{{font-size:20px}}</style>
<h1>Concourse motion: walk, consider, continue</h1><p>Five clean native takes. Captain exchange, food concourse, parts market, gantry walk and entrance-view consideration. The two brief ship flips use approved stills with right-to-left reveal wipes.</p><p>One continuous gantry take supplies both walking sections, with the close-up between them. 240 credits charged. User playback review pending.</p>
<video controls preload="metadata" src="timed-still-board.mp4"></video><p><a href="/?v=v50">Full V50 animatic</a> · <a href="hybrid-picture.mp4">Clean assembled passage, no lyrics or music</a></p>{''.join(cards)}'''
(OUT/'index.html').write_text(page,encoding='utf-8')
print('Built native motion assembly:',OUT/output)
