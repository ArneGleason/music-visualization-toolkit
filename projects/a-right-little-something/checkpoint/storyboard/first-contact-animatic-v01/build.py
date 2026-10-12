"""Render approved first-contact boards on the canonical grid and install V60."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
from PIL import Image

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2];ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from lyric_overlay import write_lyrics

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def run(args):subprocess.run(['ffmpeg','-y','-v','error',*args],cwd=OUT,check=True)
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(path)]))['streams'][0]

path=BASE/'shots/shotlist.json';register=read(path)
save(OUT/'prior-shotlist.json',register)
shots=sorted([s for s in register['storyboardProposals'] if s.get('batch')=='first-contact-v01'],key=lambda s:s['startFrame'])
start,end=shots[0]['startFrame'],shots[-1]['endFrameExclusive']
assert (start,end,len(shots))==(3144,5266,37)
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(shots,shots[1:]))
for shot in shots:
    shot.setdefault('description','Harper travels in her sphere between the destination spectacle views.')
    shot['frames']=shot['endFrameExclusive']-shot['startFrame']
    shot['startingFrameDraft'].update(image=shot['still'],userSelected=True,status='User-approved still for animatic')
save(path,register)

frames=end-start
output=OUT/'stills-picture.mp4'
encoder=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-','-an','-frames:v',str(frames),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(output)],stdin=subprocess.PIPE)
entries=[]
try:
    for shot in shots:
        count=shot['frames']
        if shot['id']=='contact-032':
            for local in range(1,count+1):
                with Image.open(OUT/f'finale-frames/frame_{local:04d}.png') as im:
                    encoder.stdin.write(im.convert('RGB').tobytes())
            kind='Blender two-source still composite'
        else:
            with Image.open(BASE/shot['still']) as im:
                pixels=im.convert('RGB').resize((1920,1080),Image.Resampling.LANCZOS).tobytes()
            for _ in range(count):encoder.stdin.write(pixels)
            kind='held storyboard still'
        entries.append(dict(shot=shot['id'],image=shot['still'],startFrame=shot['startFrame'],endFrameExclusive=shot['endFrameExclusive'],frames=count,kind=kind))
        print('Rendered',shot['id'],count,'frames',flush=True)
finally:encoder.stdin.close()
assert encoder.wait()==0
assert int(probe(output)['nb_frames'])==frames
data=read(BASE/'generated/animatic/animatic-data.json')
captions=copy.deepcopy(data)
captions['phrases']=[p for p in captions['phrases'] if start<=p['startFrame']<end]
for phrase in captions['phrases']:
    for item in [phrase]+phrase['words']:
        item['startFrame']-=start-1;item['endFrameExclusive']-=start-1
style=read(BASE/'project.json')['production']['lyricPresentation']
write_lyrics(captions,style,OUT/'lyrics.ass')
(OUT/'fonts').mkdir(exist_ok=True);shutil.copy2(style['fontFile'],OUT/'fonts'/Path(style['fontFile']).name)
source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v59.mp4'
run(['-i',str(output),'-i',str(source),'-filter_complex',f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={(start-1)/24}:end={(end-1)/24},asetpts=PTS-STARTPTS[a]',
     '-map','[v]','-map','[a]','-frames:v',str(frames),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','timed-still-board.mp4'])
assert int(probe(OUT/'timed-still-board.mp4')['nb_frames'])==frames
spec=dict(id='first-contact-v01',output=OUT.relative_to(BASE).as_posix(),sourceAnimatic=source.relative_to(BASE).as_posix(),draftForReview=False,
          presentation='V59 through frame 3143, then approved first-contact stills, five travel bridges, and an editable Blender two-source finale.',
          mediaLabel='First contact and travel finale / still animatic',
          continuationNotes='V60: full song storyboard coverage. First-contact stills approved and timed from frame3144 through5265, including five ending travel inserts. Finale uses separate cosmic and Harper stills composited in Blender; clean videos remain to be generated after timing review. V59 preserved.')
save(OUT/'review-options.json',spec)
save(OUT/'assembly-plan.json',dict(version='v60',source=str(source),fps=24,startFrame=start,endFrameExclusive=end,frames=frames,entries=entries,finale=dict(blend='finale-two-plates.blend',sourcePlan=shots[-1]['compositePlan'],preview='Blender Screen blend with animated portrait opacity and gentle cosmic drift; clean video inputs remain separate')))
subprocess.run([sys.executable,str(ROOT/'tools/insert_still_storyboard.py'),str(BASE/'project.json'),str(OUT/'review-options.json'),'--version','v60'],check=True)
r=read(path)
final_shot=next(s for s in r['storyboardProposals'] if s['id']=='contact-032')
final_shot['animaticPlacement'].update(kind='Blender composite of two separate still sources',compositor=(OUT/'finale-two-plates.blend').relative_to(BASE).as_posix(),sourcePlates=shots[-1]['compositePlan']['videoInputs'])
for e in r['reviewEdits']['v60']['entries']:
    if e['shot']=='contact-032':e.update(final_shot['animaticPlacement'])
r['firstContactSequence'].update(status='User-approved stills assembled in V60; timing review pending',animaticVersion='v60',reviewUrl='http://127.0.0.1:8768/?v=v60',timedPreview=(OUT/'timed-still-board.mp4').relative_to(BASE).as_posix(),finaleBlender=(OUT/'finale-two-plates.blend').relative_to(BASE).as_posix())
r['reviewEdits']['v60'].update(newPaidCredits=0,reviewStatus='Timing review pending',preservedVersion='v59')
save(path,r)
final=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v60.mp4'
info=probe(final)
save(OUT/'verification.json',dict(fullFrames=int(info['nb_frames']),fps=info['r_frame_rate'],width=info['width'],height=info['height'],insertStart=start,insertEndExclusive=end,insertFrames=frames,shots=len(shots),travelInserts=5,finaleFrames=shots[-1]['frames'],audio='Original V59 AAC packet hash verified by insertion tool',v59Preserved=source.exists(),newPaidCredits=0))
print('V60 first-contact still animatic ready',flush=True)
