"""Prepare the reviewed concourse images for native motion and editorial wipes."""
import copy
import hashlib
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parents[3]
OUT = BASE/'generated/storyboard/station-concourse-motion-v01'
OUT.mkdir(exist_ok=True)
path = BASE/'shots/shotlist.json'
register = json.loads(path.read_text(encoding='utf-8'))
shots = [s for s in register['storyboardProposals'] if s.get('batch')=='station-concourse-v01']
lock = shots[0]['promptLock']
assert len(shots)==11 and all(s['promptLock']==lock for s in shots)
directions = [
    'Wide exterior. The small ivory escape pod glides slowly toward the existing docking inlet, diminishing its gap to the station. A few distant craft drift gently. Station geometry and starfield remain stable. Restrained smooth forward camera drift, no abrupt bank or docking impact. Keep the pod distinct from the moored ships. Arrival movement is underway from the first frame.',
    'Medium concourse view. Harper looks from the small directory toward the real departure berths, with a natural tiny head turn and a relaxed breath; a few distant travelers walk slowly. Keep directory graphics abstract and stable. Very restrained camera drift. Do not introduce the spherical personal ship. No tapping fingers or large gestures.',
    'Harper notices the promising ivory passenger shuttle and gives a small interested glance, eyes and expression brightening subtly. Quiet breath and natural tiny curl movement. Locked camera, ship and station remain fixed; no lip movement or spoken performance.',
    'Locked-off boarding-berth view of the approved three-part organic craft. Preserve EXACTLY the three connected jade shell structures and pale rounded ribs; no morphing, growth, breathing hull or unfolding. Only a gentle low-intensity amber hatch-seam light pulse and tiny distant station traveler movement. No ship translation, camera pan, zoom, shake or image slide. Keep it windowless and structurally unchanged.',
    'Locked-off boarding-berth view of the gold light-sail craft. Preserve all four triangular sails, diamond frame and opaque ivory cabin exactly; rigid sails in vacuum, no fabric flapping or deployment. Very subtle steady onboard light activity and tiny distant station traveler movement only. No ship translation, camera pan, zoom, shake, windows or image slide.',
    'The suspect ferry captain already holds an inviting gesture and makes a small eager beckoning motion toward the existing ferry doorway. Harper remains seen from behind, still assessing him. Preserve his face, ears, jacket, ferry patches and ramp. Camera locked; movement underway from the first frame. No dialogue, lip-sync, new limbs or ship movement.',
    'Close reaction. Harper is already unimpressed; a tiny eye shift and restrained change in the set of her mouth make her rejection legible immediately. Begin a small turn away, no exaggerated disgust. Captain and ferry remain behind her. Locked camera. No speaking or lip-sync.',
    'Harper walks calmly away from the ferry and captain along the existing public concourse, continuing in the direction already established by the still. Camera tracks her smoothly at walking pace with modest motion; captain and ferry recede. Keep her hands relaxed, natural alternating footsteps, same coverall and low shoes. No bag, no running, no interaction with strangers.',
    'Harper continues walking along the quiet outer walkway toward its far end. Camera follows at an unhurried steady pace; station ribs pass with gentle parallax. Same outfit and proportions, no luggage. Sparse background remains sparse. No early reveal of the spherical ship.',
    'Harper slows near the structural pier and notices the partial cyan engine-ring glow and amber ship edge. A small head turn and one or two cautious steps orient her toward the remote berth. Camera glides subtly with her but keeps the opening ship mostly occluded throughout this partial-discovery view. No new vessels or people.',
    'Reveal the established spherical personal ship at the quiet berth. Keep its exact graphite equator, top and bottom platforms, single vertical cyan aft engine ring and thin transparent geodesic field stable. During the first second Harper assesses it briefly; over the next roughly five seconds she walks along the existing access bridge and boards through its established access opening, passing behind the rim structure naturally. By about 6.5 seconds she has entered the ship; hold the vessel steadily for the remaining handle. Smooth gentle camera follow that retains the whole ship. No transformation, second sphere, extra engine rings, new crew, wardrobe change or takeoff. Do not turn the field into solid glass; faint cyan lines only.',
]
entries=[]
for index,(shot,direction) in enumerate(zip(shots,directions),1):
    duration=max(3,math.ceil(shot['frames']/24+2))
    person=index in {2,3,6,7,8,9,10,11}
    prefix='Harper <<<323570155312565>>> is the established adult woman; the starter image controls her warm-gray survival coverall, overriding any clothing in the identity reference. ' if person else ''
    prompt=(f'{duration} seconds, one uninterrupted clean shot. '+prefix+direction+
        ' Preserve the starting-frame composition and painterly graphic-novel finish. Maintain active subtle motion throughout the usable central portion, with one-second editing handles. No generated transitions, cuts, dissolves, wipes, captions, readable text, watermark, audio or lip-sync. The right-to-left ship wipes will be added later in editing; do not generate them.\n\n'+lock)
    image=BASE/shot['startingFrameDraft']['image']
    entry=dict(id=shot['id']+'-motion-v01',shotId=shot['id'],title=shot['title'],
        startFrame=shot['startFrame'],editFrames=shot['frames'],leadInFrames=24,leadOutFrames=24,
        sourceEditStartFrame=25,model='kling-video-v3_0',duration=duration,resolution='1080p',
        imageCount=1,enable_audio=False,prefer_multi_shots=False,tailImage=None,
        firstImage=shot['startingFrameDraft']['image'],firstImageSha256=hashlib.sha256(image.read_bytes()).hexdigest(),
        prompt=prompt,estimatedCredits=duration*8)
    if person:
        entry['elements']=[dict(id='323570155312565',bindName='Harper')]
    entries.append(entry)
    (OUT/(shot['id']+'.prompt.txt')).write_text(prompt+'\n',encoding='utf-8')
    for field in ('startingFrameDraft','startingFrameSelection'):
        shot[field].update(userSelected=True,status='User accepted stills and requested clean video generation')
    shot['motionDirection']=direction
transitions=[dict(incomingShot=s['id'],boundaryFrame=s['startFrame'],startFrame=s['startFrame']-2,
                  endFrameExclusive=s['startFrame']+2,frames=4,type='right-to-left vertical reveal',
                  featherPixels=64,edgeAccentPixels=3,edgeAccentOpacity=.22,
                  imageTranslation=False) for s in shots[3:6]]
register['concourseSequence']['motionRequest']=dict(status='Prepared for native generation',
    plan='kling-station-concourse-v01.json',transitions=transitions,
    direction='User accepted current stills; requested clean videos assembled with a right-to-left reveal edge, not sliding images.')
backup=OUT/'pre-motion-shotlist.json'
if not backup.exists():
    backup.write_text(path.read_text(encoding='utf-8'),encoding='utf-8')
path.write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
plan=dict(status='Prepared; no submission yet',fps=24,output='generated/kling-tests/station-concourse-v01',
    reviewOutput='generated/storyboard/station-concourse-motion-v01',estimatedCredits=sum(s['estimatedCredits'] for s in entries),
    estimateBasis='Last confirmed 1080p silent Kling3 rate 8 credits/sec. Durations 3–15 seconds verified with live CLI declaration October11.',
    authorization='User accepted the stills and explicitly requested clean videos and assembly. Exact upload/cost approval not yet separately recorded.',
    priorConfirmedCumulativeCredits=2472,shots=entries,transitions=transitions)
(BASE/'kling-station-concourse-v01.json').write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
print('Prepared',len(entries),'takes,',sum(s['duration'] for s in entries),'seconds, estimated',plan['estimatedCredits'],'credits')
