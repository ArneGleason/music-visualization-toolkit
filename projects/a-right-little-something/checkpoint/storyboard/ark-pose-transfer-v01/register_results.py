"""Persist experiment provenance without selecting stills into the edit."""
import json
from pathlib import Path
from PIL import Image

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
path=OUT/'experiment.json'
experiment=json.loads(path.read_text(encoding='utf-8'))
qa={
    'forward':dict(original='C:/Users/arneg/.codex/generated_images/01a126c8-295b-7551-a19f-b3aa043501af/exec-6e3f0eb5-bf15-41de-ae91-6b48006b2cb5.png',
        notes='Six pods, guide camera pose, broad projected proportions and overlap order retained. Rich illustrated hull/galleries/landscapes and field ring. Nose slightly rounder than guide; fine panel detail is reinterpreted.'),
    'aft':dict(original='C:/Users/arneg/.codex/generated_images/01a126c8-4b1b-7da2-a9b3-72b02218e04b/exec-526fe6b8-6296-4056-b85b-55d36e321211.png',
        notes='Six pods, guide aft orientation, outboard middle placement and overlap order retained. Much richer illustrated finish. Broad structure is coherent; fine panels, canopy reflections and terrain are generated rather than exact 3D projections.')}
for record in experiment['items']:
    output=Path(record['destination'])
    with Image.open(output) as image:
        size=image.size
        image.verify()
    record.update(status='Agent-reviewed experiment; user review pending; not selected into animatic',
        width=size[0],height=size[1],bytes=output.stat().st_size,attempts=1,
        originalGeneratedFile=qa[record['pose']]['original'],reviewNotes=qa[record['pose']]['notes'])
experiment.update(review='http://127.0.0.1:8768/storyboard/ark-pose-transfer-v01/review-board.html',
    boardRevision=67,animaticReplacement=False,klingSubmissions=0,
    conclusion='Reference finish transfers strongly while broad Blender pose/layout survives. Local silhouette and fine detailing remain nondeterministic; user review pending.')
path.write_text(json.dumps(experiment,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
project_path=PROJECT/'project.json'
project=json.loads(project_path.read_text(encoding='utf-8'))
model=project['production']['headquartersArkModel']
model['poseTransferExperiment']=dict(manifest='generated/storyboard/ark-pose-transfer-v01/experiment.json',
    review=experiment['review'],status='Two built-in ImageGen pose/finish experiments; user review pending',
    poses=['forward','aft'],animaticReplacement=False,klingSubmissions=0)
project_path.write_text(json.dumps(project,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(outputs=[r['destination'] for r in experiment['items']],review=experiment['review'],currentFilm=project['production']['animatic'])))
