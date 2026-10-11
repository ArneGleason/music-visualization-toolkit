"""Build a hybrid review: five retained native takes and five revised stills."""
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
spec=read(OUT/'review-options.json')
plan['transitions']=spec['transitions']
register=read(BASE/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='station-concourse-v02']
entries={s['shotId']:s for s in plan['shots']}
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
        vf=f'fps=24,trim=start_frame={lead-2}:end_frame={lead+shot["frames"]+2},setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1'
        count=shot['frames']+4
    raw=subprocess.check_output(['ffmpeg','-v','error','-threads','2','-i',str(source),
        '-vf',vf,'-frames:v',str(count),'-f','rawvideo','-pix_fmt','rgb24','-'])
    assert len(raw)==count*width*height*3
    return raw

def frame(index,global_frame):
    n=0 if shots[index]['id'] not in spec['motionShotIds'] else global_frame-shots[index]['startFrame']+2
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
source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v45.mp4'
output='timed-still-board.mp4'
run(['-i',str(picture),'-i',str(source),'-filter_complex',
    f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={(start-1)/fps}:end={(end-1)/fps},asetpts=PTS-STARTPTS[a]',
    '-map','[v]','-map','[a]','-frames:v',str(end-start),'-c:v','libx264','-preset','fast',
    '-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',output])
assert int(probe(OUT/output)['nb_frames'])==490
(OUT/'timing-check.json').write_text(json.dumps(dict(mode=mode,frames=490,fps=24,startFrame=start,
    endFrameExclusive=end,transitions=plan['transitions'],imageTranslation=False),indent=2)+'\n')
cards=[]
for shot in shots:
    if shot['id'] in spec['motionShotIds']:
        continue
    name=Path(shot['startingFrameDraft']['image']).name
    cards.append(f'<article id="{shot["id"]}"><h2>{html.escape(shot["title"])}</h2><img src="{name}"><p>{(shot["startFrame"]-1)/24:.2f}–{(shot["endFrameExclusive"]-1)/24:.2f}s · {shot["frames"]/24:.2f} seconds</p><p>{html.escape(shot["description"])}</p><details><summary>Exact generation prompt</summary><pre style="white-space:pre-wrap">{html.escape(shot["imagePrompt"])}</pre></details></article>')
page=f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Concourse revision — interaction, markets and boarding</title><style>body{{background:#10282e;color:#efdfc0;font:16px/1.5 system-ui;max-width:1100px;margin:auto;padding:24px}}a{{color:#9bd9e9}}video,img{{width:100%;display:block}}article{{margin:24px 0;padding:16px;background:#19343b}}h2{{font-size:20px}}</style>
<h1>Concourse: a more inhabited route</h1><p>Five new composition stills for review. The captain interaction now holds across the third flip and Guess not, then dissolves into two busy market areas. Harper pauses at the gantry before a closer boarding cut. The ship is framed more compactly, with a target of roughly 80% of its previous physical scale; perspective makes the exact ratio approximate.</p>
<p>The first five shots retain accepted native motion. The revised shots are held stills: the pitch, head-shake and walking describe the next motion pass. No new Kling footage has been generated.</p>
<video controls preload="metadata" src="timed-still-board.mp4"></video><p><a href="/?v=v46">Full V46 animatic</a> · <a href="hybrid-picture.mp4">Clean picture preview</a> · <a href="executed.prompt.json">Prompt set</a></p>{''.join(cards)}'''
(OUT/'index.html').write_text(page,encoding='utf-8')
print('Built hybrid still revision:',OUT/output)
