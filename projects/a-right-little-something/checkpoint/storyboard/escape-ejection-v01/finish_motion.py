"""Verify the full V39 motion edit and expose useful playback excerpts."""
import json
from pathlib import Path
import subprocess

INPUT=Path(__file__).resolve().parent
PROJECT=INPUT.parents[2]
OUT=INPUT.parent/'escape-ejection-motion-v01'
def load(path):
    return json.loads(path.read_text(encoding='utf-8'))
def save(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
        '-show_entries','stream=nb_frames,r_frame_rate,width,height','-of','json',str(path)]))['streams'][0]

register_path=PROJECT/'shots/shotlist.json'
register=load(register_path)
assert register['activeReviewEdit']=='v39'
current=[s for s in register['storyboardProposals'] if s.get('batch')=='escape-ejection-motion-v01']
assert len(current)==11
for shot in current:
    if shot['id'].startswith('lab2-'):
        shot['status']='User accepted native motion retained; latest user-directed Bright night trim retained'
        shot['animaticPlacement']['userSelected']=True
for item in register['reviewEdits']['v39']['entries']:
    if item['shot'].startswith('lab2-'):
        item['userSelected']=True
save(register_path,register)

video=PROJECT/'generated/animatic/A-Right-Little-Something-selected-motion-v39.mp4'
info=probe(video)
assert (int(info['nb_frames']),info['r_frame_rate'],info['width'],info['height'])==(5265,'24/1',1920,1080)
digest=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-map','0:a:0','-c','copy',
    '-f','hash','-hash','sha256','-'],text=True).strip()
assert digest.endswith('29fa51608bc4d3b5937841dbcced1676a38721c5572ecd92e064e4c08a8e1017')
for name,start,end in [('escape-passage',1838,2105),('animatic-through-escape',1,2105)]:
    subprocess.run(['ffmpeg','-y','-v','error','-reinit_filter','0','-i',str(video),'-vf',
        f'trim=start_frame={start-1}:end_frame={end-1},setpts=N/(24*TB)',
        '-af',f'atrim=start={(start-1)/24}:end={(end-1)/24},asetpts=PTS-STARTPTS',
        '-frames:v',str(end-start),'-c:v','libx264','-preset','fast','-crf','18','-c:a','aac',
        '-b:a','192k','-movflags','+faststart',str(OUT/(name+'.mp4'))],check=True)
    assert int(probe(OUT/(name+'.mp4'))['nb_frames'])==end-start
for frame,label in [(1897,'cut-inside'),(1972,'leaving-orbit'),(2060,'exterior'),(2098,'accelerating')]:
    subprocess.run(['ffmpeg','-y','-v','error','-reinit_filter','0','-i',str(video),'-vf',
        f'select=eq(n\\,{frame-1}),setpts=PTS-STARTPTS','-frames:v','1',str(OUT/(label+'.png'))],check=True)
save(OUT/'verification.json',dict(version='v39',frames=5265,fps=24,width=1920,height=1080,
    audioPacketHash=digest,interiorStartFrame=1897,interiorEndFrameExclusive=2010,
    exteriorStartFrame=2010,exteriorEndFrameExclusive=2105,
    newShots='Native Kling interior release and exterior departure; user playback pending',
    paidCreditsThisBatch=112,confirmedCumulativeKlingCredits=2472))
print('V39 and two excerpts verified; master audio unchanged; two native departure clips inserted')
