"""Prepare one redesigned original-ark frame and preserve the accepted design."""
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
plan=json.loads((PROJECT/'kling-lab-space-motion-v01.json').read_text(encoding='utf-8'))
lock=plan['shots'][0]['prompt'].split('\n\nPROMPT LOCK:')[1]
lock='PROMPT LOCK:'+lock
prompt='''Use case: illustration-story
Asset type: single 16:9 graphic-novel music-video starter frame for the lyric "So bright". No text is drawn in the image.
Input image 1: authoritative original robot headquarters laboratory ship design and painted finish. Preserve this exact elongated graphite submarine-like ship, cyan oval culture galleries with tiny tanks inside, fine amber longitudinal lights, asymmetric branching service spars and restrained circular cyan aft drive. It has no biosphere domes. This image is a design/style reference, not a composition to copy.
Primary request: A more striking cosmic-light interlude, clearly different from another medium broadside of the ship. The complete same laboratory vessel is small in the lower-left to middle-left, about 40–45 percent of frame width, bow pointing diagonally toward upper-right, three-quarter underside angle with coherent proportions. Its shadowed graphite hull and cyan culture galleries remain readable. The visual protagonist is the breathtaking warm light: a large luminous golden-white sun is partly cropped by the upper-right edge, with a visible curved limb, richly painted granular surface and delicate soft rounded corona. The sun occupies roughly the upper-right quarter, balanced against deep dark blue space around the vessel. A beautiful thin gold rim catches the ship's bow and upper contour, contrasting with cool cyan gallery illumination. Space between ship and sun is open and calm. Fine distant stars and very subtle violet/blue nebula clouds, rich painterly atmosphere, crisp selectively inked engineering detail, controlled bloom without washing away the ship or sun texture. Quiet dark bottom 12 percent for lyric overlay.
Constraints: Light travels visually through illumination and contrast, never drawn as beams. Absolutely no long luminous streaks, speed lines, diagonal rays, rings, ribbons, arcs or trails between ship and sun. No drawn star flare spokes. No warp tunnel, motion blur, exhaust trail, extra ship, planets, giant habitat pods, human figures, text, captions, logos or watermark. Preserve the reference's elegant dark ship rather than changing its structure or materials. Full-screen painted illustration, not a photo or Blender render.
'''+lock
(OUT/'lab2-08.prompt.txt').write_text(prompt,encoding='utf-8')
(OUT/'generation-input.json').write_text(json.dumps(dict(tool='built-in ImageGen',itemId='robot-ship-so-bright-v01',
    prompt=prompt,reference=str(PROJECT/'generated/storyboard/lab-verse-v01/lab2-06.png'),
    destination=str(OUT/'lab2-08.png'),status='awaiting still generation'),indent=2),encoding='utf-8')
print('One original-ship starter-frame prompt prepared')
