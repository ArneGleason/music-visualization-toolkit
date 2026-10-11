from pathlib import Path
import sys
from PIL import Image

sys.path.insert(0,str(Path('tools').resolve()))
from build_chorus_revision import load,save

base=Path('projects/a-right-little-something').resolve()
out=base/'generated/design/ark-biopods-v04'
image=out/'ark-biopods-design-v04.png'
assert image.stat().st_size>0
size=Image.open(image).size
save(out/'generation-prompt.json',dict(id='lab-ark-biopods-concept-v04',tool='built-in image_gen',attempts=1,
    sourceImage='generated/design/ark-biopods-v03/ark-biopods-design-v03.png',imagePath=str(image),
    prompt=(out/'generation-prompt.txt').read_text(encoding='utf-8'),nativeWidth=size[0],nativeHeight=size[1],
    status='Agent inspected design candidate; user review pending',
    qa=dict(domeCount=6,geometry='Six lateral pod positions, hull, supports, drive ring and framing visually retained.',
        palette='Muted olive/sage, slate teal, mineral and earth tones with subtle plum and ochre accents; biological glow reduced.',
        scale='Small organism clusters amid broad valleys, channels, water basins and terrain layers; clear air and receding distant terrain make pods feel larger.')))
project=load(base/'project.json')
refs=project.setdefault('visualReferences',[])
for ref in refs:
    if ref.get('id')=='headquarters-alien-biopod-ark-v03':
        ref['status']='Superseded color/organism-scale draft; user requested muted variation and smaller organisms'
refs.append(dict(id='headquarters-alien-biopod-ark-v04',path=image.relative_to(base).as_posix(),
    role='Latest headquarters ship reference: six lateral terrain-scale habitats with restrained color variation and a vertical field-drive ring',
    status='User accepted v02 architecture; v04 habitat palette/scale for review',directionFile='ARK-BIOPOD-DESIGN.md'))
save(base/'project.json',project)
print('Saved reference and exact prompt; six pods verified visually;',size,'pixels.')
