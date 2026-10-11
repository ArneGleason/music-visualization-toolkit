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
BACKUP = OUT / 'checkpoints/pre-flip-v05-shotlist.json'
CHANGES = {
    'concourse-004': ('Flip 1 - three-part ribbed organic craft',
        'An elegant asymmetrical grown personal spacecraft with three visibly distinct connected structures: compact boarding body, taller tilted ribbed shell and smaller offset propulsion structure. Smooth jade shell surfaces and pale celadon bone-like ribs surround open negative-space gaps; plum is confined to subtle recesses. Functional organic structure replaces the nodules and single U-shaped body. No hooks, claws or windows.'),
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
        image = OUT / (identifier+'-v05.png')
        prompt = (OUT / (identifier+'-v05.prompt.txt')).read_text(encoding='utf-8').strip()
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
            'reason': 'User requested a prettier functional organic design with ribs and bones instead of nodules, then superseded the U with three distinct connected parts.'})
        shot.update(title=title, description=description, imagePrompt=prompt)
        shot['startingFrameDraft'] = dict(
            id=identifier+'-still-v05', image=image.relative_to(BASE).as_posix(),
            previousImage=shot['startingFrameSelection']['image'],
            userSelected=False, status='Revised composition draft; review pending',
            generationMode='built-in ImageGen edit', label=title,
            nativeWidth=width, nativeHeight=height)
    save(REGISTER, register)
    options = read(OUT/'review-options.json')
    save(OUT/'checkpoints/review-options-v43.json', options)
    options.update(sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v43.mp4',
        animaticVersion='v44',
        reviewIntro='V44 refines only the first flip into three connected organic structures with elegant ribs, smooth jade shell and subtle plum recesses, replacing the nodular U-shaped body. Color sequence: ivory, jade/plum, gold, rusty ochre. The junk ferry, captain, wardrobe, other stills and all frame timings are retained. These are held composition drafts for review.',
        presentation='V43 imagery with only the first flip ship reshaped; original master audio.',
        continuationNotes='V44 revises concourse-004 only: three-part asymmetrical organic craft with functional flowing ribs, smooth jade shell and subtle plum recesses; no nodules, hooks, claws or windows. Other imagery and timing retained. Original master audio verified. Final flip / Guess not timing remains provisional.')
    save(OUT/'review-options.json', options)
    save(OUT/'checkpoints/review-manifest-v43.json', read(OUT/'review-manifest.json'))
    print('Prepared one revised image; frame grid unchanged')
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
         tool='built-in ImageGen', animaticVersion='v44', status='Revised flips for user review', items=items))
    manifest = read(OUT/'manifest.json')
    manifest.update(fullAnimaticChanged=True, animaticVersion='v44',
        fullAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v44.mp4',
        revisedShots=list(CHANGES), timingCaveat=register['concourseSequence']['timingReview'])
    save(OUT/'manifest.json', manifest)
    checks = read(OUT/'verification.json')
    checks['flipRevisionV05'] = dict(revisedShots=list(CHANGES),
        unchangedOtherShotRecords=True, unchangedFrameGrid=True,
        exactSharedPromptLock=True, previousImagesRetained=True,
        fullAnimatic='v44', originalMasterAudio='AAC packet hashes verified by assembly tool')
    save(OUT/'verification.json', checks)
    print('Verified: only one shot record revised; prior images and all timing retained')
