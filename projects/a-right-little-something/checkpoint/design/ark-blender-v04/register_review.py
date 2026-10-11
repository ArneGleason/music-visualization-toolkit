"""Register a native Blender look-development review without changing the edit."""
import copy
import json
from pathlib import Path
import shutil

from PIL import Image

PROJECT=Path(__file__).resolve().parents[3]
OUT=PROJECT/'generated/storyboard/ark-illustrated-v01'
MODEL=PROJECT/'generated/design/ark-blender-v04'
OUT.mkdir(parents=True,exist_ok=True)
assets=[
    ('01-reference.png',PROJECT/'generated/storyboard/ark-replacement-v01/lab2-06.png','Approved illustration — target'),
    ('02-before.png',PROJECT/'generated/storyboard/ark-blender-v02/01-forward-quarter.png','Previous Blender look — V02'),
    ('03-illustrated-hero.png',MODEL/'illustrated-hero.png','Updated illustrated render — V04'),
    ('04-illustrated-aft.png',MODEL/'illustrated-aft.png','Updated aft view — same model'),
    ('05-illustrated-detail.png',MODEL/'illustrated-detail.png','Recessed galleries and habitat detail'),
    ('06-textured-hero.png',MODEL/'textured-hero.png','Updated render before subtle brush finish'),
]
manifest=[]
for i,(name,source,title) in enumerate(assets,1):
    shutil.copy2(source,OUT/name)
    with Image.open(OUT/name) as img:
        img.verify()
    manifest.append(dict(index=i,id=f'ark-illustrated-review-{i}',src=name,output=name,href=name,
        title=title,label=title,prompt='Native Blender look development. Fixed six-pod model; warm ivory alloy, dark graphite recesses, cyan galleries, amber rim lighting, muted terrain-scale habitats. User review pending.'))
(OUT/'review-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(OUT/'review-options.json').write_text(json.dumps(dict(preset='detail-review',showCaptions=True,minTileWidth=480,
    title='Headquarters ark — illustrated Blender lighting and materials',contactSheetColumns=3,
    contactSheetThumb=480,contactSheetOutput='look-overview.png'),indent=2),encoding='utf-8')

project_file=PROJECT/'project.json'
project=json.loads(project_file.read_text(encoding='utf-8'))
old=copy.deepcopy(project['production']['headquartersArkModel'])
current=copy.deepcopy(old)
current.update(model='generated/design/ark-blender-v04/headquarters-ark-v04.blend',
    styleSource='generated/design/ark-blender-v03/style_ark.py',
    geometryPolishSource='generated/design/ark-blender-v04/polish_ark.py',
    renderFinishSource='generated/design/ark-blender-v04/finish_look.py',
    status='Native illustrated lighting/material/gallery refinement; user review pending',
    review='http://127.0.0.1:8768/storyboard/ark-illustrated-v01/review-board.html',
    previousModel=old['model'],previousReview=old['review'],
    cameraSweepNote='Existing V02 sweep demonstrates fixed geometry; it does not show the updated V04 style.',
    renderSettings=dict(engine='Cycles',device='OptiX',samples=96,viewTransform='AgX',look='Medium High Contrast',
        exposure=.25,proofSize=[1600,900],brushRadiusPixels=3,brushBlend=.35),
    animationStyleReviewPending=True)
project['production']['headquartersArkModel']=current
project_file.write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

shots_file=PROJECT/'shots/shotlist.json'
shots=json.loads(shots_file.read_text(encoding='utf-8'))
changed=[]
def update_records(value):
    if isinstance(value,dict):
        if 'blenderModelDevelopment' in value:
            changed.append(value.get('id'))
            value['blenderModelDevelopment']=copy.deepcopy(current)
        for key,child in value.items():
            if key!='blenderModelDevelopment':
                update_records(child)
    elif isinstance(value,list):
        for child in value:
            update_records(child)
update_records(shots)
assert changed==['lab2-06','lab2-07','lab2-08','lab2-09'],changed
shots_file.write_text(json.dumps(shots,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(review=str(OUT),updatedShotMetadata=changed,currentFilm=project['production']['animatic'],newPaidGenerations=0)))
