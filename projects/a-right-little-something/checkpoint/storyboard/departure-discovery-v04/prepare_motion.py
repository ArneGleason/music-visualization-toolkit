"""Prepare exact clean-motion requests from the accepted V54 storyboard."""
import hashlib
import json
from pathlib import Path

BASE=Path(__file__).resolve().parents[3]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,v): p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
r=read(BASE/'shots/shotlist.json')
assert r['activeReviewEdit']=='v54'
shots={s['id']:s for s in r['storyboardProposals'] if s.get('batch')=='departure-discovery-v01'}
lock=shots['departure-002']['promptLock']
specs=[
 ('signing','departure-001',5,2595,70,25,
  'Medium two-shot at the berth. Harper makes one short fingertip signing gesture on the transfer panel, lifts her hand, and accepts the small control token offered by the existing slate-blue fin-eared owner. Owner releases it naturally. Calm practical agreement; neither speaks or grins. Stable hands, panel and established ship behind them. Camera almost fixed. Perform the clear signing and handover between seconds1 and3.8.',None),
 ('departure','departure-002',8,2665,140,7,
  'ONE CONTINUOUS EXTERIOR CAMERA PULLBACK, from provided first image toward the distant-station tail image. Start camera movement IMMEDIATELY, no static opening hold. Within the first0.75 seconds the sphere shrinks to less than half its initial apparent diameter; by1.5 seconds it is a small recognizable ship and Harper is no longer individually readable. Camera rapidly retreats farther through space, settling into enormous cosmic scale by5.5 seconds, then continues very slowly through the last2 seconds near the tail composition. Ship itself moves gently away from station toward camera like a careful new driver, while camera retreats MUCH faster. This is changing camera distance, never the spacecraft physically shrinking, growing, transforming or morphing. Station stays behind ship in depth and both recede together. Harper floats inside throughout; maintain full body, both shoes, gray outfit. Preserve EXACT starting ship model: one outer equatorial band, entry, single aft vertical engine ring, pole plates; no inner cockpit ring. No left-right broadside slide. No cuts, crossfades or dissolves, no blur hiding a geometry transformation. Stable stars, sensible perspective, no added planet.',
  'generated/storyboard/departure-discovery-v01/distant-station.png'),
 ('target','departure-003',5,2805,68,25,
  'Interior side-profile medium. Harper floats almost imperceptibly, studies the small distant point, then makes one precise fingertip touch to the existing sparse cyan control between seconds2 and3.5. The tiny target bracket responds with a gentle light pulse. Only stars outside; do not reveal a planet yet. Preserve face, hand anatomy, long sleeves and exact approved framing. Small breathing and eye movement, camera steady, no talking or lip-sync.',None),
 ('planet','departure-005',4,2946,48,25,
  'Clean full-frame remote view of the existing emerald-jungle and copper-sea planet. Very subtle coherent globe rotation and slow ivory cloud drift, with a delicate atmospheric rim. Keep the exact continent geography and framing recognizable; less than two degrees rotation over the take. Stars remain stable. No additional moons, objects, ship or HUD. No camera zoom; this is the resolved big-now reveal after the separate hard-cut magnification sequence.',None),
 ('cabin','departure-006',4,2994,45,25,
  'Wide cabin view. Harper remains a small figure, studying the magnified remote jungle planet on the virtual dome. Existing sparse cyan route line extends smoothly a little farther between seconds1 and2.5, indicating remaining travel distance. Minimal weightless body drift and one tiny hand adjustment. Planet stays a dome display, no arrival, no flying into it, no changing geography, no newly invented inner cockpit ring. Retain approved composition; camera steady.',None),
 ('affirmation','departure-007',4,3039,42,25,
  'Tight three-quarter reaction. Harper studies the discovery; focused eyes soften into restrained satisfaction, a tiny breath and almost-nod between seconds1 and2.7. Closed relaxed mouth, no broad smile, no speech. Keep mature freckled face, short auburn curls and warm-gray collar. Minimal floating hair movement; camera steady and stable face identity.',None),
 ('confirm','departure-008',5,3081,63,25,
  'Tight hand/control insert. The existing hand makes a single deliberate touch to the amber destination point between seconds1.3 and2.4; the sparse cyan course line settles into a single clear route and gives one restrained confirmation pulse. The hand relaxes and withdraws just a little. Preserve five-finger anatomy and gray sleeve. No additional hands or text, no dense HUD, no camera pan, no planet arrival.',None),
]
takes=[]
for name,sid,duration,start,frames,source_start,action,tail in specs:
    s=shots[sid]
    image=s['storyboardSegments'][1]['image'] if name=='planet' else s['storyboardSegments'][0]['image']
    elements=[] if name=='planet' else [{'id':'323570155312565','bindName':'Harper'}]
    identity='Harper <<<323570155312565>>> is the established adult woman. The starter image controls gray long-sleeved coverall and utility shoes, overriding identity-reference clothes. ' if elements else ''
    prompt=f'{duration} seconds. Clean silent single shot. '+identity+action+' Preserve the painted graphic-novel rendering and all approved starter designs. No montage, captions, readable words, watermark, generated audio or lip-sync. '+('The immediate pullback is essential; do not wait for a one-second static handle.' if name=='departure' else 'Allow one-second editing handles before and after the main action.')+'\n\n'+lock+'\n\nMOTION CONTINUITY: Only subjects in the starter and required action appear. The ship has no extra inner cockpit ring; the continuity-lock rail means its established outer equatorial structure. Keep character and ship scale constant in world space.'
    takes.append(dict(id='departure-'+name+'-motion-v01',shotId=sid,title=s['title'],startFrame=start,editFrames=frames,leadInFrames=source_start-1,leadOutFrames=duration*24-(source_start-1)-frames,sourceEditStartFrame=source_start,model='kling-video-v3_0',duration=duration,resolution='1080p',imageCount=1,enable_audio=False,prefer_multi_shots=False,tailImage=tail,firstImage=image,firstImageSha256=hashlib.sha256((BASE/image).read_bytes()).hexdigest(),prompt=prompt,elements=elements,estimatedCredits=duration*8,placements=[dict(shotId=sid,startFrame=start,editFrames=frames,sourceEditStartFrame=source_start)]))
    if tail: takes[-1]['tailImageSha256']=hashlib.sha256((BASE/tail).read_bytes()).hexdigest()
    assert takes[-1]['leadOutFrames']>=24
plan=dict(status='Prepared for clean generation; no submissions yet',fps=24,output='generated/kling-tests/departure-discovery-v01',reviewOutput='generated/storyboard/departure-discovery-motion-v01',estimatedCredits=sum(t['estimatedCredits'] for t in takes),priorConfirmedCumulativeCredits=3104,authorization='User requested all clean shots and assembly after accepting V54, with an immediate fairly quick departure-camera pullback. Exact upload/cost request will be handled by execution approval review.',shots=takes,stillShotIds=['departure-004'],stillSegments=[dict(startFrame=2873,endFrameExclusive=2946,reason='Nine accepted hard-cut magnification stills plus last-view resolving hold')],uploadCount=8,promptLock=lock,sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v54.mp4',assemblyNotes='Replace departure002 entire140frames with one continuous rapid pullback: no old dissolve or static far-station segment. departure005 begins with26frames of last zoom still then48frames planet native motion. Preserve all exact edit boundaries and master audio. Select actual action after native review; no silent paid retries.')
save(BASE/'kling-departure-discovery-v01.json',plan)
r['departureDiscoverySequence'].update(status='V54 accepted; seven clean motion takes prepared',motionRequest=dict(plan='kling-departure-discovery-v01.json',status='Prepared; not submitted',estimatedCredits=plan['estimatedCredits'],immediatePullback=True,keepNineZoomStills=True))
s=shots['departure-002']
s['motionDirection']='Immediate brisk camera pullback; no static opening dwell on simplified Harper. Sphere below half starting apparent diameter within0.75s, small by1.5s. Ship departs gently while camera retreats much faster. Preserve one equatorial band, floating Harper, true perspective and world-space scale. Reach distant-station composition without cuts or dissolves.'
for t in takes: shots[t['shotId']]['videoPrompt']=t['prompt']
save(BASE/'shots/shotlist.json',r)
out=BASE/plan['reviewOutput'];out.mkdir(exist_ok=True)
save(out/'assembly-plan.json',dict(sourceVersion='v54',targetVersion='v55',startFrame=2595,endFrameExclusive=3144,totalFrames=549,placements=[p for t in takes for p in t['placements']],stillSegments=plan['stillSegments'],noDissolveInDeparture=True))
print(f'Prepared {len(takes)} videos, {plan["uploadCount"]} still uploads, {sum(t["duration"] for t in takes)} seconds, estimated {plan["estimatedCredits"]} credits')

if __name__=='__main__': pass
