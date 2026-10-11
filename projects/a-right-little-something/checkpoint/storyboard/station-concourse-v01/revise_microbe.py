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
BACKUP = OUT / 'checkpoints/pre-flip-v04-shotlist.json'
CHANGES = {
    'concourse-004': ('Flip 1 - compact microbial U ship',
        'A compact asymmetrical U-shaped grown personal spacecraft, inspired by enlarged microscopic organisms. Unequal blunt lobes and rounded compound jade shell volumes surround a deep open concavity, with plum membrane folds and an opaque amber-edged boarding hatch. No hooks, claws, spikes, long prow or windows; the approved jade/plum palette remains.'),
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
        image = OUT / (identifier+'-v04.png')
        prompt = (OUT / (identifier+'-v04.prompt.txt')).read_text(encoding='utf-8').strip()
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
            'reason': 'User approved the colors and requested a compact asymmetrical U-shaped microbial body with rounded organic compound forms and no hooks or claws.'})
        shot.update(title=title, description=description, imagePrompt=prompt)
        shot['startingFrameDraft'] = dict(
            id=identifier+'-still-v04', image=image.relative_to(BASE).as_posix(),
            previousImage=shot['startingFrameSelection']['image'],
            userSelected=False, status='Revised composition draft; review pending',
            generationMode='built-in ImageGen edit', label=title,
            nativeWidth=width, nativeHeight=height)
    save(REGISTER, register)
    options = read(OUT/'review-options.json')
    save(OUT/'checkpoints/review-options-v42.json', options)
    options.update(sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v42.mp4',
        animaticVersion='v43',
        reviewIntro='V43 reshapes only the first flip into a compact asymmetrical U-shaped microbial vessel with soft rounded lobes, retaining the jade/plum colors. Color sequence: ivory, jade/plum, gold, rusty ochre. The junk ferry, captain, wardrobe, other stills and all frame timings are retained. These are held composition drafts for review.',
        presentation='V42 imagery with only the first flip ship reshaped; original master audio.',
        continuationNotes='V43 revises concourse-004 only: compact asymmetrical U-shaped microbial ship with rounded lobes, no hooks or claws, same jade/plum colors. Other imagery and timing retained. Original master audio verified. Final flip / Guess not timing remains provisional.')
    save(OUT/'review-options.json', options)
    save(OUT/'checkpoints/review-manifest-v42.json', read(OUT/'review-manifest.json'))
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
         tool='built-in ImageGen', animaticVersion='v43', status='Revised flips for user review', items=items))
    manifest = read(OUT/'manifest.json')
    manifest.update(fullAnimaticChanged=True, animaticVersion='v43',
        fullAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v43.mp4',
        revisedShots=list(CHANGES), timingCaveat=register['concourseSequence']['timingReview'])
    save(OUT/'manifest.json', manifest)
    checks = read(OUT/'verification.json')
    checks['flipRevisionV04'] = dict(revisedShots=list(CHANGES),
        unchangedOtherShotRecords=True, unchangedFrameGrid=True,
        exactSharedPromptLock=True, previousImagesRetained=True,
        fullAnimatic='v43', originalMasterAudio='AAC packet hashes verified by assembly tool')
    save(OUT/'verification.json', checks)
    print('Verified: only one shot record revised; prior images and all timing retained')
