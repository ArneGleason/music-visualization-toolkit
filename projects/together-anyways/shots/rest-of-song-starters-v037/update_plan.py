"""Apply reviewed story revisions while preserving scene boundaries."""
import json
from pathlib import Path
from copy import deepcopy
P=Path(__file__).resolve().parents[2]
N=Path(__file__).resolve().parent
source=P/'shots/rest-of-song-v024/proposal.json'
backup=N/'proposal-before.json'
if not backup.exists(): backup.write_text(source.read_text())
q=json.loads(backup.read_text())
actions={
'S07-SH01':('A route around the checkpoint','From farther back, Harper and Taffy approach the cover beside the crossing. The same guard already stands at the position seen in Shot2. Harper spots the rear route, edges ahead and prepares to cross.','Wide establishing view of the exact Shot2 geography, pair smaller in frame; strong scale change into Shot2.'),
'S07-SH02':('Are you coming?','Harper beckons Taffy across while the stationary guard is distracted. Once together, both head away around the back of the port toward the remote salvage refuge, bypassing the sentry rather than passing through the checkpoint.','Retain existing starter. Show crossing and the pair turning away into the rear route.'),
'S08-SH01':('Together, then','In a deeply shaded unpatrolled back salvage nook, Harper offers the fake jewel. The scrapper knows it is fake but recognizes a missing piece for his collection; Taffy stays close.','Retain trade blocking; remote dark background and small portable lamp, no visible patrols or surveillance.'),
'S08-SH02':('The ship nobody wants','The scrapper accepts the jewel and reveals the hidden junker behind a salvage panel. His help includes pointing them toward a maintenance helper routine he previously planted in the port system; he does not install it on screen. Nobody patrols this remote recess.','Wider reveal in deep shade; ship interior mostly dark, no exposed upper security walkway.'),
'S09-SH07':('Lost it','The cartridge slips into the aperture of a broad powered sliding maintenance door below the repair bench. Harper misses the catch. It wedges between the opposing edges just as the closing cycle begins.','Clear view of the aperture, cartridge and moving door edges; same mechanism in S10SH01.'),
'S10-SH01':('No retrieving that','The powered maintenance door slams shut on the trapped cartridge, visibly buckling its casing and destroying its connector. The partners react; the scrapper points them toward a donor vehicle.','Starter shows cartridge trapped and just denting, before the final crushing stroke; do not start with the finished aftermath.'),
'S10-SH02':('An unattended donor','An ordinary yard mechanic pushes a parts cart away from an exposed donor vehicle. Harper and Taffy wait for the mechanic to turn away, then approach the open service bay and its visible teal module.','Establish the exact donor vehicle/panel used in next shot; departing mechanic is not the scrapper.'),
'S10-SH03':('Wrong part, useful part','At the same donor vehicle and exposed service panel, Taffy frees the teal substitute while Harper braces a tool and watches the departing mechanic. They take the mismatched part.','Closer angle preserves donor geometry, panel and module orientation.'),
'S10-SH04':('An improvised fit','At the same port-bench housing established in S09SH05, Harper fits the teal substitute with a braided right-angle adapter while Taffy steadies it. The test sputters, then steadies.','Match original mounting position, not a new compartment.'),
'S11-SH05':('Things left undone','Taffy straps down the improvised module while Harper checks the escape route and unfinished work. There is no time to enjoy the job or finish it properly.','Harper has empty hands; remove cushion/comfort-fitting business entirely.'),
'S12-SH03':('A helpful accomplice','At the second terminal Harper works with the scrapper’s planted maintenance helper. It suggests a sequence of glyphs. Taffy keeps lookout toward the patrol approach, ready to warn her.','Preserve terminal location and cover; simple amber helper symbol and green suggested path, no readable language.'),
'S12-SH04':('Set the trap','Harper and the helpful system arm a link from the pending clearance start to the port-control interruption. Taffy remains lookout. The helper offers a shutdown step that would break the live trigger.','Harper faces the system; Taffy does not reach for a plug.'),
'S12-SH05':('Do not turn it off','Harper urgently addresses the security system itself, asking it to keep the circuit powered. The helper pauses the shutdown and holds the armed indicator. Taffy stays lookout.','Natural hand on console or restrained plea gesture; correct wrist, no backward palm or hand-stop directed at Taffy.'),
'S12-SH07':('Their bad news, our opening','The demolition operator begins the clearance cycle. The familiar machine starts advancing and its signal triggers the prepared port-control outage.','Brief exterior trigger; use the machine from S11SH02 bulletin as vehicle anchor.'),
'S13-SH01':('Hang on','The ship scrambles out of concealment, knocking loose scrap aside and lurching clear of the yard while departure controls are down. Harper commits to launch; Taffy braces.','Rough, imperfect departure with readable acceleration, not a graceful hover.'),
'S13-SH02':('A city below them','The craft struggles timidly upward over the city and mine roads, with a little smoke and loose fragments. Its wobble begins to settle toward the end.','Climbing wide view tied to opening landmarks; keep faults readable without catastrophic failure yet.'),
'S13-SH03':('Almost free','At the opening high regional viewpoint the craft briefly steadies. It appears they may escape; give that hope a short pause before the failure.','Retain approved wide starter; shortened by one beat for the following reaction.'),
'S13-SH04':('The compromise fails','The substitute shakes loose and the warning lamp returns. In the wider cabin Harper and Taffy notice and turn toward it; thrust stutters, the cabin tilts and the descent begins.','Show module and both characters with believable port-bench/cockpit geography. Failure then reaction within the cut.'),
'S14-SH01':('The surface gives way','The ship hurtles down toward the apron beside the quarry, strikes hard and breaks through the buried ancient-city entrance. Dust swallows it. Its final orientation must match the wreck in Shot3.','Starter higher above intact ground with runway for approach during head handle. Preserve correct intake and sealed entry; impact damage develops in motion.'),
'S14-SH02':('Still together','In the tilted dusty cabin Taffy is briefly slumped with eyes closed. Harper shoves his shoulder; he stirs awake, showing that both survived.','Start before the rousing gesture, restrained concern, no visible injury.'),
'S14-SH03':('Only a few steps','The pair step away from the grounded wreck toward the vast buried city entrance. Taffy sweeps his flashlight toward a monumental beaked-ant ancestor statue.','Match crash site and wreck orientation; correct ship entry/intake; establish statue for next angle.'),
'S14-SH04':('Something noticed','Taffy raises the flashlight to the giant ancient statue, unmistakably an ancestor of the scrapper’s beaked ant species. Dormant lights begin to wake around it and the city entrance. End before they know what the response means.','Huge dignified four-armed ant-bird ancestor statue, tiny pair below. Starter mostly dormant; reveal activation in motion.')}
for s in q['shots']:
 if s['id'] in actions:
  s['title'],s['action'],s['camera']=actions[s['id']]
  s['reviewOverlay']=s['action']
 s['status']='starter_review_v037'
 if s['id']=='S12-SH07':s['endFrameExclusive']=4286;s['boundaryBasis']='start retained; split at DAW bar66 beat1 (178.588185s rounded to24fps)'
 if s['id']=='S13-SH03':s['endFrameExclusive']=4717
 if s['id']=='S13-SH04':s['startFrame']=4717;s['boundaryBasis']='DAW bar72 beat2 (196.532575s rounded to24fps)'
 s['frames']=s['endFrameExclusive']-s['startFrame'];s['seconds']=s['frames']/24
idx=next(i for i,s in enumerate(q['shots']) if s['id']=='S12-SH07')
b=deepcopy(q['shots'][idx]);b.update(id='S12-SH07B',title='Ready in the cockpit',startFrame=4286,endFrameExclusive=4353,frames=67,seconds=67/24,action='Harper settles at the flight controls while Taffy gets into the adjacent seat and braces. The cockpit confirms the departure window; they commit to leaving before the clearance machine reaches the hideaway.',camera='Interior two-shot, two occupied side-by-side seats, brisk physical preparation before launch.',boundaryBasis='DAW bar66 beat1; end retains Scene13 boundary');b['reviewOverlay']=b['action'];b['transitionInProposal']={'type':'cut','frames':0,'reason':'Exterior trigger to immediate cockpit response.','status':'proposed_not_applied'};q['shots'].insert(idx+1,b)
q['status']='starter_review_v037';q['note']='User revisions: covert geography, crushed cartridge, donor theft, helpful security routine, cockpit preparation and ancestral city. 39 planned shots. Existing active Scenes1–6 edit unchanged.'
assert len(q['shots'])==39
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(q['shots'],q['shots'][1:]))
assert sum(s['frames'] for s in q['shots'])==3234
for scene in q['scenes']:
 ss=[s for s in q['shots'] if s['sceneId']==scene['id']]
 assert ss[0]['startFrame']==scene['startFrame'] and ss[-1]['endFrameExclusive']==scene['endFrameExclusive']
import sys
sys.path.insert(0,str(P.parents[1]/'tools'))
from frame_review import load_lyrics
lyrics=load_lyrics(P/'generated/timeline.compiled.json',0,5190,0,24)
for shot in q['shots']:
 shot['indexes']=[line['label'] for line in lyrics if line['startFrame']<shot['endFrameExclusive'] and line['endFrameExclusive']>shot['startFrame']]
source.write_text(json.dumps(q,indent=2)+'\n');(N/'proposal.json').write_text(json.dumps(q,indent=2)+'\n')
print('39 planned shots, same3234frames and scene boundaries; split4286; failure4717.')
