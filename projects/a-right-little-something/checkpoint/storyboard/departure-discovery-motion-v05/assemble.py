"""Install the brighter station twinkle while retaining all accepted V58 effects."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
from PIL import Image, ImageChops

OUT=Path(__file__).resolve().parent
OLD=OUT.with_name('departure-discovery-motion-v04')
BASE=OUT.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def run(args): subprocess.run(['ffmpeg','-y','-v','error',*args],cwd=OUT,check=True)
r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v58'
save(OUT/'prior-shotlist.json',r)
changed=[]
for frame in range(1,141):
    name=f'frame_{frame:04d}.png'
    before=Image.open(OLD/'departure-frames'/name).convert('RGB')
    after=Image.open(OUT/'departure-frames'/name).convert('RGB')
    if ImageChops.difference(before,after).getbbox(): changed.append(frame)
assert changed and all(2<=f<=16 for f in changed),changed
run(['-framerate','24','-i','departure-frames/frame_%04d.png','-frames:v','140','-an',
    '-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','departure-pullout-twinkle.mp4'])
concat=(OLD/'concat.txt').read_text().replace((OLD/'departure-pullout-twinkle.mp4').as_posix(),(OUT/'departure-pullout-twinkle.mp4').as_posix())
(OUT/'concat.txt').write_text(concat)
run(['-f','concat','-safe','0','-i','concat.txt','-an','-c','copy','hybrid-picture.mp4'])
shutil.copy2(OLD/'lyrics.ass',OUT/'lyrics.ass')
shutil.copytree(OLD/'fonts',OUT/'fonts',dirs_exist_ok=True)
source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v58.mp4'
run(['-i','hybrid-picture.mp4','-i',str(source),'-filter_complex',
    f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={2594/24}:end={3143/24},asetpts=PTS-STARTPTS[a]',
    '-map','[v]','-map','[a]','-frames:v','549','-c:v','libx264','-preset','fast','-crf','18',
    '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','timed-still-board.mp4'])
options=read(OLD/'review-options.json')
options.update(output=OUT.relative_to(BASE).as_posix(),sourceAnimatic=source.relative_to(BASE).as_posix(),
    presentation='Accepted stronger zoom and Blender pullout, with brighter and larger cyan station twinkle',
    continuationNotes='V59: cyan twinkle doubled in size and 2.5x linear light intensity. V58 pullout, stronger zoom overlaps, all timing and master music retained.')
save(OUT/'review-options.json',options)
subprocess.run([sys.executable,str(BASE.parents[1]/'tools/insert_still_storyboard.py'),str(BASE/'project.json'),str(OUT/'review-options.json'),'--version','v59'],check=True)
current=read(BASE/'shots/shotlist.json')
r['activeReviewEdit']='v59'
r['reviewEdits']['v58'].update(acceptedElements=['Stronger zoom overlaps','Blender pullout'],
    reviewNotes='User accepts stronger zoom and pullout; requests a more noticeable twinkle.')
edit=copy.deepcopy(r['reviewEdits']['v58'])
edit.update(source=str(source),video=current['reviewEdits']['v59']['video'],type='Brighter cyan station twinkle',
    presentation=options['presentation'],newPaidCredits=0)
r['reviewEdits']['v59']=edit
s=next(s for s in r['storyboardProposals'] if s['id']=='departure-002')
notes='V59: station twinkle doubled in spatial size and 2.5x linear light intensity. Same cyan hue, peak at localframe6, gone by17. Accepted V58 Blender 18% pullout and stronger zoom transitions retained; all timing and music unchanged.'
ref=(OUT/'departure-pullout-twinkle.mp4').relative_to(BASE).as_posix()
composite=copy.deepcopy(s['motionSelection']['compositor'])
composite['twinkle'].update(sizeMultiplierVsV58=2,linearLightMultiplierVsV58=2.5)
composite['blend']=(OUT/'departure-pullout-twinkle.blend').relative_to(BASE).as_posix()
selection=copy.deepcopy(s['motionSelection'])
selection.update(id='departure-brighter-twinkle-v59',motionRef=ref,compositor=composite,reviewNotes=notes)
s.setdefault('motionTests',[]).append(selection)
s.update(motionSelection=selection,motionRef=ref,motionReview=dict(usable=True,notes=notes),
    editorialDirection=notes,stillPreviewNote=notes,status='Brighter twinkle in V59; playback review pending')
for placement in s['nativePlacements']: placement['motionRef']=ref
s['animaticPlacement'].update(motionRef=ref,nativePlacements=s['nativePlacements'],compositor=composite)
for shot in r['storyboardProposals']:
    if shot.get('batch')=='departure-discovery-v01': shot['animaticPlacement']['animaticVersion']='v59'
    if shot['id']=='departure-004':
        shot['status']='Stronger zoom overlaps accepted by user; retained in V59'
        shot['animaticPlacement']['userSelected']=True
for entry in edit['entries']:
    entry['animaticVersion']='v59'
    if entry['shot']=='departure-002': entry.update(s['animaticPlacement'])
edit['departureComposite']=composite
seq=r['departureDiscoverySequence']
seq.update(status='V59 brighter twinkle preview ready',reviewUrl='http://127.0.0.1:8768/?v=v59',motionReviewUrl='http://127.0.0.1:8768/storyboard/departure-discovery-motion-v05/')
seq['motionRequest']['status']='Existing media assembled in V59; stronger zoom and pullout accepted, brighter twinkle for review; no new spend'
save(BASE/'shots/shotlist.json',r)
opening=read(BASE/'generated/animatic/current-opening.json')
for item in opening['shots']:
    if item['id']=='departure-002': item['review']=s['motionReview']
save(BASE/'generated/animatic/current-opening.json',opening)
save(OUT/'verification.json',dict(fullFrames=5265,passageFrames=549,departureFrames=140,fps=24,
    changedDepartureFrames=changed,unchangedDepartureFrames=140-len(changed),
    acceptedZoomClip='V58 zoom-overlap.mp4 reused without modification',
    originalMasterAudio='AAC packets verified identical to V58 by insertion tool',newCredits=0,cumulativeCredits=3384,compositor=composite))
(OUT/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Brighter station twinkle — V59</title><style>body{background:#10282e;color:#efdfc0;font:16px/1.5 system-ui;max-width:1100px;margin:24px auto;padding:0 20px}video{width:100%}a{color:#9bd9e9}</style><h1>V59 · More visible station twinkle</h1><video controls src="timed-still-board.mp4"></video><p>Twice the size and brighter, with the same short pulse. Accepted pullout and stronger zoom retained.</p><a href="/">Current full animatic</a> · <a href="../departure-discovery-motion-v04/">Prior comparison</a> · <a href="departure-pullout-twinkle.blend">Editable Blender scene</a>''',encoding='utf-8')
print('V59 ready; only departure pulse frames changed:',changed)
