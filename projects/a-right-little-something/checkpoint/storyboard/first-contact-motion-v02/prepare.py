"""Record the V62 review and prepare six narrowly scoped replacement takes."""
import copy
import hashlib
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
register=read(BASE/'shots/shotlist.json')
assert register['activeReviewEdit']=='v62'
if not (OUT/'prior-shotlist.json').exists(): save(OUT/'prior-shotlist.json',register)
shots={s['id']:s for s in register['storyboardProposals'] if s.get('batch')=='first-contact-v01'}
old=read(BASE/'kling-first-contact-motion-v01.json')
harper=next(s['elements'] for s in old['shots'] if s.get('elements'))
notes={
'contact-001':('replace','Side-on warp pulse fails. Replace first two cuts with one continuous rear-oblique departure composite.'),
'contact-002':('replace','Rear direction works but Harper disappears. Separate passenger/ship animation from the warp background.'),
'contact-003':('keep','Dark-side arrival works.'),'contact-004':('keep','Surface-selection image works.'),
'contact-005':('keep','Little-something creature reaction is great.'),'contact-006':('keep','Community reaction works.'),
'contact-007':('keep','Analysis works. Speaking can read as a voice interface; do not regenerate only to remove speech.'),
'contact-008':('keep','Surface survey retained.'),'contact-009':('keep','Finger interaction works.'),
'contact-010':('replace','Cyan wisp lacks context. Replace with creatures walking toward a canopy clearing, looking around/up.'),
'contact-012':('keep','Ground projection two-shot works.'),'contact-013':('keep','Homes through the trees work.'),
'contact-014':('replace','Tool pickup is not functional enough. Proposed replacement: creature lowers a woven home awning over its familiar belongings.'),
'contact-015':('keep','Seedfruit exchange works with things that I need.'),
'contact-016':('replace-motion','Both gliders must travel; one follows the other along the same path, no stationary flapping.'),
'contact-017':('local-polish','Keep native tidal footage, add a slight smooth Blender pan and pullout.'),
'contact-018':('keep','Highland creatures are great.'),'contact-019':('keep','Useful bridge repair illustrates the lyric and moves well.'),
'contact-020':('local-polish','Keep night settlement and add restrained star twinkles in Blender.'),
'contact-021':('keep','Creature portrait works.'),
'contact-022':('local-polish','Down-here insert feels long; subtle Blender camera movement and a shorter hold.'),
'contact-023':('keep','Projection and creature pairing works.'),
'contact-024':('extend','Eye glint is excellent; give it longer without moving the night-orbit or finale cues.'),
'contact-025':('keep','Ship back in orbit works.'),
'contact-026':('replace-motion','Avoid generating her face from a rear view. Keep her head facing the planet throughout.'),
'contact-027':('keep','First outro system vista works.'),
'contact-027-travel':('composite-test','Preserve current take as fallback. Separate ship plus Harper gently floating from warp trails; try simple composite first. Reflections deferred until this works.')}
entries=[]
for sid,(status,note) in notes.items():
    s=shots[sid]
    review=dict(version='v62',status=status,notes=note,source='User playback review and composite clarification')
    s.setdefault('userMotionReviews',[]).append(review)
    s['motionReview']=dict(notes=note,reviewStatus=status,reviewVersion='v62')
    if status=='keep':
        s['motionSelection'].update(userSelected=True,draftForReview=False,status='User retained in V62 review')
    entries.append(dict(shotId=sid,startFrame=s['startFrame'],endFrameExclusive=s['endFrameExclusive'],**review))
review=dict(id='first-contact-v62-review',sourceVersion='v62',entries=entries,
    globalDirections=['Use short fade transitions through the outro; preserve exact musical section timing.',
    'Simple two-plate warp composite first; defer synthesized reflected streaks on the ship.',
    'Keep earlier accepted footage and V62 as comparison.'],
    eyeTiming=dict(downHereEnd=4334,harperListensStart=4334,harperListensEnd=4371,eyeStart=4371,eyeEnd=4416,
        basis='Frame 4334 is DAW bar 69 beat 1. Retain 37-frame Harper projection; give the eye 45 frames instead of 27. Night orbit remains at 4416.'),
    tentativeEcologyFades=True,reviewedThrough='contact-027-travel')
save(BASE/'first-contact-v62-review.json',review)
register['firstContactSequence'].update(status='V62 reviewed; targeted V63 revisions in progress',reviewNotes='first-contact-v62-review.json')
save(BASE/'shots/shotlist.json',register)

lock='MOTION CONTINUITY LOCK: Preserve the exact visible subjects, proportions, materials, fine illustrated linework, palette and camera framing of the input. A single continuous silent full-frame 16:9 shot. Do not invent subjects absent from the image. No cuts, transitions, text, logos, new objects, extra limbs or transformations. Keep facial identity and anatomy stable. Only perform the specifically requested small motion.'
specs=[
 ('warp-rear-plate-v01','contact-001','Ship and Harper / opening rear plate',5,60,'ship-rear-chroma.png',
  'A locked effects-source plate. The entire spacecraft silhouette stays absolutely fixed in screen space: no flight, scaling, camera movement or rotation. Only Harper moves: gentle weightless body drift, a small relaxed knee bend and natural hair motion while continuously visible above and to the right of the engine. Her head remains facing forward away from camera for the entire take. No face reveal, no talking. The uniform magenta background remains perfectly uniform, including through all empty dome areas. Preserve thin cyan hexagonal lines and metal geometry. Do not add stars, trails, exhaust, scenery, floor, shadow or reflections. Keep the magenta key color unchanged and unlit. One second steady lead-in and lead-out.',True),
 ('warp-side-plate-v01','contact-027-travel','Ship and Harper / outro separate plate',4,34,'ship-side-chroma.png',
  'A locked effects-source plate. Keep the whole sphere and engine absolutely fixed in screen space. Only Harper floats a few centimeters gently inside, bends one knee a little, and lets her arms settle, with small natural curly-hair movement. She stays entirely visible and looks in her current forward direction away from camera throughout; no turn toward camera or speech. All empty background and transparent dome spaces stay perfectly flat vivid magenta. No warp streaks, stars, exhaust, floor, moving ship, shadows or reflections. Preserve the exact ship silhouette and hexagonal dome lines. One second lead-in and lead-out.',True),
 ('contact-010-motion-v02','contact-010','Creatures approach clearing',5,55,'creatures-clearing.png',
  'Both existing creatures walk naturally forward on all fours along the root path into the canopy clearing, taking two or three small coordinated steps. The nearer creature follows the farther one, each briefly looks toward the open sky. Gentle attentive curiosity, not running or panic. Camera remains almost locked and low. Keep four limbs per animal, fan crests, tail and facial proportions unchanged. Background homes and foliage remain stable. No cyan effects, light wisp, hologram, human, spacecraft or new animal. One second lead-in and lead-out.',False),
 ('contact-014-motion-v02','contact-014','Useful home awning',5,56,'home-awning.png',
  'The existing creature performs ONE small useful action: gently pulls the existing vine cord down with its raised forefoot, causing the attached woven leaf awning to unroll downward by a small amount over its home nook. Other three feet stay planted. The cord remains attached and taut, the hand keeps its grip. The bedding, basket and hanging tools remain stationary and recognizable beneath the shade. No tool pickup, fruit exchange, new object, human gesture, mouth movement or speech. Quiet practical familiarity, locked camera. One second lead-in and lead-out.',False),
 ('contact-016-motion-v02','contact-016','Two gliders following',4,26,None,
  'Both existing membrane-winged animals MOVE FORWARD across the valley. The nearer glider follows the leading glider along the same gently curving path from left toward right and into depth, like one chasing the other playfully. Their bodies translate smoothly through the air from the beginning; no hovering or stationary wing flapping. Mostly extended gliding wings with only a small corrective flex. Stable species, wing count and anatomy. Background canopy and valley retain their form, camera almost locked. No extra animal. One second lead-in and lead-out.',False),
 ('contact-026-motion-v02','contact-026','Harper keeps watching the planet',8,137,None,
  'Rear over-shoulder view of Harper watching the planet. Keep the BACK of her curly head toward camera for ALL eight seconds. She never turns around, never reveals her face, and never looks toward camera. Gentle weightless breathing and tiny hair motion, her existing hand makes only a small settling movement and then rests. Her attention stays on the correctly round planet. Preserve hexagonal dome lines and shoulder framing; no speech, new interface, additional ring, cockpit furniture or body change. Fixed camera. One second lead-in and lead-out.',True)]
plan=dict(status='Prepared from user V62 review; no jobs submitted',fps=24,output='generated/kling-tests/first-contact-motion-v02',reviewOutput=OUT.relative_to(BASE).as_posix(),
    promptLock=lock,priorPassCredits=1632,estimatedCredits=248,combinedEstimate=1880,shots=[])
for sid,shotid,title,duration,length,image,action,with_harper in specs:
    source=(OUT/image).relative_to(BASE).as_posix() if image else shots[shotid]['startingFrameSelection']['image']
    item=dict(id=sid,shotId=shotid,title=title,startFrame=shots[shotid]['startFrame'],editFrames=length,sourceEditStartFrame=25,
        leadInFrames=24,leadOutFrames=24,model='kling-video-v3_0',duration=duration,resolution='1080p',imageCount=1,
        enable_audio=False,prefer_multi_shots=False,firstImage=source,firstImageSha256=hashlib.sha256((BASE/source).read_bytes()).hexdigest(),
        prompt=f'{duration} seconds. Silent native 1080p. {action}\n\n{lock}',estimatedCredits=duration*8)
    if with_harper: item['elements']=copy.deepcopy(harper)
    if 'plate' in sid: item['tailImage']=source
    plan['shots'].append(item)
    (OUT/(sid+'.prompt.txt')).write_text(item['prompt']+'\n',encoding='utf-8')
assert sum(s['estimatedCredits'] for s in plan['shots'])==248
save(BASE/'kling-first-contact-motion-v02.json',plan)
print('Prepared 6 takes / 248 credits; stored user review without changing V62 timing or media.')
