import json
from pathlib import Path

base=Path('projects/a-right-little-something')
register=json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))
shots=[s for s in register['storyboardProposals'] if s.get('batch')=='lab-verse-v02']
assert len(shots)==9
actions=[
 'Tight adult face through sealed growth-tank glass. Her eyes gently focus and make a small independent glance, lips relax, breathing and tiny floating auburn curls feel alive. Small culture bubbles rise. No speech or lip-sync. Keep the exact face, tank rib and concealed body. Locked camera; editorial pan will be added later.',
 'Wide growth-tank reveal. Harper floats quietly upright with tiny hair drift and breathing, body concealed by unchanged solid opaque tank armor. The bizarre ivory/graphite robotic caretakers make slow precise coordinated service motions outside: one tool tests the exterior cyan control and another makes a small tending sweep. The lab remains calm, no new chambers or people. Locked camera; editorial opening move will be added later.',
 'Medium close view of Harper INSIDE the sealed upper culture window. Her one raised natural hand at head level makes a small independent finger gesture. A regular internal cyan geometric lattice responds with a restrained asymmetric amber branching pulse, an authored-constraint malfunction. Outside, the ivory mantis tool depresses its external control once; it cannot touch her hand. Keep unbroken glass, liquid and bubbles over face and hand, forearm rising naturally from below inside. No portal, opening, cuff, wall penetration or chamber escape. Keep five fingers. Locked camera; editorial pan will be added later.',
 'Head-level calculation detail inside the sealed upper growth chamber. Exactly five natural fingers: thumb and index slowly pinch and rotate the small violet/cyan light ring, then settle one luminous node into alignment. Other three fingers respond with a tiny natural articulation. One coherent restrained geometric calculation changes continuously, no giant new screens or random interface rebuild. Harper eyes track the finger action behind it. All hand, forearm and light graphics remain inside culture fluid behind continuous glass, never outside, no cuff, port or opening. Small bubbles and floating curls. Locked camera; editorial pan will be added later.',
 'Concentration close-up of the same adult Harper inside culture fluid. Brow tightens slightly and eyes track a tiny calculation below her eyeline; a restrained violet/cyan geometric reflection shifts over cheek and eyes. A small resolved expression, subtle breathing and floating curls, rising bubbles. No talking, head swing, face change or newly visible body. Locked camera; a modest editorial push will be added later.',
 'Reveal the massive elongated submarine-like laboratory ark among stars. Make one slow smooth camera pullback by about fifteen percent over six seconds, keeping its entire exact graphite hull, oval cyan culture galleries, amber seams, asymmetrical service spars and cyan aft engine coherent. Gallery lights have subtle living activity, restrained drive energy and delicate illustrated bloom. Distant starfield stable, small nebula depth/parallax. Hull drifts gently forward, no turn or banking. A reveal of the laboratory vessel, no personal spherical ship, no geometry morph.',
 'Deep-space dark-sky view of the same laboratory ark. Smooth measured lateral camera drift to the right while the ark glides slowly toward the upper-right, leaving more empty deep indigo-black sky on the left. Distinct lateral travel rather than another pullback. Preserve the exact hull and spars, lit oval culture galleries and amber lines; cyan aft energy stays restrained. Distant stars stay far away, no high-speed warp streaks, spinning, banking or new worlds.',
 'So-bright cosmic-light interlude. From this exact starting composition, gently pan toward the bright star in the upper-right; let the unchanged laboratory ark gradually slip toward and partly beyond the lower-left edge. The visual attention passes from the hull to the luminous star and textured violet/cyan dust. Warm illustrated star bloom and subtle long luminous streaks evolve slowly, never strobing or becoming a blown-out white screen. Smooth functional motion, not a repeated ship zoom. Keep the same coherent ark while visible. No new spacecraft, planets or geometry changes.',
 'Bright-night vastness. The same tiny laboratory ark continues its slow diagonal journey toward the upper-right through the richly painted cyan/violet nebula. A very slow broad camera opening move, around eight percent over six seconds, makes cosmic space feel immense; faint layered dust parallax, steady far stars, softly breathing illustrated warm bloom. Ship remains small and fully coherent, with unchanged submarine-like hull, spars, oval cyan galleries, amber seams and cyan aft drive. No fast zoom, hard banking, warp trail or new objects.'
]
shared=' One uninterrupted six-second shot, motion established from the start and continuing through the whole clip so any central trim remains alive. No cuts, internal dissolves, zoom blur, shake, camera jiggle, readable text, captions, watermark or generated audio. Preserve the exact illustrated painterly graphic-novel finish of the starting still. The growth tank stays sealed; all human hands and internal virtual interfaces remain inside culture fluid behind unbroken upper glass; robots and physical controls stay outside. All chest, pelvis and buttocks remain hidden by the original opaque tank structure or framing. Preserve adult identity and natural anatomy.'
plan=dict(status='Prepared exact image/prompt uploads; user requested all nine Kling animations',fps=24,
 output='generated/kling-tests/lab-motion-v01',reviewOutput='generated/storyboard/lab-motion-v01',
 estimatedCredits=432,timingSource='Canonical DAWproject-derived shotlist frames1550–1958, 24fps; native source handles24frames each side.',
 authorization='User October10: do Kling shots for all nine accepted lab-verse stills. Exact uploads and estimated432credit charge presented for automatic approval review.',shots=[])
for shot,action in zip(shots,actions):
 item=dict(id=shot['id']+'-motion-v01',shotId=shot['id'],title=shot['title'],
   startFrame=shot['startFrame'],editFrames=shot['frames'],leadInFrames=24,leadOutFrames=24,
   model='kling-video-v3_0',duration=6,resolution='1080p',imageCount=1,enable_audio=False,
   prefer_multi_shots=False,tailImage=None,firstImage=shot['startingFrameDraft']['image'],
   prompt=action+shared+'\n\n'+shot['promptLock'],reviewNotes=shot['motionDirection'],estimatedCredits=48)
 if shot['id'] <= 'lab2-05':
   item['elements']=[dict(id='323570155312565',bindName='Harper')]
   item['prompt']='Harper <<<323570155312565>>> is the established adult woman in this exact starting still; match her face and keep her body concealed as shown. '+item['prompt']
 plan['shots'].append(item)
 shot['startingFrameDraft']['userSelected']=True
 shot['startingFrameDraft']['status']='User accepted v27 composition for Kling animation'
 shot['motionReview']={'notes':'Accepted still; prepared native animation. '+action}
assert len({p['prompt'].split('PROMPT LOCK:',1)[1] for p in plan['shots']})==1
(base/'kling-lab-motion-v01.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(base/'shots/shotlist.json').write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Prepared nine six-second 1080p jobs; estimated432 credits; no submissions yet.')
