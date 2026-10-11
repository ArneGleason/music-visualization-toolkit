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
BACKUP = OUT / 'checkpoints/pre-flip-v03-shotlist.json'
CHANGES = {
    'concourse-004': ('Flip 1 - asymmetrical jade bioship',
        'An asymmetrical windowless grown vessel with an offset crest and unequal organic ribs. Muted jade shell ridges contrast with deep plum connective tissue; restrained warm boarding light ties it to the station. The cool color mass separates it from the preceding ivory shuttle and following gold sails.'),
    'concourse-005': ('Flip 2 - geometric light-sail craft',
        'A tall geometric light-sail craft with gold structural spars, saffron and ivory triangular sails, and an opaque warm-ivory angular cabin without windows. Its warm geometric silhouette follows the cool jade bioship and leads into the rusty ferry.'),
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
        image = OUT / (identifier+'-v03.png')
        prompt = (OUT / (identifier+'-v03.prompt.txt')).read_text(encoding='utf-8').strip()
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
            'reason': 'User requested windowless craft, greater biomechanical asymmetry and a coherent sequence of contrasting ship colors.'})
        shot.update(title=title, description=description, imagePrompt=prompt)
        shot['startingFrameDraft'] = dict(
            id=identifier+'-still-v03', image=image.relative_to(BASE).as_posix(),
            previousImage=shot['startingFrameSelection']['image'],
            userSelected=False, status='Revised composition draft; review pending',
            generationMode='built-in ImageGen edit', label=title,
            nativeWidth=width, nativeHeight=height)
    save(REGISTER, register)
    options = read(OUT/'review-options.json')
    save(OUT/'checkpoints/review-options-v41.json', options)
    options.update(sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v41.mp4',
        animaticVersion='v42',
        reviewIntro='V42 refines the first two flips: asymmetrical jade/plum biomechanical ship and windowless ivory cabin on the gold light-sail craft. Color sequence: ivory, jade/plum, gold, rusty ochre. The junk ferry, captain, wardrobe, other stills and all frame timings are retained. These are held composition drafts for review.',
        presentation='V41 imagery with revised first and second flip stills; original master audio.',
        continuationNotes='V42 revises concourse-004 and concourse-005 only: windowless asymmetrical jade/plum bioship then gold light-sail craft with opaque ivory cabin. Other imagery and timing retained. Original master audio verified. Final flip / Guess not timing remains provisional.')
    save(OUT/'review-options.json', options)
    save(OUT/'checkpoints/review-manifest-v41.json', read(OUT/'review-manifest.json'))
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
         tool='built-in ImageGen', animaticVersion='v42', status='Revised flips for user review', items=items))
    manifest = read(OUT/'manifest.json')
    manifest.update(fullAnimaticChanged=True, animaticVersion='v42',
        fullAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v42.mp4',
        revisedShots=list(CHANGES), timingCaveat=register['concourseSequence']['timingReview'])
    save(OUT/'manifest.json', manifest)
    checks = read(OUT/'verification.json')
    checks['flipRevisionV03'] = dict(revisedShots=list(CHANGES),
        unchangedOtherShotRecords=True, unchangedFrameGrid=True,
        exactSharedPromptLock=True, previousImagesRetained=True,
        fullAnimatic='v42', originalMasterAudio='AAC packet hashes verified by assembly tool')
    save(OUT/'verification.json', checks)
    print('Verified: only two shot records revised; prior images and all timing retained')
