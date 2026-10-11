"""Render the canonical still segments at exact lyric-grid frame counts."""
import copy
from functools import lru_cache
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

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def run(args):
    subprocess.run(['ffmpeg','-y','-v','error',*args],cwd=OUT,check=True)
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(path)]))['streams'][0]

register=read(BASE/'shots/shotlist.json')
shots=sorted([s for s in register['storyboardProposals'] if s.get('batch')=='departure-discovery-v01'],key=lambda s:s['startFrame'])
segments=[segment for shot in shots for segment in shot['storyboardSegments']]
start,end=shots[0]['startFrame'],shots[-1]['endFrameExclusive']
assert end-start==549
@lru_cache(maxsize=4)
def picture(name,scale=1,cx=.5,cy=.5):
    with Image.open(BASE/name) as im:
        if scale!=1:
            w,h=im.width/scale,im.height/scale
            box=(im.width*cx-w/2,im.height*cy-h/2,im.width*cx+w/2,im.height*cy+h/2)
            assert box[0]>=0 and box[1]>=0 and box[2]<=im.width and box[3]<=im.height
            im=im.crop(box)
        return im.convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS)

output=OUT/'stills-picture.mp4'
encoder=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-an',
    '-frames:v',str(end-start),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(output)],stdin=subprocess.PIPE)
index=0
try:
    for f in range(start,end):
        while index+1<len(segments) and f>=segments[index+1]['startFrame']:
            index+=1
        segment=segments[index]
        framing=segment.get('editorialFraming',{})
        frame=picture(segment['image'],framing.get('scale',1),framing.get('cx',.5),framing.get('cy',.5))
        if 2747<=f<2759:
            frame=Image.blend(picture(segments[1]['image']),picture(segments[2]['image']),(f-2747+.5)/12)
        encoder.stdin.write(frame.tobytes())
finally:
    encoder.stdin.close()
assert encoder.wait()==0
assert int(probe(output)['nb_frames'])==549
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
source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v52.mp4'
run(['-i',str(output),'-i',str(source),'-filter_complex',
    f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={(start-1)/24}:end={(end-1)/24},asetpts=PTS-STARTPTS[a]',
    '-map','[v]','-map','[a]','-frames:v','549','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','192k','-movflags','+faststart','timed-still-board.mp4'])
assert int(probe(OUT/'timed-still-board.mp4')['nb_frames'])==549
print('Built 549-frame still passage with word-timed lyrics')
