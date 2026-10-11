import json
from pathlib import Path

base = Path(__file__).resolve().parents[2]
path = base/'storyboard-chorus1-ideas-v01.json'
spec = json.loads(path.read_text(encoding='utf-8'))
register = json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))
lock = next(s['promptLock'] for s in register['shots'] if s.get('promptLock'))
data = json.loads((base/'generated/animatic/animatic-data.json').read_text(encoding='utf-8'))
edges = [1046,1170,1228,1292,1412,1550]
choices = ['B','A','B','A','A']
scenes = [
    'Harper floating naturally at the right of an intimate interior crop, only a narrow dark metal amber-lit rail is visible. In front of her float THREE large volumetric living-world globes, their curved surfaces showing tiny nascent ecosystems rather than diagrams: one turquoise tidal basin with violet ribbed fan-fronds and small pearlescent six-legged shelled creatures, one warm ochre branching fungal terrain, one deep indigo luminous reef. A thoughtful gentle reaching gesture chooses the turquoise world. The worlds are luminous holographic projections suspended within reach, their miniature ecological details readable at different scales; do not depict three actual planets pressed against the cabin. No extra hands, no floating screens, no written labels. A starfield behind her; the ship is framing only, not the subject. The mood is attentive care and a responsibility she cannot fully foresee.',
    'Direct alien-coast experience, no ship or display. Harper kneels barefoot at a shallow water channel on peach tidal flats, gray tee and trousers, with a careful modest gesture opening a narrow gap in a low bank of dark blue stones. A thin stream of turquoise water leads from her fingertips toward a small colony of translucent violet ribbed fan-fronds; the first frond is beginning to open. Several tiny pearlescent six-legged shelled tidal animals gather near the water. Medium-wide low three-quarter view, adult face visible, natural two hands and feet, action immediately legible. Immense distant dark blue rock spires and peach clouds retain the established coast. Positive intention without omnipotent magic; one tiny change, broad surroundings.',
    'Continue the exact alien-coast ecosystem from the water-channel frame. Medium view with Harper kneeling to the left, watching intently with wonder and a slight thoughtful uncertainty. In the right foreground pearlescent six-legged shelled tidal animals have piled small blue stones and opened diverging channels so the thin turquoise stream now flows in their own beautiful branching arrangement among violet ribbed fan-fronds. The composition shows local organisms repurposing her intervention, not obeying a pre-drawn diagram. No new seed capsule is introduced: the water channel from the previous shot is the catalyst, preserving the selected A-to-B continuity. Warm upper-right light. A beautiful hopeful result with unanswered consequences, no disaster, no instantly evolved cities.',
    'A pure cosmic wide shot, no Harper portrait, no cabin, no interface. A beautiful turquoise-and-peach living planet with branching luminous coastal patterns occupies the lower-left, viewed from orbital height; a few delicate curved cyan and amber light arcs lift off its coast into broad orbital trajectories around the limb. Most of the frame opens into deep indigo/violet cosmic space, scattered luminous distant stars, restrained nebula wisps. The branching pattern from the shore becomes the shape of the orbit, a poetic match rather than a scientific diagram. A tiny light on the outward arc suggests onward travel; no need to include a recognizable spacecraft. Clear depth, vast scale, paths sparse and restrained, avoid repeated bullseye rings or dense HUD.',
    'Continue the pure cosmic painterly composition from the orbital-expansion frame, now farther out. Three distinct distant star systems distributed at different depths through an indigo-violet nebula field, connected by very sparse broad curved amber/cyan pulses. Each system has a small living world with a distinct visible ecological motif: turquoise coastal branching fans, warm ochre organic ridges, indigo luminous reefs. An echoing ripple reaches each world differently: the turquoise pattern opens, the ochre pattern bends the path, the indigo pattern absorbs it into a diffuse glow. This is exploration and uncertain intervention as abstract cosmic poetry, NOT an infographic, not a dashboard, not identical little balls aligned on a grid. Wide cinematic negative space, luminous stars and subtle atmosphere, no cabin, no character, no text, no giant obvious spacecraft.'
]
for i,s in enumerate(spec['shots']):
    s['selection'] = choices[i]
    s['description'] = s['alternatives'][choices[i]]
    s['selectedBranchDirection'] = 'User selected '+choices[i]+' on October 10; stills first, no Blender blockout.'
    s['replaceCreative'] = True
    s['promptLock'] = lock
    s['lyrics'] = [p['text'] for p in data['phrases'] if edges[i] <= p['startFrame'] < edges[i+1]]
    s['imagePrompt'] = 'Use case: illustration-story\nAsset type: one 16:9 cinematic storyboard still, no collage.\nReference roles: preserve Harper face, gray outfit and illustrated style from supplied portrait/coast references; use supplied earlier sequence frames for ecosystem or cosmic motif continuity, not their camera layout.\nScene: '+scenes[i]+'\nHigh-detail painterly graphic-novel illustration matching the references, warm expressive light, sophisticated depth. No baked lyrics, text, logo, watermark, border or panel divisions. Leave the bottom 8 percent visually quiet for later lyric overlay.\n\n'+lock+'\nThe lock describes shared identities; include only subjects explicitly requested in this scene. No ship, field grid or moons in ship-free coast/cosmic compositions.'
spec['output'] = 'generated/storyboard/chorus1-ideas-v01'
spec['title'] = 'Chorus 1 · mission, intervention and orbit echoes'
spec['selectionSequence'] = choices
spec['generationMode'] = 'Built-in ImageGen; still composition drafts; no Blender or Kling'
spec['reviewIntro'] = 'Five still composition drafts following the selected B → A → B → A → A imagery arc. Static holds use the existing lyric frame grid. Zoom blurs and dissolves are planned alternatives, not simulated motion in this preview. One-second source handles are reserved for eventual footage.'
path.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(base/spec['output']).mkdir(parents=True,exist_ok=True)
print('Prepared five selected prompts with identical lock.')
