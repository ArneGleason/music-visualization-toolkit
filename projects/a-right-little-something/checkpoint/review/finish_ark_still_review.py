from pathlib import Path
import subprocess
import sys
from PIL import Image,ImageDraw

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,probe,run,save

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/storyboard/ark-replacement-v01'
source=base/'generated/animatic/A-Right-Little-Something-selected-motion-v32.mp4'
final=base/'generated/animatic/A-Right-Little-Something-selected-motion-v33.mp4'
info=probe(final)
assert (int(info['nb_frames']),info['width'],info['height'],info['r_frame_rate'])==(5265,1920,1080,'24/1')
hashes=[subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip() for p in (source,final)]
assert hashes[0]==hashes[1]
for name,a,b in [('animatic-through-bright-night',0,1957),('new-ark-passage',1761,1957)]:
    run(['-reinit_filter','0','-i',str(final),'-vf',f'trim=start_frame={a}:end_frame={b},setpts=N/(24*TB)',
        '-af',f'atrim=start={a/24}:end={b/24},asetpts=PTS-STARTPTS','-frames:v',str(b-a),
        '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
        '-movflags','+faststart',str(out/(name+'.mp4'))])
    assert int(probe(out/(name+'.mp4'))['nb_frames'])==b-a
frames=[1783,1821,1853,1910]
proof=out/'proof-frames'
proof.mkdir(exist_ok=True)
select='+'.join(f'eq(n\\,{n-1})' for n in frames)
run(['-reinit_filter','0','-i',str(final),'-vf',f'select={select},scale=960:540','-fps_mode','passthrough',str(proof/'%02d.png')])
sheet=Image.new('RGB',(1920,1144),'#111111')
draw=ImageDraw.Draw(sheet)
for i,n in enumerate(frames):
    x,y=(i%2)*960,(i//2)*572
    sheet.paste(Image.open(proof/f'{i+1:02d}.png').convert('RGB'),(x,y))
    draw.text((x+8,y+545),f'Frame {n} · {(n-1)/24:.2f}s',fill='white')
sheet.save(out/'animatic-proof.png')
register=load(base/'shots/shotlist.json')
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='ark-replacement-v01']
assert len(shots)==9 and len({s['promptLock'] for s in shots})==1
replacements=[s for s in shots if s['id'] in ('lab2-06','lab2-07','lab2-08','lab2-09')]
assert len(replacements)==4 and all(s['animaticPlacement']['kind']=='still with editorial pan' for s in replacements)
assert [s['frames'] for s in replacements]==[47,29,31,89]
register['reviewEdits']['v33'].update(draftForReview=True,type='Four new biopod ark starting-frame previews',
    nativeLabShots=5,newArkStills=4,reviewUrl='http://127.0.0.1:8768/storyboard/ark-replacement-v01/animatic-through-bright-night.mp4')
save(base/'shots/shotlist.json',register)
project=load(base/'project.json')
project['production']['labVerseReview']=register['reviewEdits']['v33']['reviewUrl']
for ref in project['visualReferences']:
    if ref.get('id')=='headquarters-alien-biopod-ark-v04':
        ref.update(status='User approved reference for replacement starter frames',approvedOn='2026-10-10')
save(base/'project.json',project)
directions=load(out/'shot-directions.json')
manifest=[dict(index=i+1,id=s['id'],output=s['id']+'.png',src=s['id']+'.png',href=s['id']+'.png',
    title=s['title']+' — '+s['direction'],label=s['title'],prompt=s['motionPrompt'],caption=s['direction'],
    route={'startFrame':s['startFrame'],'endFrameExclusive':s['endFrameExclusive'],'frames':s['frames']}) for i,s in enumerate(directions['shots'])]
save(out/'review-manifest.json',manifest)
save(out/'review-options.json',dict(preset='detail-review',showCaptions=True,minTileWidth=480,title='Four new ark starter frames'))
save(out/'verification.json',dict(fullFrames=5265,reviewFrames=1957,arkPassageFrames=196,fps=24,width=1920,height=1080,
    masterAudioHash=hashes[1],audioPreserved=True,nativeLabShots=5,newArkStills=4,newCredits=0,
    cumulativeConfirmedCredits=2264,klingStatus='Prepared directions only; user still review before video go-ahead',
    phraseFrames=[dict(id=s['id'],startFrame=s['startFrame'],frames=s['frames']) for s in replacements]))
print('V33 verified;4newarkstills at exact47/29/31/89frames; originalmaster retained; no new Kling submissions.')
