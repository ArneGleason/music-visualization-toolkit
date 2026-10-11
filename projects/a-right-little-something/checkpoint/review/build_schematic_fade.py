import copy
from pathlib import Path
import shutil
import subprocess
import sys

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import encode, load, probe, run, save
from lyric_overlay import write_lyrics

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/schematic-fade-v01'
out.mkdir(parents=True,exist_ok=True)
source=base/'generated/animatic/A-Right-Little-Something-selected-motion-v27.mp4'
project=load(base/'project.json')
register=load(base/'shots/shotlist.json')
shots={s['id']:s for s in register['storyboardProposals']}
data=load(base/'generated/animatic/animatic-data.json')
fps=data['fps']
boundary=shots['space-007']['endFrameExclusive']
assert boundary==737
width=24
start,end=boundary-width//2,boundary+width//2
# Map source121–144 extends the nominal source29–132 edit by twelve frames.
# Inlet source13–36 begins twelve frames before its nominal source25 entry.
for name,path,first in [('map',base/shots['space-007']['motionRef'],121),
                       ('inlet',base/shots['space-008']['motionRef'],13)]:
    assert int(probe(path)['nb_frames'])>=first-1+width
    encode(['-i',str(path),'-vf',f'fps={fps},trim=start_frame={first-1}:end_frame={first-1+width},setpts=N/({fps}*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1'],
           width,out/(name+'.mp4'))
graph=("[0:v]format=gbrp[a];[1:v]format=gbrp[b];"
       f"[a][b]blend=all_expr='A*(1-min(1,max(0,(N-1)/{width-1})))+B*min(1,max(0,(N-1)/{width-1}))':shortest=1,format=yuv420p[v]")
encode(['-i',str(out/'map.mp4'),'-i',str(out/'inlet.mp4'),'-filter_complex',graph,'-map','[v]'],width,out/'fade-picture.mp4')
captions=copy.deepcopy(data)
captions['phrases']=[p for p in captions['phrases'] if p['startFrame']<end and p['endFrameExclusive']>start]
for phrase in captions['phrases']:
    for item in [phrase]+phrase['words']:
        item['startFrame']=max(start,min(end,item['startFrame']))-start+1
        item['endFrameExclusive']=max(start,min(end,item['endFrameExclusive']))-start+1
style=project['production']['lyricPresentation']
write_lyrics(captions,style,out/'lyrics.ass')
(out/'fonts').mkdir(exist_ok=True)
shutil.copy2(style['fontFile'],out/'fonts'/Path(style['fontFile']).name)
encode(['-i','fade-picture.mp4','-vf','ass=lyrics.ass:fontsdir=fonts'],width,out/'fade-lettered.mp4',out)
for name,a,b in [('before',0,start-1),('after',end-1,data['frames'])]:
    encode(['-reinit_filter','0','-i',str(source),'-vf',f'trim=start_frame={a}:end_frame={b},setpts=N/({fps}*TB),setsar=1'],b-a,out/(name+'.mp4'))
(out/'full.txt').write_text("file 'before.mp4'\nfile 'fade-lettered.mp4'\nfile 'after.mp4'\n",encoding='utf-8')
run(['-f','concat','-safe','0','-i','full.txt','-c','copy','full-picture.mp4'],out)
final=base/'generated/animatic/A-Right-Little-Something-selected-motion-v28.mp4'
pending=final.with_name(final.stem+'.rendering.mp4')
run(['-i',str(out/'full-picture.mp4'),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(pending)])
info=probe(pending)
assert (int(info['nb_frames']),info['width'],info['height'],info['r_frame_rate'])==(5265,1920,1080,'24/1')
hashes=[subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip() for p in (source,pending)]
assert hashes[0]==hashes[1]
pending.replace(final)
for name,a,b in [('fade-review',713,769),('animatic-through-bright-night',0,1957)]:
    run(['-reinit_filter','0','-i',str(final),'-vf',f'trim=start_frame={a}:end_frame={b},setpts=N/(24*TB)',
        '-af',f'atrim=start={a/fps}:end={b/fps},asetpts=PTS-STARTPTS','-frames:v',str(b-a),
        '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
        '-movflags','+faststart',str(out/(name+'.mp4'))])
    assert int(probe(out/(name+'.mp4'))['nb_frames'])==b-a
proposal=dict(id='schematic-fade-v01',boundaryFrame=boundary,frames=width,startFrame=start,endFrameExclusive=end,
    outgoingSourceFrames=[121,144],incomingSourceFrames=[13,36],recoveredOutgoingFrames=12,
    timing='Centered at unchanged Why am I so cramped phrase start; no held or retimed frames',
    status='Agent checked transition draft; user playback pending')
register.setdefault('editProposals',{})['schematic-fade-v01']=proposal
register['reviewEdits']['v27']['userReview']='User: good; approved lab stills for Kling motion and requested schematic fade catch-up.'
register['reviewEdits']['v28']=dict(source=str(source),video=str(final),proposal='schematic-fade-v01',frames=5265,fps=24,
    draftForReview=True,startFrame=start,endFrameExclusive=end,audio='Original master AAC packets preserved')
register['activeReviewEdit']='v28'
shots['space-007']['compositeSelection']['transitionLeadOutUsedFrames']=12
for item in register['storyboardProposals']:
    if item.get('batch')=='lab-verse-v02':
        for key in ('startingFrameDraft','startingFrameSelection','animaticPlacement'):
            item[key]['userSelected']=True
        item['status']='User accepted still; native Kling animation prepared, not yet submitted'
save(base/'shots/shotlist.json',register)
root=base/'generated/animatic'
save(root/'current-media.json',dict(video=final.name+f'?v={final.stat().st_mtime_ns}'))
save(base/'generated/review/current-render.json',dict(video=str(final),master_start=1))
opening=load(root/'current-opening.json')
opening['version']='v28'
next(s for s in opening['shots'] if s['id']=='space-007')['review']['notes']+=' V28 uses all12 outgoing tail frames in a centered24frame dissolve into inlet, no lyric timing shift.'
save(root/'current-opening.json',opening)
project['production'].update(animatic=final.relative_to(base).as_posix(),schematicFadeReview='http://127.0.0.1:8768/storyboard/schematic-fade-v01/fade-review.mp4')
save(base/'project.json',project)
save(out/'verification.json',dict(proposal,fullFrames=5265,reviewFrames=1957,masterAudioHash=hashes[1],audioPreserved=True,extraKlingCredits=0))
print('V28 ready:12 outgoing frames recovered in24frame fade; master audio/grid preserved.')
