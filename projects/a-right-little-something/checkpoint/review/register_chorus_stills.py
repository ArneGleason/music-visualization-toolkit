import hashlib
import json
from pathlib import Path

base = Path(__file__).resolve().parents[2]
spec = json.loads((base/'storyboard-chorus1-ideas-v01.json').read_text(encoding='utf-8'))
path = base/'shots/shotlist.json'
register = json.loads(path.read_text(encoding='utf-8'))
shots = {s['id']: s for s in register['storyboardProposals']}
manifest = []
for index, item in enumerate(spec['shots'], 1):
    image = base/spec['output']/(item['id']+'-starting-frame-v01.png')
    assert image.is_file() and image.stat().st_size > 0, image
    shot = shots[item['id']]
    shot['startingFrameDraft'] = dict(image=image.relative_to(base).as_posix(),
        label=f"{shot['startSeconds']:.2f}s · {item['selection']} · {item['title']}",
        status='Generated composition draft; awaiting image review', userSelected=False,
        generator='Built-in ImageGen', prompt=item['imagePrompt'],
        sha256=hashlib.sha256(image.read_bytes()).hexdigest())
    shot['status'] = 'Selected imagery branch; generated still draft awaiting review'
    shot['generationApproach'] = item['generationApproach']
    shot['lyrics'] = item['lyrics']
    manifest.append(dict(index=index, title=shot['startingFrameDraft']['label'],
        imagePath=str(image.resolve()), href=image.name, prompt=item['imagePrompt'],
        caption=item['description'], route='built-in-imagegen'))
path.write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(base/spec['output']/'review-items.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
project_path = base/'project.json'
project = json.loads(project_path.read_text(encoding='utf-8'))
project['production']['chorus1StillReview'] = 'http://127.0.0.1:8768/storyboard/chorus1-ideas-v01/'
project_path.write_text(json.dumps(project,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Registered five generated draft stills; branch selection and image approval kept distinct.')
