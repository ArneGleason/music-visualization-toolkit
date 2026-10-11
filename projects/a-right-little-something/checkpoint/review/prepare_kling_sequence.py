import copy
import json
import math
from pathlib import Path
import sys

base = Path(__file__).resolve().parents[2]
repo = base.parents[1]
sys.path.insert(0, str(repo/'tools'))
from timeline import MusicalGrid

def load(name):
    return json.loads((base/name).read_text(encoding='utf-8'))

def save(name, value):
    (base/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

register = load('shots/shotlist.json')
lock = next(s['promptLock'] for s in register['shots'] if s.get('promptLock'))
spec = load('storyboard-window-coast-v01.json')
spec.setdefault('timingHistory', []).append({'endPhrase':spec['endPhrase'], 'reason':'User confirmed chorus begins on lyr-015, October 10'})
spec['endPhrase'] = 'lyr-015'
spec['handlesFrames'] = 24
coast = next(s for s in spec['shots'] if s['id']=='space-011')
coast['replaceCreative'] = True
coast['description'] = 'One continuous direct VR alien-coast experience: Harper opens her arms and the shallow tide responds, then cut into chorus 1 on the question at frame 1046. No longer hold through the question.'
coast['sourceDirection'] += ' October 10 user correction supersedes the earlier hold: cut to chorus 1 at How much can you do with it all, frame 1046.'
coast['transition'] = 'Cut or proposed zoom-out blur into chorus1-01 at frame 1046; no hold through the question.'
coast['generationApproach'] = 'One eight-second 1080p take for 134 edit frames plus 24-frame handles each side. Gesture then tide; cut at the chorus entrance.'
coast['lyrics'] = coast['lyrics'][:2]
coast['actionBeats'] = coast['actionBeats'][:2]
save('storyboard-window-coast-v01.json', spec)

window = load('kling-window-coast-v01.json')
window.setdefault('timingHistory', []).append(copy.deepcopy(window['shots']))
for s in window['shots']:
    s['leadInFrames'] = s['leadOutFrames'] = 24
    if s['shotId']=='space-011':
        s.update(duration=8, editFrames=134)
        s['prompt'] = ('One continuous eight-second illustrated alien-coast performance matching the approved starting still. Harper <<<323570155312565>>> keeps her adult face, auburn curls, gray tee/trousers and bare feet. First second: breeze, curls, fronds and water already living. From source 1.0 to 3.3 seconds she opens both arms wide naturally, shoulders relaxed. From about 3.3 to 6.6 seconds broad shallow tide fronts draw across the peach flats, changing the wet/dry shoreline in response; no towering wave. Continue living movement through the last second. Stable human proportions and scale, two arms/two feet, face readable. Almost locked three-quarter camera. Preserve turquoise sea, dark blue spires, violet ribbed fans and small pearlescent six-legged shelled animals. No ship, field grid, headset, equipment, text, audio, automatic cuts or scene transitions.\n\n'+lock)
    s['duration'] = math.ceil((s['editFrames']+48)/24)
window.update(estimatedCredits=sum(s['duration']*8 for s in window['shots']), reviewSummary='Prepared revised coast ending at chorus entrance. One-second handles; no old question hold.', status='Authorized October 10, awaiting sequential generation after chorus')
save('kling-window-coast-v01.json', window)

by_id = {s['id']:s for s in register['storyboardProposals']}
motion = {
 'chorus1-02': 'Five-second continuous alien-coast action, almost locked low three-quarter camera. Harper <<<323570155312565>>> is kneeling as in the starting frame. During the first second water, curls, fans and small pearlescent shelled animals already move naturally. From source 1.0 to 1.9 seconds she carefully nudges one small loose dark-blue stone outward with the hand already beside the water gap, slightly widening the opening. From 1.7 to 3.3 seconds a visibly stronger thin turquoise stream flows through that gap toward the violet ribbed fan-frond colony; one frond gently opens in response. Harper watches with a warm curious expression and withdraws the acting hand slightly. Water and fauna continue moving through the final second. Keep the act modest and causal, not magical. Do not invent a new bank, change the coastline, multiply hands or make her rise. One stone moved, one little flow response; fauna wander but do not build elaborate channels yet. No ship, projection grid, tools, text, audio, camera cut, morph, blur transition or sudden zoom.',
 'chorus1-03': 'Five-second continuous follow-up on the same living alien coast. Harper <<<323570155312565>>> kneels left and observes, hands withdrawn and resting, subtle breathing, gaze and curls. Keep the water-channel intervention in place. From source 1.0 to 2.6 seconds two foreground pearlescent six-legged shelled animals use their forelegs to roll one or two tiny blue stones along the edge of the already existing low banks, opening small side gaps. From 2.2 to 3.7 seconds turquoise water visibly takes those side channels in a beautiful branching flow among violet ribbed fan-fronds. Harper responds with fascination and a hint of thoughtful uncertainty. All life and water continue through the tail. Keep structures low and tidal, not dams appearing from nowhere. No instant cities, seed device, duplicated limbs, deformed shells, time-lapse landscape replacement, ship, HUD, text, audio, automatic cuts or transition. Almost locked camera, natural consistent scale. If a tiny stone motion is subtle, flowing water and purposeful organism interaction must still clearly show the response.',
 'chorus1-01': 'Eight-second continuous intimate interior mission shot. Harper <<<323570155312565>>> floats attentively beside THREE luminous volumetric ecosystem globes as in the starting still. The turquoise coast with violet ribbed fan-fronds and pearlescent shelled tidal animals matches the shore; ochre fungal terrain and indigo luminous reef remain distinct. Keep their arrangement, scale and identity stable; very gentle rotation and tiny ecological movement within globes, no swapping or merging. During first second maintain living hair/face/projection motion. From source 1.0 to 3.2 seconds her already extended hand makes a small deliberate selecting gesture at the turquoise globe. From 3.0 to 6.2 seconds its rim gently brightens and the living water pattern subtly responds; she focuses on it with care and thoughtful responsibility. Continue float and soft motion through tail. Almost locked camera, warm upper-right rim light, only the existing dark metal amber/cyan rail for cabin context. Globe contents are projections, not literal neighboring planets. Preserve anatomy; no new equipment, dense dashboard, English labels, dialogue, audio, automatic cut or inter-scene transition.',
 'chorus1-04': 'Seven-second continuous cosmic wide matching the illustrated starting frame. Turquoise and peach living world below-left with dark blue rock islands and branching coastal light patterns; deep indigo-violet stars remain distant. Very gentle coherent orbital camera drift with visible slow surface/cloud movement, planet remains round and stable. From source 1.0 to 3.0 seconds a soft cyan/amber pulse travels outward along the existing sparse curves from the branching coast around the planetary limb. From 3.0 through 6.0 seconds a tiny bright traveling point continues outward along the long arc into space. Keep line paths sparse, elegant and stable rather than stretching planet geography. Background stars almost stationary at astronomical distance. Natural ongoing motion through handles. No newly invented ship, person, moons, HUD, text, audio, hard cut, zoom blur or wormhole. Keep the graphic-novel texture and beautiful warm upper-right light.',
 'chorus1-05': 'Eight-second continuous abstract cosmic echo composition matching the illustrated starting frame. Three distinct living worlds at different depths retain turquoise branching coast lower-left, ochre organic ridges upper-middle and indigo luminous reef at right. Distant stars and violet nebula retain their scale. Sparse cyan/amber route arcs remain as shown; do not add a dense network or uniform rings. First second: gentle cloud/surface drift and quiet path glow. From source 1.0 to 2.7 seconds an amber/cyan pulse leaves the turquoise world and opens its coastal pattern. From 2.7 to 4.3 seconds the pulse curves around the ochre world and its local pattern bends the path. From 4.3 to 6.7 seconds a cooler pulse reaches the indigo reef world and disperses into a diffuse luminous glow. Continue subtle motion through final second. No geography melting, explosive colonization, planets merging, character, ship, HUD, text, audio or automatic cut. Almost locked wide camera; this is poetic exploration and uncertain influence, not literal rapid physical planet travel.'
}
order = ['chorus1-02','chorus1-03','chorus1-01','chorus1-04','chorus1-05']
shots = []
for sid in order:
    s = by_id[sid]
    duration = math.ceil((s['frames']+48)/24)
    shots.append(dict(id=sid+'-motion-v01',shotId=sid,title=s['title'],model='kling-video-v3_0',duration=duration,resolution='1080p',imageCount=1,enable_audio=False,prefer_multi_shots=False,firstImage=s['startingFrameSelection']['image'],tailImage=None,startFrame=s['startFrame'],editFrames=s['frames'],leadInFrames=24,leadOutFrames=24,prompt=motion[sid]+'\n\n'+lock,**({'elements':[{'id':'323570155312565','bindName':'Harper'}]} if sid in order[:3] else {})))
plan = dict(status='User authorized October 10; sequential submission and review',fps=24,output='generated/kling-tests/chorus1-motion-v01',reviewOutput='generated/storyboard/kling-chorus1-motion-v01',estimatedCredits=sum(s['duration']*8 for s in shots),estimateBasis='Last observed eight credits per second at native 1080p without audio; live CLI has no quotation endpoint. Actual charge recorded on submission.',reviewTitle='Chorus 1 · Kling motion review',reviewSummary='Sequential motion tests with one-second source handles; exact lyric-grid edit lengths and original song audio.',reviewChecks='Check causal hand/water action, purposeful animal response, stable Harper/organisms, ecological continuity, globe identity and sparse cosmic paths.',shots=shots)
save('kling-chorus1-motion-v01.json', plan)
print('Prepared chorus:',plan['estimatedCredits'],'estimated credits; backfill:',window['estimatedCredits'],'estimated credits. No jobs submitted by preparation.')
