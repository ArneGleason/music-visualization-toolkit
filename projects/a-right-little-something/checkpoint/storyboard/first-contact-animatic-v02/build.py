"""Render the shortened tour and longer Blender finale, then install V61."""
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
ROOT = BASE.parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')


plan = read(OUT/'assembly-plan.json')
data = read(BASE/'generated/animatic/animatic-data.json')
assert all(p['endFrameExclusive'] <= plan['startFrame'] for p in data['phrases']), 'Tail needs lyrics'
encoder = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
    '-s', '1920x1080', '-r', '24', '-i', '-', '-an', '-frames:v', str(plan['frames']),
    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
    str(OUT/'timed-still-board.mp4')], stdin=subprocess.PIPE)
try:
    for entry in plan['entries']:
        if entry['shot'] == 'contact-032':
            for frame in range(1, entry['frames']+1):
                with Image.open(OUT/f'finale-frames/frame_{frame:04d}.png') as im:
                    encoder.stdin.write(im.convert('RGB').tobytes())
        else:
            with Image.open(BASE/entry['image']) as im:
                pixels = im.convert('RGB').resize((1920,1080), Image.Resampling.LANCZOS).tobytes()
            for _ in range(entry['frames']):
                encoder.stdin.write(pixels)
        print('Rendered', entry['shot'], entry['frames'], 'frames', flush=True)
finally:
    encoder.stdin.close()
assert encoder.wait() == 0
subprocess.run([sys.executable, str(ROOT/'tools/insert_still_storyboard.py'),
    str(BASE/'project.json'), str(OUT/'review-options.json'), '--version', 'v61'], check=True)
path = BASE/'shots/shotlist.json'
register = read(path)
finale = next(s for s in register['storyboardProposals'] if s['id'] == 'contact-032')
finale['animaticPlacement'].update(kind='Blender composite of two separate still sources',
    compositor=(OUT/'finale-two-plates.blend').relative_to(BASE).as_posix(),
    sourcePlates=finale['compositePlan']['videoInputs'])
for entry in register['reviewEdits']['v61']['entries']:
    if entry['shot'] == 'contact-032':
        entry.update(finale['animaticPlacement'])
sequence = register['firstContactSequence']
sequence.pop('activeEditUnchanged', None)
sequence.update(status='V61 earlier finale assembled; timing review pending', animaticVersion='v61',
    reviewUrl='http://127.0.0.1:8768/?v=v61', timelineShotCount=36,
    travelInsertIds=[f'contact-{i:03d}-travel' for i in range(27,31)],
    assemblyPlan=(OUT/'assembly-plan.json').relative_to(BASE).as_posix(),
    timedPreview=(OUT/'timed-still-board.mp4').relative_to(BASE).as_posix(),
    timedPreviewStartFrame=plan['startFrame'],
    finaleBlender=(OUT/'finale-two-plates.blend').relative_to(BASE).as_posix(),
    finaleStartFrame=5031, finaleFrames=235, removedShotIds=['contact-031-travel'])
register['reviewEdits']['v61'].update(newPaidCredits=0, preservedVersion='v60',
    reviewStatus='Timing review pending', removedShotIds=['contact-031-travel'])
save(path, register)
save(OUT/'verification.json', dict(fullFrames=data['frames'], fps=24, width=1920, height=1080,
    insertStart=plan['startFrame'], insertEndExclusive=plan['endFrameExclusive'],
    insertFrames=plan['frames'], finaleStartFrame=5031, finaleStartSeconds=5030/24,
    finaleFrames=235, timelineShotCount=36, travelInserts=4,
    directPreviousShot='contact-031', removedShot='contact-031-travel',
    audio='Original V60 AAC packet hash verified by insertion tool', v60Preserved=True, newPaidCredits=0))
print('V61 ready: Harper by 3:30, direct galaxy cut, V60 preserved.', flush=True)
