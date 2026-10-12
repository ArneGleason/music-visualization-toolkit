"""Prepare the authorized 37-source V61 Kling pass without submitting jobs."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
register = json.loads((BASE/'shots/shotlist.json').read_text(encoding='utf-8'))
estimate = json.loads((BASE/'kling-first-contact-cost-estimate-v01.json').read_text(encoding='utf-8'))
canonical = {s['id']: s for s in register['storyboardProposals'] if s.get('batch') == 'first-contact-v01'}
assert register['activeReviewEdit'] == 'v61' and len(canonical) == 36
lock = canonical['contact-001']['promptLock']
assert all(s['promptLock'] == lock for s in canonical.values())

motions = {
 'contact-001': 'Locked wide side view. During seconds1.0 to1.7 the compact cyan warp pulse around the existing aft drive intensifies, briefly bends the nearby star light, and launches the intact sphere forward in its established direction. One restrained pulse, no explosion. Ship and floating Harper retain their shape and size; no new ring or portal.',
 'contact-002': 'Rear chase camera travels behind the intact sphere at nearly constant distance. Long cyan and ivory warp streaks flow backward past the ship as it advances toward the tunnel vanishing point. Keep the single aft engine in its original place; faint Harper stays inside. Immediate steady travel, no camera orbit or cut.',
 'contact-003': 'Slow wide approach toward the night-side orbital limb. The tiny sphere advances gently while the vast planet remains a correctly round stable globe. One sun gradually peeks just past the far edge, strengthening the diamond-ring flare and thin atmosphere. Preserve astronomical distance; no growth of the ship or second sun.',
 'contact-004': 'Tight hand insert inside the established hexagonal sphere. Keep the large three-dimensional floating terrain relief from the starter. One fingertip selects a valley; a delicate cyan ripple spreads over the terrain and a small region brightens. Stable hand anatomy, one slow precise gesture. No real planet in the background, no new cockpit or flat touchscreen.',
 'contact-005': 'Intimate creature portrait. It gently raises its curious gaze toward the existing tiny sky glint, with one slight fan-crest twitch and natural breath. Keep the same amber eyes, blunt muzzle and nonhuman quadruped anatomy. Calm interest, not fear or speech. Almost locked camera.',
 'contact-006': 'Wide view from behind the foreground creature. The companions look toward the canopy opening, then briefly toward one another; one makes a small inquisitive forefoot gesture. A tiny cyan sky point twinkles once. Leaves move gently. Preserve the number and anatomy of creatures and the rooted settlement. No giant ship in the sky.',
 'contact-007': 'Medium interior view. Harper floats calmly INSIDE the same hexagonal sphere, studying the large volumetric terrain map. She slowly spreads two fingers to enlarge one local valley slightly, then settles into attentive observation. Map remains three-dimensional and below her eyeline, not another planet. Stable dome facets, no outside planet or new ship interior.',
 'contact-008': 'Slow smooth aerial survey along the jungle valley toward the tiny woven settlement. Gentle depth parallax in nearer treetops and flowing copper river. Preserve the terrain and dwelling layout; no objects grow into a city, no holographic interface or people appear in front of the lens.',
 'contact-009': 'Close cabin portrait. Harper notices something on an offscreen survey down-right; her eyes focus, expression changes subtly from concentration to recognition, and her already raised hand begins a small deliberate contact gesture. No broad smile or speaking. Camera nearly locked; preserve faint HEXAGONAL dome lines and dark space.',
 'contact-010': 'Ground-level settlement view. The existing thin cyan haze slowly gathers above the root at frame right; the main creature turns its head toward it and nearby companions pause. Friendly quiet curiosity. The glow stays a delicate abstract haze throughout; DO NOT reveal a human silhouette or Harper in this shot.',
 'contact-011': 'Maintain the cool low-angle side-profile creature composition and open sky. The creature turns its gaze a little toward the offscreen visitor and makes a small calm forefoot gesture suggesting an answer. Its fan crests and throat shift naturally with breath. No lip-sync, human posture, new projection or camera reversal.',
 'contact-012': 'Reverse two-shot of the translucent cyan Harper projection and the small creature. Harper holds the tiny sphere-ship icon gently above her open palm; the creature makes a small courteous declining forefoot gesture. Her entire figure remains see-through, with roots visible behind her. No physical contact, no opaque body, no additional limbs or dialogue. Locked framing.',
 'contact-013': 'Creature point-of-view across the home valley. A gentle forward camera drift reveals the existing rooted homes, tended gardens and flowing river, with small natural leaf motion. Preserve the wide landscape; no new Harper, close creature portrait, spacecraft or holographic interface.',
 'contact-014': 'Tactile close insert. The familiar nonhuman forefeet carefully lift the existing little wooden gardening tool, turn it a little, and hold it with quiet familiarity beside the basket and river stone. Keep the exact tool and forefoot anatomy, no human fingers. Background seedlings stir softly; locked camera.',
 'contact-015': 'Warm home garden medium-wide. The companion calmly passes the existing ripe seedfruit to the main creature, who receives it with its dexterous forefeet. One clear unhurried exchange, stable quadruped bodies and object count. A small friendly head acknowledgment, no ceremony, eating or new characters.',
 'contact-016': 'Wide living canopy. The existing small membrane-gliding animals glide naturally through the open space between branches while epiphytes and leaves sway gently. Subtle forward camera drift and river shimmer far below. Preserve the original species; no birds, humans or community creatures added.',
 'contact-017': 'Low tidal-flat view. Shallow copper water ripples through mineral channels; the existing shelled fan-feeders slowly open and close their feeding fans. A gentle lateral camera drift emphasizes the low shore. Keep the same organisms and terrain, no new giant creature or ocean wave.',
 'contact-018': 'Wide cold highland. The existing shaggy six-legged grazing animals take small natural steps and graze among low red-gold plants. Light wind moves fur and vegetation; distant clouds drift imperceptibly. Restrained camera glide, stable mountains and limb count, no warmer jungle or new herd.',
 'contact-019': 'Medium community scene. The two established creatures use their dexterous forefeet to tighten and place an existing woven bridge strand together, then inspect their modest repair. One small cooperative task. Keep the bridge geometry, four limbs per creature, and quiet root-settlement background.',
 'contact-020': 'Hold the expansive ground-up twilight composition. Leaves and small settlement silhouettes move softly, warm home lights glow, and the first stars become slightly more perceptible. Very slow upward camera drift at most, preserving the canopy silhouette. No accelerated day-night timelapse, aurora, spacecraft or new planet.',
 'contact-021': 'Quiet close creature portrait under the night canopy. Gentle breath, one natural blink, a small assured head movement and relaxed fan crests convey belonging. Preserve intelligent warm amber eyes and original nonhuman anatomy. No exaggerated smile, tears, human lips or lip-sync. Camera remains almost fixed.',
 'contact-022': 'Extreme low forefoot insert. The creature settles its existing forefoot gently on the mossy root; nearby tiny bioluminescent organisms flicker softly and leaves move a little. Tactile grounded contact, no digging or additional foot, no human hand. Locked close framing.',
 'contact-023': 'Close portrait of Harper AS A TRANSLUCENT CYAN HOLOGRAM in the night settlement. She listens, makes one small accepting nod, and relaxes into quiet understanding. Trees and home lights stay visibly transmitted THROUGH her face and shoulders. Preserve identity and transparent effect; no physical body, broad grin or speaking.',
 'contact-024': 'Extreme macro of the creature amber eye. Tiny natural eye movement and faint breath in surrounding skin; the single cyan reflected point gives one subtle glint. Keep the eye open for the usable beat. No new reflection scene, detailed ship, tears or transformation. Locked macro camera.',
 'contact-025': 'Very wide night orbit. The tiny intact sphere moves gently along the existing atmospheric limb against vast dark land and clouds. The camera drifts slowly with it. Maintain astronomical scale, faint sphere design and one drive ring; no giant spacecraft, sunrise or extra planet.',
 'contact-026': 'Close rear over Harper shoulder INSIDE the sphere. She floats quietly watching the correctly round planet, slowly turns her head a few degrees toward a distant possibility, and lightly settles her raised hand. Preserve the hexagonal dome, original shoulder framing and open cabin; no rectangle grid or new cockpit furniture. Slow restrained camera drift.',
 'contact-027': 'Wide system view, gentle camera retreat into space. Preserve the warm sun and distinct distant worlds at their enormous separations. Very subtle planetary cloud motion and soft star glow. No fast orbiting, planets swelling, new ship, people or graphic interface.',
 'contact-027-travel': 'Keep the starter rear-oblique sphere framing. Ship flies forward along the existing cyan and amber streaks toward the vanishing point. Camera tracks with it; nearby light streaks pass backward. Harper remains floating inside. Do not spin the ship, reverse direction, add a drive ring or cut to a destination.',
 'contact-028': 'Serene binary-sun vista. Gentle camera drift past the dark rust planet crescent; amber and blue-white suns retain their exact separation and astronomical depth. A little restrained coronal light motion, no rapid star orbit, new spacecraft or explosion.',
 'contact-028-travel': 'Follow the starter ship perspective into the violet and copper stellar dust ahead. Smooth purposeful forward flight, light trails sliding backward, one continuous camera path. Keep the intact single-ring sphere and Harper inside. No new destination, close portrait, ship morph or change of travel direction.',
 'contact-029': 'Slow forward glide into the existing layered dusty stellar nursery. Near dust filaments show subtle depth parallax and newborn blue stars glow steadily. Keep the grand scale, dark negative space and established cloud forms. No turbulent smoke boiling, new planet, ship or people.',
 'contact-029-travel': 'Tight off-axis rear chase of the intact sphere toward the existing distant red glow. The aft drive shines steadily while tapered cyan streaks flow backward. Camera maintains the starter distance and angle. Harper stays inside; no rotation, extra ring, planet reveal or cut.',
 'contact-030': 'Quiet wide red-star system. A very gentle camera drift past the small slate rocky world, restrained deep-red stellar glow and faint distant dust parallax. Preserve stable astronomical scale and sparse composition. No new planet ring, ship, characters or sudden flare.',
 'contact-030-travel': 'High wide oblique view. The small recognizable sphere follows its existing curved cyan wake toward the far starcloud. Smooth continuous forward travel; camera remains wide and calm so the ship stays tiny. Preserve the single sphere and faint Harper inside; no closer hero shot or new planet.',
 'contact-031': 'Grand oblique galactic view. Very slow forward camera drift, subtle depth in starclouds and a faint cyan brightness pulse traveling along the existing few exploration threads. Preserve the spiral composition and countless distant stars. No new path network, map labels, ship or face. This is the last vista before the editorial Harper overlay.',
 'cosmic-background': 'Independent COSMIC BACKGROUND PLATE ONLY. A slow continuous forward glide along the existing delicate cyan path toward the distant warm-white star, through stable deep indigo and copper cosmic dust. Gentle parallax, quiet luminous destination. Hold the starter composition throughout. NO Harper, people, faces, portraits, silhouette, double exposure or superimposition; those will be added separately in Blender.',
 'harper-portrait': 'Independent HARPER PORTRAIT PLATE ONLY. Tight close-up in the exact starter position at left. Harper slowly looks up and right with quiet awe, subtle natural breathing, small eye movement and one or two restrained blinks. No speech, grin, big head turn or drifting out of frame. Keep the original near-black seamless background completely dark and empty throughout; no stars, ship, planet, cosmic scenery, lighting flashes or double exposure. Fixed camera. This portrait will be superimposed in Blender later.',
}
harper_ids = {'contact-001','contact-002','contact-007','contact-009','contact-012','contact-023','contact-026',
              'contact-027-travel','contact-028-travel','contact-029-travel','contact-030-travel','harper-portrait'}
shots = []
for item in estimate['sourceVideos']:
    shot = canonical[item['shotId']]
    assert (shot['startFrame'],shot['frames']) == (item['startFrame'],item['editFrames'])
    key = item['plate'] if item['plate'] != 'main' else item['shotId']
    first = BASE/item['firstImage']
    assert first.is_file()
    seconds = item['sourceSeconds']
    identity = ('Harper <<<323570155312565>>> is the established adult woman. The starter controls the current warm-gray long-sleeved coverall and all framing. ' if key in harper_ids else '')
    prompt = (f'{seconds} seconds. One clean silent continuous illustrated shot at native1080p. '
        + identity + motions[key]
        + f' Keep one second of usable lead-in and at least one second of lead-out; the main readable motion occurs between seconds1 and{1+item["editFrames"]/24:.3f}. '
        + 'Preserve the approved starter composition, subjects, anatomy, materials and painted graphic-novel style. Natural small motion continues through the handles; no static title hold, montage, cuts, captions, lettering, watermark, audio or lip-sync. Only subjects explicitly requested appear.\n\n'
        + lock)
    take_id = item['shotId'] + (('-'+item['plate']) if item['plate'] != 'main' else '') + '-motion-v01'
    entry = dict(id=take_id,shotId=item['shotId'],plate=item['plate'],title=shot['title'],
        startFrame=item['startFrame'],editFrames=item['editFrames'],leadInFrames=24,leadOutFrames=24,
        sourceEditStartFrame=25,model='kling-video-v3_0',duration=seconds,resolution='1080p',
        imageCount=1,enable_audio=False,prefer_multi_shots=False,tailImage=None,
        firstImage=item['firstImage'],firstImageSha256=hashlib.sha256(first.read_bytes()).hexdigest(),
        prompt=prompt,estimatedCredits=item['estimatedCredits'])
    if key in harper_ids:
        entry['elements'] = [{'id':'323570155312565','bindName':'Harper'}]
    shots.append(entry)
    (OUT/(take_id+'.prompt.txt')).write_text(prompt+'\n',encoding='utf-8')
assert len(shots) == 37 and sum(s['estimatedCredits'] for s in shots) == 1528
plan = dict(status='Prepared, user authorized after reviewing V61 and the 1528-credit tally',
    authorization='User: Okay, no worries then... go and do the generations. This follows the explicit 37-video silent1080p Kling3.0 tally of1528credits, including separate cosmic and Harper finale sources.',
    sourceAnimatic='v61',fps=24,output='generated/kling-tests/first-contact-motion-v01',
    reviewOutput='generated/storyboard/first-contact-motion-v01',estimatedCredits=1528,
    submissionCreditLimit=1528,priorConfirmedCumulativeCredits=3384,
    expectedRemainingCredits=17353,separateFinaleVideoPlates=True,promptLock=lock,
    shots=shots)
(BASE/'kling-first-contact-motion-v01.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Prepared37 source videos;1528credits; exact accepted images hashed; no jobs submitted.')
