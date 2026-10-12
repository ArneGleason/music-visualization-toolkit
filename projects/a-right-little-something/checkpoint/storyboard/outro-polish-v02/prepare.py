"""Prepare V65 local revisions without changing the accepted timeline."""
import copy
import json
from pathlib import Path
import subprocess

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
V63 = OUT.parent/'first-contact-motion-v02'
V64 = OUT.parent/'outro-polish-v01'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def save(p,d):
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

register = read(BASE/'shots/shotlist.json')
if not (OUT/'prior-shotlist.json').exists():
    assert register['activeReviewEdit']=='v64'
    save(OUT/'prior-shotlist.json',register)
prior = {e['shot']:e for e in read(V63/'assembly-plan.json')['entries']}
prior.update({e['shot']:e for e in read(V64/'assembly-plan.json')['entries']})
shots = sorted([s for s in register['storyboardProposals'] if s.get('batch')=='first-contact-v01'],key=lambda s:s['startFrame'])
changes = {'contact-001':('opening',0),'contact-002':('opening',18),
           'contact-026':('planet-push',0),'contact-027':('system-departure',0),
           'contact-027-travel':('travel',0),'contact-032':('finale',0)}
entries = []
for s in shots:
    old = prior[s['id']]
    e = dict(shot=s['id'],startFrame=s['startFrame'],endFrameExclusive=s['endFrameExclusive'],frames=s['frames'],
             clip=old['clip'],priorClip=old['clip'],priorSegmentsRoot=str(Path(old['clip']).parent.parent/'segments').replace('\\','/'))
    if 'transition' in old:
        e['transition']=copy.deepcopy(old['transition'])
    if s['id'] in changes:
        effect,lead=changes[s['id']]
        e.update(effect=effect,effectSourceIn=lead)
    entries.append(e)
assert sum(e['frames'] for e in entries)==2122
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(entries,entries[1:]))
save(OUT/'assembly-plan.json',dict(version='v65',source='v64',fps=24,startFrame=3144,endFrameExclusive=5266,frames=2122,entries=entries))

# The portrait starts 48 frames later in its native source, keeping the cosmic
# background and final fade timing fixed. Only invisible tail frames are held.
manifest=read(OUT.parent/'first-contact-motion-v01/media-manifest.json')
portrait=next(s for s in manifest if s['shotId']=='contact-032' and s['plate']=='harper-portrait')
folder=OUT/'sources/harper-advanced'
folder.mkdir(parents=True,exist_ok=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(BASE/portrait['motionRef']),'-vf',
                'trim=start_frame=72,setpts=N/(24*TB),pad=1920:1080:(ow-iw)/2:0,setsar=1,tpad=stop_mode=clone:stop_duration=1',
                '-frames:v','235',str(folder/'frame_%04d.png')],check=True)
assert len(list(folder.glob('frame_*.png')))==235
push=OUT/'sources/planet-push'
push.mkdir(parents=True,exist_ok=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',str(BASE/prior['contact-026']['clip']),'-frames:v','46',str(push/'frame_%04d.png')],check=True)
assert len(list(push.glob('frame_*.png')))==46
save(OUT/'source-manifest.json',dict(
    portrait=dict(source=portrait['motionRef'],oldSourceStartFrame=25,newSourceStartFrame=73,advanceFrames=48,
                  firstInvisibleLocalFrame=155,invisibleTailHoldStartsLocalFrame=218),
    sphereStack=['Warp background','Sphere-only refraction and dark cyan transmission','Unaltered ship / Harper foreground'],
    systemDeparture=dict(twinkleStartFrame=4550,twinklePeakFrame=4567,escapeStartFrame=4583,escapeEndFrame=4648,
                         timing='DAW bar72 beats2–4; escape continues through last frame before Travel27'),
    title=dict(font='Bahnschrift',size=68,tracking=3,copyrightSize=30),newPaidCredits=0))
save(BASE/'outro-v64-review.json',dict(sourceVersion='v64',targetVersion='v65',newPaidCredits=0,
    instructions=[
        'Clean futuristic sans-serif end title and copyright.',
        'Advance final Harper video source by two seconds; keep cosmic source and fade 3:34–3:36.',
        'Make Travel27 sphere much darker; keep V64 reversed Travel28 unchanged.',
        'Same blue-cyan sphere refraction/tint on opening rear warp around 2:11.',
        'System view: swell a departure twinkle near the central world, then a small accelerating light on a curved escape trajectory.',
        'Gentle push and pan toward the planet side of the rear-view Harper shot.'
    ],clarification='User confirmed sandwich architecture: optics affect only the background, with unaltered ship and Harper composited in front.',preservedVersion='v64'))
print('Prepared V65, unchanged 2122-frame section, no new generations.',flush=True)
