"""Catalog the editable 3D design without altering the timed animatic."""
import json
from pathlib import Path
import shutil

base = Path(__file__).resolve().parents[2]
source = base/'generated/design/ark-blender-v02'
review = base/'generated/storyboard/ark-blender-v02'
review.mkdir(parents=True, exist_ok=True)


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')


assets = [
    ('Approved illustration anchor', base/'generated/storyboard/ark-replacement-v01/lab2-06.png', 'reference.png'),
    ('First geometry blockout', base/'generated/design/ark-blender-v01/clay-01-forward-quarter.png', 'clay.png'),
    *[(title, source/f'lookdev-{name}.png', name+'.png') for name, title in [
        ('01-forward-quarter', 'Refined forward quarter'), ('02-aft-quarter', 'Same model — aft quarter'),
        ('03-top-plan', 'Same model — top plan'), ('04-side-profile', 'Same model — low side view')]],
]
manifest = []
for i, (title, image, filename) in enumerate(assets):
    assert image.stat().st_size > 0
    shutil.copy2(image, review/filename)
    manifest.append(dict(index=i+1, id='ark-3d-review-'+str(i+1), src=filename, output=filename,
                         href=filename, title=title, label=title,
                         prompt='Native Blender geometry and material study from the approved illustration. Six mirrored pod positions remain fixed across views.'))
save(review/'review-manifest.json', manifest)
save(review/'review-options.json', dict(preset='detail-review', showCaptions=True, minTileWidth=480,
     title='Headquarters ark — editable Blender model', contactSheetColumns=3,
     contactSheetThumb=480, contactSheetOutput='model-overview.png'))
save(review/'verification.json', load(source/'geometry-verification.json'))
project = load(base/'project.json')
project['production']['headquartersArkModel'] = dict(
    model='generated/design/ark-blender-v02/headquarters-ark-v02.blend',
    builder='generated/design/ark-blender-v02/build_ark.py',
    firstBlockout='generated/design/ark-blender-v01/headquarters-ark-v01.blend',
    status='Actual 3D geometry and initial material refinement; user review pending',
    review='http://127.0.0.1:8768/storyboard/ark-blender-v02/review-board.html',
    cameraSweep='http://127.0.0.1:8768/storyboard/ark-blender-v02/camera-sweep.mp4',
    animaticReplacement=False, newPaidGenerations=0)
save(base/'project.json', project)
register = load(base/'shots/shotlist.json')
for shot in register['storyboardProposals']:
    if shot.get('batch') != 'ark-replacement-v01' or shot['id'] not in ['lab2-06', 'lab2-07', 'lab2-08', 'lab2-09']:
        continue
    accepted = shot['id'] == 'lab2-06'
    for key in ['startingFrameSelection', 'startingFrameDraft']:
        shot[key]['userSelected'] = accepted
        shot[key]['status'] = ('User accepted geometry as the Blender reconstruction anchor' if accepted else
                               'User rejected distorted ship geometry; replaced direction with actual Blender reconstruction')
    shot['blenderModelDevelopment'] = project['production']['headquartersArkModel']
save(base/'shots/shotlist.json', register)
plan = load(base/'kling-ark-replacement-v01.json')
plan['status'] = 'Superseded by user request for actual 3D Blender ship; no replacement Kling jobs submitted'
plan['authorization'] = 'The three distorted angle stills are rejected; no video upload or credit charge authorized for this plan.'
save(base/'kling-ark-replacement-v01.json', plan)
print('Native model catalogued; V33 film unchanged; rejected angle images marked; no new paid generations.')
