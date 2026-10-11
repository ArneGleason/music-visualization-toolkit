"""Stage the two ejection stills at the user's 1:19 cut on the existing grid."""
import copy
import json
from pathlib import Path
import shutil

OUT = Path(__file__).resolve().parent
PROJECT = OUT.parents[2]

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

register_path = PROJECT/'shots/shotlist.json'
register = load(register_path)
shots = register['storyboardProposals']
prior = [s for s in shots if s.get('batch') == 'escape-approach-motion-v01']
assert len(prior) == 9, 'Register only once, preserving the pre-ejection edit'
generation = load(OUT/'generation-input.json')
for item in generation['items']:
    assert Path(item['destination']).stat().st_size > 0
save(OUT/'pre-ejection-shot-snapshot.json', prior+[next(s for s in shots if s['id']=='escape-001')])

lock = prior[0]['promptLock'].replace(
    'The pod exterior design is unresolved until the departure scene.',
    'Escape views use the enclosed ivory-and-graphite one-seat ovoid capsule derived from the boarding cabin; the tank is absent from the escape cabin.')
lock += '\n\n'+generation['promptLock']
batch = 'escape-ejection-v01'
for shot in prior:
    shot['batch'] = batch
    shot['promptLock'] = lock
    if shot['id'] != 'lab2-09':
        shutil.copy2(PROJECT/'generated/storyboard/escape-approach-motion-v01'/(shot['id']+'.mp4'), OUT/(shot['id']+'.mp4'))

night = next(s for s in prior if s['id']=='lab2-09')
night.setdefault('timingHistory', []).append(dict(version='v37', startFrame=1869,
    endFrameExclusive=1958, frames=89, reason='User moved the pod interior cut to exactly 1:19'))
night.update(endFrameExclusive=1897, frames=28,
    generationApproach='Reuse the opening of the accepted original-ship motion; shorten Bright night to the user-directed 1:19 cut.',
    motionDirection='Retain the original calm exterior, then cut into the secured escape cabin at frame1897 (79 seconds).')
selection = night['motionSelection']
selection.update(editFrames=28, availableLeadOutFrames=selection['sourceFrames']-(selection['sourceEditStartFrame']-1)-28)

interior_motion = '''Eight seconds, one continuous interior shot. Camera remains inside the compact escape cabin with a small smooth, purposeful lateral drift from Harper toward the side viewport. First about 3.5 seconds: Harper is already seated in the fixed cushioned chair, held by ordinary padded flight shoulder restraints; quiet breathing and a brief alert glance toward the window, hands below frame. Cabin structure and harness stay fixed. At about 3.5 seconds the cradle releases with one small believable inertial settling of her shoulders, without shake or violent recoil. The external graphite mother-ship hull, cyan gallery and docking lip begin sliding and receding across the side viewport as the capsule moves away. By about 5.7 seconds much more open starfield is visible and the mother ship is distinctly farther away. Keep the glass, ivory cabin, silver halter top, face and hairstyle unchanged. No lip-sync, strap fastening, finger gestures, suit change, tank, robots, interior transformation, cut, dissolve, zoom blur, audio or readable text. Release occurs during Leaving orbit in the planned edit, not before the interior is established.'''
exterior_motion = '''Six seconds, one continuous exterior shot. Start with the compact ovoid capsule already safely separated from the original massive graphite robot laboratory ship, as in the first frame. During the first 1.5 seconds extend the clearance gap smoothly along its present outward heading. Between roughly 1.5 and 3 seconds the pod performs one brisk, smooth bank with a small roll: its nose swings upward-right into open space, then the roll settles. From about 3 seconds accelerate decisively along that new upward-right arc, with restrained speed blur and a smooth camera follow that keeps the pod legible and lets the mother ship recede. The functional thin cyan-white ejection wake connects the initial departure direction to the release recess at first; as the heading changes, new wake follows the curved flight path. Brightest near the pod, the trail decays rapidly behind it into a long faint tail; it never becomes a tether, laser, solid line or spaghetti. Keep one pod, one unchanged mother ship, consistent hull proportions and coherent viewport/hatch/recessed drives. No abrupt kink, repeated spinning, teleportation, warp tunnel, sun, collision, debris, explosion, additional ships, cuts, dissolves, camera jiggle, audio or readable text.'''

interior = next(s for s in shots if s['id']=='escape-001')
interior.setdefault('directionHistory', []).append({k:copy.deepcopy(v) for k,v in interior.items() if k!='directionHistory'})
interior.update(batch=batch, title='Leaving orbit — secured inside the escape pod',
    description='At 1:19 Harper is secured inside the cabin; the robot ship falls away through the side window during Leaving orbit.',
    startFrame=1897, endFrameExclusive=2010, frames=113, startPhrase='lyr-030',
    lyrics=['Bright night.','Leaving orbit at the moment.'],
    sourceDirection='User: cut inside at1:19, shorten prior wide shot, show secured Harper and ejection through her pod window; use a new cabin-derived pod.',
    promptLock=lock, imagePrompt=generation['items'][0]['prompt'],
    motionDirection=interior_motion,
    cameraMove=dict(zoom=[1.015,1.04],panX=[.35,.65],panY=[.5,.5]),
    generationApproach='Two linked stills for timing/design review first. Prepared eight-second 1080p Kling interior take, one-second source handles each side; not submitted.',
    continuityConstraints=['Same adult Harper and silver top','Ordinary flight harness, hands cropped','Mother ship outside the sealed side viewport','Same warm ivory boarding cabin; no tank','New ovoid escape pod, distinct from opening spherical ship'],
    status='Generated starter frame in timing review; native ejection not generated',
    handles=dict(leadInFrames=24,leadOutFrames=24,status='Planned native source handles'))

exterior = dict(id='escape-002', batch=batch, title='Clear, bank and accelerate',
    description='The pod has cleared the mother ship; it gains distance, banks into a new heading and zings away with a rapidly fading curved wake.',
    startPhrase='lyr-032',startFrame=2010,endFrameExclusive=2105,frames=95,
    lyrics=['Moments count here.','Just perfect.','We\u2019ll make all.'],
    sourceDirection='User: exterior after visible clearance, trail between ship and pod, then spin/bank and zing away in another direction.',
    promptLock=lock,imagePrompt=generation['items'][1]['prompt'],motionDirection=exterior_motion,
    cameraMove=dict(zoom=[1.045,1.015],panX=[.5,.65],panY=[.5,.5]),
    generationApproach='Cabin-derived exterior still for review, followed by prepared six-second1080p Kling take with one-second source handles; not submitted.',
    handles=dict(leadInFrames=24,leadOutFrames=24,status='Planned native source handles'),
    continuityConstraints=['Exactly one original robot ship and one ovoid capsule','Clear the hull before the bank','Ivory/graphite cockpit, side hatch and twin recessed drives match interior','Fading functional wake, brightest at pod; no solar streaks'],
    status='Generated starter frame in timing review; native ejection not generated')
assert not any(s['id']=='escape-002' for s in shots)
shots.append(exterior)
for shot,item in zip([interior,exterior],generation['items']):
    image='generated/storyboard/escape-ejection-v01/'+shot['id']+'.png'
    shot['startingFrameDraft']=dict(id=item['itemId'],image=image,userSelected=False,
        status='Generated first-frame draft for ejection review',generationMode='built-in ImageGen',nativeWidth=1672,nativeHeight=941)
    shot['motionReview']=dict(notes='Starter still with a small editorial pan for timing. '+shot['description']+' Planned native action: '+shot['motionDirection'])
    item['status']='Generated and inspected; staged for user review'
save(OUT/'generation-input.json',generation)
current=sorted([s for s in shots if s.get('batch')==batch],key=lambda s:s['startFrame'])
assert len(current)==11 and len({s['promptLock'] for s in current})==1
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(current,current[1:]))
assert sum(s['frames'] for s in current)==2105-1550
save(register_path,register)

spec=load(PROJECT/'storyboard-escape-approach-motion-v01.json')
spec.update(id=batch,output='generated/storyboard/'+batch,
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v37.mp4',
    presentation='Accepted native laboratory/ship passage, shortened Bright night, then two ejection starter frames in full-song timing.',
    mediaLabel='Kling / Blender / ejection starter-frame timing draft',
    continuationNotes='V38 cuts into the secured escape cabin at1:19 (frame1897), carries Leaving orbit through2010, then an exterior clearance/bank/acceleration starter through2105. Both new shots are stills with editorial pans; native ejection motion is prepared but not generated. Earlier native footage, exact lyric timing, fades and original audio retained.',
    status='Two new starter stills staged for review; no paid departure jobs submitted',
    reviewUrl='http://127.0.0.1:8768/?v=v38',
    stillReviewUrl='http://127.0.0.1:8768/storyboard/escape-ejection-v01/review-board.html')
save(PROJECT/'storyboard-escape-ejection-v01.json',spec)

template=load(PROJECT/'kling-escape-approach-v01.json')['shots'][0]
takes=[]
for shot,duration in [(interior,8),(exterior,6)]:
    take=copy.deepcopy(template)
    take.update(id=shot['id']+'-ejection-motion-v01',shotId=shot['id'],title=shot['title'],
        startFrame=shot['startFrame'],editFrames=shot['frames'],duration=duration,
        estimatedCredits=duration*8,
        firstImage=shot['startingFrameDraft']['image'],prompt=shot['motionDirection']+'\n\n'+generation['promptLock'],
        reviewNotes='Prepared for first-frame/timing review. Preserve at least24sourceframes each side; final native window chosen after animation QA.')
    takes.append(take)
save(PROJECT/'kling-escape-ejection-v01.json',dict(status='Prepared only; awaiting review and approval for new paid batch',
    fps=24,output='generated/kling-tests/escape-ejection-v01',reviewOutput='generated/storyboard/escape-ejection-motion-v01',
    estimatedCredits=112,estimateBasis='Observed8credits/sec: eight-second64 plus six-second48; provider duration support checked read-only',
    authorization=None,shots=takes))
project_path=PROJECT/'project.json'
project=load(project_path)
project['production']['escapeSetup']=dict(approachShot='lab2-08',departureShot='escape-001',exteriorShot='escape-002',
    departureStartFrame=1897,exteriorStartFrame=2010,endFrameExclusive=2105,
    timingDecision='Latest user direction: cut inside at1:19, then exterior after Leaving orbit',
    podDesign='New compact ivory/graphite one-seat ovoid capsule derived from the accepted boarding cabin; first-frame design pending review',
    status='Two linked starter frames generated; native ejection motion not submitted',
    review=spec['stillReviewUrl'])
save(project_path,project)
save(OUT/'review-manifest.json',[
    dict(index=1,id='escape-001',title='1:19 — secured inside; release seen through the window',src='escape-001.png',href='escape-001.png',output='escape-001.png'),
    dict(index=2,id='escape-002',title='1:23.71 — clear the ship, bank, accelerate',src='escape-002.png',href='escape-002.png',output='escape-002.png')])
save(OUT/'review-options.json',dict(preset='detail-review',showCaptions=True,minTileWidth=640,title='Escape — linked interior and exterior starter frames'))
print('Registered1897-2010interior;2010-2105exterior; preserved eight prepared native shots')
