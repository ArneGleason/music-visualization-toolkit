"""Correct the bow/sun relationship without changing the robot ship design."""
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
prior=json.loads((PROJECT/'kling-robot-ship-so-bright-v01.json').read_text(encoding='utf-8'))
lock='PROMPT LOCK:'+prior['shots'][0]['prompt'].split('\n\nPROMPT LOCK:')[1]
prompt='''Use case: precise-object-edit
Asset type: single 16:9 illustrated graphic-novel starter frame for So bright. No text.
Input images: Image 1 is the previous So bright still to revise; preserve its beautiful graphite ship, painted sun texture, cyan/amber lighting and illustration quality. Image 2 is the original robot laboratory ship identity reference; preserve its elongated hull, four tapering oval cyan culture galleries, amber seams, branching service spars and cyan aft drive.
Primary request: Change only the composition and lighting direction to show safe travel ACROSS the sunlight, clearly AWAY from the star. Put the large textured cropped solar limb in the UPPER LEFT corner, extending only through the upper-left third of the image. The ship lies in the LOWER RIGHT half, complete and uncropped, about half the frame width, centre at roughly 62% image width and 68% image height. Its long axis is nearly horizontal, its pointed BOW facing RIGHT and slightly DOWN, towards open dark space and the right edge. Its circular cyan aft drive is at the LEFT end. The star is behind and above the ship's STERN, not ahead of the bow. Show a broad obvious dark gap between the entire vessel and solar limb. Keep at least a quarter frame of open dark blue space between the solar limb and the ship's nearest silhouette. Do not put the ship's nose on a line that points at the sun. The star is a distant source of brilliant illumination, not an obstacle in the flight path.
Keep the existing image's richly painted golden solar surface and soft rounded corona, controlled bloom and detailed dark graphite engineering. Warm light catches the ship's aft/top contour from upper-left; cool cyan galleries remain readable. Fine stars, sparse soft indigo/violet cloud depth, calm negative space around the ship. Bottom 12% stays dark for lyrics. A beautiful simple readable contrast between sunlight and cool ship, matching the established painted graphic-novel finish.
Constraints: The entire solar limb stays well away from the vessel. No overlap, contact, approach, diving, bow pointing toward the sun, collision-course composition or huge near-sun impression. No starward streaks, drawn beams, rays, ribbons, trails, warp tunnel, solar flare spokes, extra spacecraft or planets. No added exhaust jet. No biosphere domes, characters, labels or watermark. Preserve the ship identity and richness; composition is the requested change.
'''+lock
(OUT/'lab2-08.prompt.txt').write_text(prompt,encoding='utf-8')
(OUT/'generation-input.json').write_text(json.dumps(dict(tool='built-in ImageGen',itemId='robot-ship-so-bright-v02',
    prompt=prompt,inputs=[str(PROJECT/'generated/storyboard/robot-ship-so-bright-v01/lab2-08.png'),str(PROJECT/'generated/storyboard/lab-verse-v01/lab2-06.png')],
    destination=str(OUT/'lab2-08.png'),status='Awaiting composition correction'),indent=2),encoding='utf-8')
print('Composition correction prepared')
