"""Assemble pose-transfer proofs with their actual source images."""
import json
from pathlib import Path
import shutil
from PIL import Image

OUT=Path(__file__).resolve().parent
experiment=json.loads((OUT/'experiment.json').read_text(encoding='utf-8'))
assets=[('01-reference.png',Path(experiment['items'][0]['reference']),'Approved illustration — finish target')]
for record,index in zip(experiment['items'],[2,4]):
    pose=record['pose']
    assets.extend([(f'{index:02d}-{pose}-guide.png',Path(record['guide']),f'{pose.title()} pose — Blender guide'),
                   (f'{index+1:02d}-{pose}-painted.png',Path(record['destination']),f'{pose.title()} pose — ImageGen experiment')])
manifest=[]
for i,(name,source,title) in enumerate(assets,1):
    assert source.is_file() and source.stat().st_size>0,source
    with Image.open(source) as image:
        image.verify()
    shutil.copy2(source,OUT/name)
    manifest.append(dict(index=i,id=f'ark-pose-transfer-review-{i}',title=title,label=title,
        src=name,href=name,output=name,prompt='Experiment: native Blender pose guide plus approved painted ship reference. Quality and structure require review; no shot replacement yet.'))
(OUT/'review-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(OUT/'review-options.json').write_text(json.dumps(dict(preset='detail-review',showCaptions=True,minTileWidth=480,
    title='Headquarters ark — Blender pose / ImageGen finish experiment',contactSheetColumns=3,
    contactSheetThumb=480,contactSheetOutput='pose-transfer-overview.png'),indent=2),encoding='utf-8')
print('Validated and copied five comparison assets')
