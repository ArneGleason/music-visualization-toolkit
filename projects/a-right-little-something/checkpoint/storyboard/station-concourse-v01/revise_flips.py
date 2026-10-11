"""Revise two ship options, preserving prior stills and the saved timing grid."""
import copy
import hashlib
import json
from pathlib import Path
import sys
from PIL import Image

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
REGISTER = BASE / 'shots/shotlist.json'
BACKUP = OUT / 'checkpoints/pre-flip-v02-shotlist.json'
CHANGES = {
    'concourse-004': ('Flip 1 - biomechanical vessel',
        'A grown biomechanical passenger vessel with a sweeping bone-and-chitin silhouette, organic ribs and a green-lit living boarding entrance. The first flip introduces a radically different technology from the arrival pod.'),
    'concourse-005': ('Flip 2 - geometric light-sail craft',
        'A tall geometric light-sail craft: open gold structural spars, translucent triangular sails and a suspended angular cabin reached by a slender boarding bridge. Its airy silhouette contrasts immediately with the grown ship and the battered ferry.'),
}

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

register = read(REGISTER)
if sys.argv[1] == 'prepare':
    assert not BACKUP.exists(), 'Revision already prepared'
    BACKUP.parent.mkdir(exist_ok=True)
    save(BACKUP, register)
    for shot in register['storyboardProposals']:
        if shot['id'] not in CHANGES:
            continue
        identifier = shot['id']
        title, description = CHANGES[identifier]
        image = OUT / (identifier+'-v02.png')
        prompt = (OUT / (identifier+'-v02.prompt.txt')).read_text(encoding='utf-8').strip()
        assert shot['promptLock'] in prompt
        with Image.open(image) as img:
            img.verify()
        with Image.open(image) as img:
            width, height = img.size
        assert abs(width/height - 16/9) < .08
        shot.setdefault('stillRevisionHistory', []).append({
            'title': shot['title'], 'description': shot['description'],
            'imagePrompt': shot['imagePrompt'],
            'startingFrameDraft': copy.deepcopy(shot['startingFrameDraft']),
            'reason': 'User requested different ship silhouettes and technology families.'})
        shot.update(title=title, description=description, imagePrompt=prompt)
        shot['startingFrameDraft'] = dict(
            id=identifier+'-still-v02', image=image.relative_to(BASE).as_posix(),
            previousImage=shot['startingFrameSelection']['image'],
            userSelected=False, status='Revised composition draft; review pending',
            generationMode='built-in ImageGen edit', label=title,
            nativeWidth=width, nativeHeight=height)
    save(REGISTER, register)
    options = read(OUT/'review-options.json')
    save(OUT/'checkpoints/review-options-v40.json', options)
    options.update(sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v40.mp4',
        animaticVersion='v41',
        reviewIntro='V41 revises only the first two flip ship designs: a grown biomechanical vessel and a geometric light-sail craft. The junk ferry, captain, wardrobe, other stills and all frame timings are retained. These are held composition drafts for review.',
        presentation='V40 imagery with revised first and second flip stills; original master audio.',
        continuationNotes='V41 revises concourse-004 and concourse-005 only: biomechanical vessel then geometric light-sail craft. Other imagery and timing retained. Original master audio verified. Final flip / Guess not timing remains provisional.')
    save(OUT/'review-options.json', options)
    save(OUT/'checkpoints/review-manifest-v40.json', read(OUT/'review-manifest.json'))
    print('Prepared two revised images; frame grid unchanged')
elif sys.argv[1] == 'finish':
    prior = read(BACKUP)
    original = {s['id']: s for s in prior['storyboardProposals']}
    # The assembly helper refreshes metadata for its entire batch. Preserve
    # untouched shot records exactly, including their original placement history.
    register['storyboardProposals'] = [s if s['id'] in CHANGES else original[s['id']]
                                      for s in register['storyboardProposals']]
    shots = [s for s in register['storyboardProposals'] if s.get('batch') == 'station-concourse-v01']
    assert len(shots) == 11 and len({s['promptLock'] for s in shots}) == 1
    for shot in shots:
        old = original[shot['id']]
        for key in ('startFrame','endFrameExclusive','frames'):
            assert shot[key] == old[key]
    save(REGISTER, register)
    items = [dict(id=s['id'], image=s['startingFrameDraft']['image'],
                  sha256=digest(BASE/s['startingFrameDraft']['image']),
                  prompt=s['imagePrompt'], startFrame=s['startFrame'],
                  endFrameExclusive=s['endFrameExclusive']) for s in shots]
    save(OUT/'review-manifest.json', dict(boardId='ce27973e-c009-4d44-8eab-ed01be58c996',
         tool='built-in ImageGen', animaticVersion='v41', status='Revised flips for user review', items=items))
    manifest = read(OUT/'manifest.json')
    manifest.update(fullAnimaticChanged=True, animaticVersion='v41',
        fullAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v41.mp4',
        revisedShots=list(CHANGES), timingCaveat=register['concourseSequence']['timingReview'])
    save(OUT/'manifest.json', manifest)
    checks = read(OUT/'verification.json')
    checks['flipRevisionV02'] = dict(revisedShots=list(CHANGES),
        unchangedOtherShotRecords=True, unchangedFrameGrid=True,
        exactSharedPromptLock=True, previousImagesRetained=True,
        fullAnimatic='v41', originalMasterAudio='AAC packet hashes verified by assembly tool')
    save(OUT/'verification.json', checks)
    print('Verified: only two shot records revised; prior images and all timing retained')
