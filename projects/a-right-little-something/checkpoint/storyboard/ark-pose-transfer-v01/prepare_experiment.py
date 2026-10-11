"""Two bounded Blender-pose / painted-reference image experiments."""
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
LOCK='''SHIP LOCK — IDENTICAL FOR BOTH POSES:
Exactly six equal-sized biosphere domes in three mirrored lateral pairs, all bases in one plane. The middle pair sits farther outboard. One long ivory-and-graphite central laboratory spine, curved lateral support arms, cyan oval culture galleries, amber rim lights and cyan navigation accents. One vertical circular aft field-drive ring with cyan inner light and a blue-violet field. No rockets. Physical pod centres, canopy radii, spine length, symmetry and drive-ring placement are those in Image 1. Keep the guide's ship orientation, perspective, projected proportions, silhouette, framing and overlap order. Do not rearrange, merge, duplicate or omit pods. Retain each habitat's location and restrained green/teal/plum/ochre identity; enrich them with tiny terrain-scale alien flora, shorelines, valleys and distant ridges rather than giant plants. No rainbow habitats. No text or characters.'''
BASE='''Use case: style-transfer
Asset type: single 16:9 painted graphic-novel music-video starter frame, not a sheet or comparison.
Input images: Image 1 is the EDIT TARGET and authoritative native Blender camera/geometry guide. Image 2 is the approved ship illustration: authoritative materials, finish, lighting, detail level and visual style. Repaint Image 1 into the rich illustrated quality of Image 2. Do not merely smooth or recolor the Blender render. Do not copy Image 2's camera pose.
Primary request: Preserve the actual pose and layout of Image 1 while rendering the same ship as if the artist of Image 2 illustrated it. Refine the simple hull surfaces into layered ivory alloy armour, inset graphite engineering, precise panel seams and beautifully illuminated deep cyan galleries. The gallery detailing may become richer within the existing openings; structural layout stays fixed. Domes contain sweeping miniature alien landscapes, convincing clear curved canopies with delicate structural networks and restrained warm reflections. Use the reference's richly detailed painted surfaces, deliberate graphic shadows, warm edge light, crisp selective highlights and controlled cyan/amber bloom. The field drive has the reference's intricate illuminated housing and illustrated blue-violet energy.
Scene/backdrop: Deep dark space with richly painted blue-violet star-cloud texture and fine stars like Image 2, preserving the amount and placement of negative space in Image 1. Keep the bottom lyric area dark. No captions, labels, watermarks or collage.
Constraints: This is a pose-preserving paintover of Image 1, not a redesign. Intricate surface and landscape detail must follow the supplied geometry and perspective. Keep the ship rigid, symmetrical and believable. Do not inherit the sparse plastic Blender finish. Do not rotate the ship back to the reference pose.
'''
poses=[('forward','ark-pose-transfer-v01-forward','Forward pose — painted-reference finish','illustrated-hero.png'),
       ('aft','ark-pose-transfer-v01-aft','Aft pose — painted-reference finish','illustrated-aft.png')]
records=[]
for pose,item,title,guide in poses:
    prompt=BASE+f'Camera pose: Preserve the {pose} view shown in Image 1 exactly.\n'+LOCK
    (OUT/f'{pose}.prompt.txt').write_text(prompt,encoding='utf-8')
    records.append(dict(pose=pose,itemId=item,title=title,prompt=prompt,
        guide=str(PROJECT/'generated/design/ark-blender-v04'/guide),
        reference=str(PROJECT/'generated/storyboard/ark-replacement-v01/lab2-06.png'),
        destination=str(OUT/f'{pose}.png'),status='experiment pending; no animatic replacement'))
(OUT/'experiment.json').write_text(json.dumps(dict(tool='built-in ImageGen',boardId='ea37232e-e258-4176-b1b9-1d38747fc88e',
    promptLock=LOCK,items=records),indent=2),encoding='utf-8')
print(json.dumps([dict(id=r['itemId'],title=r['title']) for r in records]))
