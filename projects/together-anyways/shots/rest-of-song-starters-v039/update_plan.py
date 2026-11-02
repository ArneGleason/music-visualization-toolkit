"""Capture approved direction, grid-derived timing refinements and review starters."""
from pathlib import Path
from copy import deepcopy
import json
P=Path(__file__).resolve().parents[2]; N=Path(__file__).resolve().parent
q=json.loads((N/'proposal-before.json').read_text())
# Action / playable motivation. Keep each future video prompt confined to its own beat.
rows='''S07-SH01|Approach cautiously along the service lane toward the port; exchange a brief low-voiced remark while checking the guard and continuing forward.|Harper is purposeful and reassuring; Taffy is willing but nervous. Small cautious steps have a destination, not idle shuffling.
S07-SH02|Harper beckons hesitant Taffy across. He checks the larger adult guard, commits to his break and joins Harper; they angle toward the hidden rear route.|Taffy must overcome fear; Harper urges him with patient urgency. Guard stays occupied, unaware.
S08-SH01|Harper passes the blue jewel into the scrapper's receiving hand; it lights as he accepts it.|A quick recognition and pleased surprise from the scrapper; Harper reads acceptance. One clean handoff, no extra negotiation business.
S08-SH02|Holding the received jewel, the scrapper agrees and gestures to the unwanted ship. The pair turn and start down the clear aisle toward it as camera reveals its exterior.|He is quietly generous and appreciates what she gave him; they are hopeful and delighted. Keep four separate arms and the ship silhouette coherent.
S09-SH01|They enter the grounded ship and look around its cabin while moving inside.|Curious, relieved to have a place of their own; hopeful rather than apprehensive.
S09-SH02|Harper opens the small cabinet/inspection compartment already under her hand; a few harmless bits of old junk tumble out. Taffy lights the discovery.|Both find the quirks amusing and remain pleased; no alarming failure or cartridge handling.
S09-SH03|Taffy experiments with the door-side buttons. Harper notices, tells him to stop randomly flipping switches, and he sheepishly pulls his hand away.|His eager curiosity outruns caution; her gently authoritative response says they need to understand the ship first.
S09-SH04|Harper studies the old cockpit controls, tries a control herself and presses it on the sung True at the existing lyric anchor near frame2507. A few local dashboard indicators light.|Amused confidence with a hint of hypocrisy after scolding Taffy. This is limited local power, not the full ship startup. End with pleased discovery.
S09-SH05|Harper directs Taffy to raise the portable light; he lifts it and angles the beam so she can inspect the overhead fitting.|She is intent on seeing the latch; he is earnestly helpful. Her small higher gesture motivates his action.
S09-SH06|At the repair housing they work to pry the stuck original regulator loose. Resistance gives way, sending the cartridge flipping upward out of their grip.|Cooperative effort turns to sudden surprise. This is the original part that will be lost, not the later scavenged replacement.
S09-SH07|The loose cartridge falls into the exposed powered linkage and lodges between the gears/jaw.|They reach too late and freeze at the jam. Follow the part's clear trajectory into the established mechanism.
S10-SH01|Taffy confidently throws the nearby release switch to free the jam. It drives the mechanism shut instead, crushing the cartridge. Harper recoils and touches her forehead in disbelief.|Taffy's certainty collapses into guilty surprise; Harper's exasperation is affectionate but immediate. Scrapper is absent.
S10-SH02|They watch the exposed donor bay and quietly confer while its human mechanic walks away with the cart.|Assessing an opportunity, keeping inconspicuous; they move only after the worker clears the bay.
S10-SH03|They carefully extract the usable substitute module from that same donor bay.|Quick, coordinated opportunism, checking the departed worker's direction before committing.
S10-SH04|Back in their ship they seat the substitute into the established housing with its improvised adapter and secure it.|Relief at a workable fit, concentrated cooperation. Preserve module and housing geometry.
S10-SH05|With the installation complete the ship stirs to life: panels and systems wake in sequence.|Their hope rises as each response confirms progress; a little uneven vibration keeps the old ship believable.
S11-SH01|They run further diagnostics, make useful adjustments and bring the monitor online.|Growing competence and satisfaction; work is going well.
S11-SH02|The newly working screen reports imminent demolition of this salvage area.|Attention shifts from successful diagnostics to unwelcome news. Keep the machine recognizable.
S11-SH03|The bulletin cuts to guards taking away their scrapper ally.|Show the arrest clearly on the screen; do not invent a camera pullback that reconstructs absent protagonists.
S11-SH04|Taffy works hard on urgent remaining repairs. Harper checks his progress, rises and leaves frame toward the rear cabin to tackle another task.|The news has made them hurried and purposeful. No idle watching; Harper exits decisively while Taffy continues.
S11-SH05|Taffy keeps working on another fitting while Harper checks the doorway and thinks through their exit problem.|Taffy is absorbed in readiness; Harper's worried scan becomes an idea. No bag or cushion business.
S11-SH06|Inside the unmistakable ship cabin Harper traces a sabotage route on a horizontal tabletop plan; Taffy works farther away.|Harper is calculating a way out, quietly decisive. Distinguish this planning image radically from the exterior port terminals that follow.
S12-SH01|At the first port terminal Harper tests access while Taffy stands lookout.|She is focused under pressure; he actively scans approaches. Establish they have left the ship.
S12-SH02|Harper works through rapidly changing glyph combinations. The machine shifts from neutral responses to a responsive helper persona, recognizes her intent and indicates the next terminal.|Frustration gives way to surprised rapport and trust. Express personality through coherent glyph pulses and helpful responses, not a new physical robot or human face.
S12-SH03|At the next terminal Harper follows the helper's route and continues the override while Taffy watches the port.|A cooperative exchange with the system; she is quicker and more confident now, he remains vigilant.
S12-SH04|The guard initially faces their general direction but does not notice or recognize them. He casually turns away and wanders off along a different route. Taffy spots him, quietly warns Harper, and she finishes the live sabotage while keeping inconspicuous.|Guard is distracted and unaware, not suspicious or pursuing. Taffy reacts to the risk; Harper stays controlled and focused. His turn and departure must read clearly during the shot.
S12-SH05|They slip away covertly from the live terminal. Harper looks back toward the guard and murmurs Don't turn it off as a desperate wish that the sabotage is left running.|An anxious almost superstitious plea to the situation, not an instruction to Taffy or a literal magical spell. Guard must not actually shut it off in this shot.
S12-SH06|They hurry back to the ship's entry and climb aboard.|Suppress panic but move with purpose; the task is getting inside before clearance starts.
S12-SH07|The approaching demolition machine rolls forward and crushes or pushes loose debris out of its way.|Show its heavy destructive force in this brief cut; the already planted clearance trigger interrupts port control.
S12-SH07B|In the cockpit they fasten their belts. Harper presses startup controls and calls urgent instructions; Taffy braces and responds.|Committed, energized urgency. Two side-by-side occupied seats, clear physical preparations.
S13-SH01|The ship clatters out of the salvage recess, knocking debris aside and shedding a few loose nonessential panels as it lifts.|An untidy escape under pressure; maintain the approved airframe and fixed nose bowl.
S13-SH02|The ship struggles upward over the port with intermittent smoke, sputtering and a few loose fragments.|It is gaining height despite strain; ascent remains readable rather than hovering in place.
S13-SH03|The climb steadies and the way ahead appears clear, revisiting the opening landscape from high altitude.|A brief release of tension: they seem to be making it away. Do not trigger the decisive failure until the next shot.
S13-SH04|Taffy tries to keep the substitute module stable while Harper watches. The scavenged part fails with a burst of smoke; both react as power drops.|His concentrated effort becomes alarm; her watchfulness turns to decisive emergency response. Preserve visible actors and established module location.
S13-SH05|The ship visibly loses powered climb and descends toward the mine region.|An unpowered falling trajectory with residual momentum; geography connects to the opening and the landing.
S14-SH01|The ship tilts slightly into hard ground contact and continues skidding forward for a considerable distance.|Keep momentum and weight. Cut away before any final collision or breakthrough needs to be shown.
S14-SH02|In the dusty aftermath Taffy is slumped apparently unconscious. Harper checks him and nudges his shoulder; he wakes and responds.|Her fear turns to relief; his dazed response confirms survival. Keep it brief and physical.
S14-SH03|They leave the resting craft and take a few tentative steps toward the revealed underground city.|Awe and caution replace escape urgency. The wider view explains their new surroundings.
S14-SH04|They approach the monumental beaked-ant ancestor statue. Taffy raises the flashlight up it; lights and dormant systems activate around the statue.|Curiosity turns to alert uncertainty. Reveal a response to their presence and end on the unresolved new adventure.'''
D={}
for line in rows.splitlines():
 k,action,acting=line.split('|');D[k]=(action,acting)
for s in q['shots']:
 s['action'],s['acting']=D[s['id']];s['reviewOverlay']=s['action'];s['status']='direction_review_v039'
 s['motionPrinciple']='Natural-speed motivated action with a changed end pose; camera supports the actor objective. Keep the main beat inside the edit, with24frame handles each side.'
# DAW grid: bar39beat3 =103.097663sec; bar54beat3 =145.819212sec.
by={s['id']:s for s in q['shots']}
by['S09-SH03']['endFrameExclusive']=2474
by['S09-SH04']['startFrame']=2474
by['S09-SH04']['boundaryBasis']='DAW bar39beat3,103.097663s rounded to24fps; local button light on True near2507 retained'
by['S09-SH04']['indexes']=['L30','I31','L31']
by['S11-SH03']['endFrameExclusive']=3500
b=deepcopy(by['S11-SH03']);b.update(id='S11-SH03B',title='They have taken our ally',startFrame=3500,endFrameExclusive=3525,action='Cut back to Harper and Taffy watching the screen, visibly troubled by the arrest and demolition news.',acting='A short shared look of alarm and recognition: their ally is gone and time is running out.',camera='Interior reaction two-shot using the news-viewing setup; both characters present in the starter.',boundaryBasis='DAW bar54beat3,145.819212s rounded to24fps; retains prior end3525')
b['reviewOverlay']=b['action'];q['shots'].insert(q['shots'].index(by['S11-SH03'])+1,b)
for s in q['shots']:
 s['frames']=s['endFrameExclusive']-s['startFrame'];s['seconds']=s['frames']/24
 if s['id'] in ['S10-SH02','S10-SH04','S12-SH01']:
  s['transitionInProposal']={'type':'wipe','direction':'left-to-right','softEdge':True,'frames':8 if s['id'].startswith('S10') else 12,'reason':'Elapsed travel/location change; wipe makes the omitted journey explicit.','status':'proposed_not_applied'}
 if s['id']=='S11-SH06':s['camera']='Wide oblique onboard tabletop-plan composition, Taffy farther back working; distinct from exterior port terminals.'
 if s['id']=='S12-SH04':s['camera']='Guard-oriented threat cutaway with warning Taffy and Harper/service terminal in geographical context.'
 if s['id']=='S12-SH05':s['camera']='Covert withdrawal, anxious glance back at guard and live terminal; natural hands, no literal spell.'
 if s['id']=='S09-SH04':s['camera']='Retain control close-up; longer lead-in explores controls before the True button/light beat.'
q['status']='direction_and_starter_review_v039';q['note']='40shots. User-approved v038 except six new/revised starters. Full acting pass,3proposed wipes, grid-derived S09 timing redistribution and S11SH03B. No footage generated.'
assert len(q['shots'])==40 and sum(s['frames'] for s in q['shots'])==3234
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(q['shots'],q['shots'][1:]))
for path in [N/'proposal.json',P/'shots/rest-of-song-v024/proposal.json']:path.write_text(json.dumps(q,indent=2)+'\n')
lines=['# Direction pass v039','','40 shots;1956–5190 at24fps. All scene boundaries unchanged. No Kling generation or active animatic replacement.','','## Timing and interpretation','','- S09SH03 now81f/3.375s; SH04 now52f/2.167s. Split2474=DAW39.3; press/light on True near2507.','- S11SH03 now49f/2.042s; new SH03B25f/1.042s. Split3500=DAW54.3.','- Onboard planning reference called scene12shot6 in dictation is S11SH06, before the exterior sabotage.','- Original regulator is pried loose and lost in S09; scavenged substitute appears in S10.','- Proposed soft wipes into S10SH02, S10SH04 and S12SH01. Handle overlaps preserve the music timeline.','- Limited local indicators may light in S09; full systems startup remains S10SH05.','- S12SH05 now pleads that the guard leave the sabotage on; no literal magic.','','## Shot direction','']
for s in q['shots']:
 lines += [f"### {s['id']} · {s['title']}",'',f"{s['startFrame']}–{s['endFrameExclusive']} · {s['frames']}f / {s['seconds']:.3f}s · {', '.join(s['indexes'])}",'',s['action'],'','Acting: '+s['acting'],'','Camera: '+s['camera'],'','Transition: '+json.dumps(s['transitionInProposal']),'']
(N/'scene-and-shot-directions.md').write_text('\n'.join(lines)+'\n')
# Prompt-ready shot direction pack; source handles remain explicit and are not a request to generate.
(N/'motion-prompts.json').write_text(json.dumps({'status':'draft_for_review_not_submitted','fps':24,'shots':[{'id':s['id'],'editFrames':s['frames'],'handles':s['sourceHandles'],'direction':s['action'],'acting':s['acting'],'camera':s['camera'],'pacing':s['motionPrinciple']} for s in q['shots']]},indent=2)+'\n')
print('40 shots;3234frames;timing refinements and acting saved')
