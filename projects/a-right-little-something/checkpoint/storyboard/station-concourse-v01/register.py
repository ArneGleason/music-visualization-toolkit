"""Register the generated concourse composition drafts without altering timing."""
import json
from pathlib import Path
import shutil
from PIL import Image

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
spec = json.loads((OUT/'generation-input.json').read_text(encoding='utf-8'))
path = BASE/'shots/shotlist.json'
register = json.loads(path.read_text(encoding='utf-8'))
shots = [s for s in register['storyboardProposals'] if s.get('batch') == 'station-concourse-v01']
assert len(shots) == len(spec['items']) == 11
items = {item['id']:item for item in spec['items']}
for shot in shots:
    item = items[shot['id']]
    receipt_path = OUT/(shot['id']+'.actual-generation.json')
    if not receipt_path.exists():
        receipt_path = OUT/(shot['id']+'-actual-generation.json')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    actual_prompt = receipt.get('actual_prompt', receipt.get('prompt'))
    assert actual_prompt and spec['promptLock'] in actual_prompt
    (OUT/(shot['id']+'.prompt.txt')).write_text(actual_prompt+'\n', encoding='utf-8')
    image = Path(item['destination'])
    assert image.exists() and image.stat().st_size > 0, image
    with Image.open(image) as img:
        img.verify()
    with Image.open(image) as img:
        width, height = img.size
    assert abs(width/height-16/9) < 0.08, (image, width, height)
    shot.update(
        promptLock=spec['promptLock'], imagePrompt=actual_prompt,
        generationApproach='Built-in ImageGen linked composition draft; later native motion needs still and timing review.',
        startingFrameDraft={
            'id':shot['id']+'-still-v01', 'image':image.relative_to(BASE).as_posix(),
            'userSelected':False, 'status':'Generated composition draft; user review pending',
            'generationMode':'built-in ImageGen', 'label':shot['title'],
            'nativeWidth':width, 'nativeHeight':height,
        },
        status='Generated still draft ready for timed animatic review',
    )
assert len({s['promptLock'] for s in shots}) == 1
sequence = register['concourseSequence']
sequence.setdefault('directionHistory', []).append({
    'date':'2026-10-11', 'stage':'before still generation',
    'continuityNotes':sequence['continuityNotes'],
})
sequence['continuityNotes'] = [n for n in sequence['continuityNotes'] if not n.startswith('Wardrobe continuity')]
sequence['continuityNotes'].append('User allows a change aboard the pod before station arrival. Current draft choice: practical warm-gray long-sleeve pod-issue survival coverall, plain adjustable belt, graphite utility shoes and tiny unlettered amber upper-arm tab. Change happens offscreen in transit; retain this outfit through station and ship discovery. This outfit is a review draft, distinct from the opening short-sleeve gray outfit; any later change into the opening outfit remains to be staged.')
sequence.update(stillReview='http://127.0.0.1:8768/storyboard/station-concourse-v01/',
                boardId=spec['boardId'],
                status='User-selected concourse route; survival-suit still drafts for review')
backup = OUT/'pre-stills-shotlist.json'
if not backup.exists():
    shutil.copy2(path,backup)
path.write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
batch = {
    'id':'station-concourse-v01', 'title':'Station concourse - find a way onward',
    'output':'generated/storyboard/station-concourse-v01',
    'sourceAnimatic':'generated/animatic/A-Right-Little-Something-selected-motion-v39.mp4',
    'draftForReview':True, 'assembledStills':True, 'animaticVersion':'v40',
    'reviewIntro':'Eleven linked composition drafts on the saved frame grid. Harper wears a practical survival coverall found aboard the pod. The directory briefly orients her; real ship options lead to a suspect ferry captain, a quiet outer walkway, and discovery of the opening spherical ship. The final flip / Guess not edge remains provisional. These are held stills for timing and design review.',
    'presentation':'V39 accepted native footage followed by station concourse still drafts through frame 2595; original master audio.',
    'mediaLabel':'native motion / station concourse still drafts',
    'continuationNotes':'V40 inserts 11 linked station-concourse still drafts at frames 2105-2595. Harper changes offscreen in pod transit into a warm-gray survival coverall. The final flip / Guess timing remains provisional; review the station and outfit before native generation. The full 5265-frame edit and original master audio are retained.',
}
(OUT/'review-options.json').write_text(json.dumps(batch,indent=2)+'\n',encoding='utf-8')
print('Registered eleven linked still drafts and shared prompt lock')
