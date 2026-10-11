"""Reverse the accepted departure picture, preserving lyric and edit timing."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
OLD = OUT.with_name('departure-discovery-motion-v01')
REPO = BASE.parents[1]

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def save(p, d):
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def run(args):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *args], cwd=OUT, check=True)

register = read(BASE/'shots/shotlist.json')
assert register['activeReviewEdit'] == 'v55'
save(OUT/'prior-shotlist.json', register)
source = BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v55.mp4'
run(['-i', str(OLD/'departure-departure-motion-v01-selected.mp4'),
     '-vf', 'reverse,setpts=N/(24*TB)', '-frames:v', '140', '-an',
     '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
     'departure-reversed-clean.mp4'])
lines = (OLD/'concat.txt').read_text().splitlines()
new_lines = []
for line in lines:
    name = line.split("'")[1]
    target = OUT/'departure-reversed-clean.mp4' if name == 'departure-departure-motion-v01-selected.mp4' else OLD/name
    new_lines.append("file '"+target.as_posix()+"'")
(OUT/'concat.txt').write_text('\n'.join(new_lines)+'\n')
run(['-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-an', '-c', 'copy', 'hybrid-picture.mp4'])
shutil.copy2(OLD/'lyrics.ass', OUT/'lyrics.ass')
shutil.copytree(OLD/'fonts', OUT/'fonts', dirs_exist_ok=True)
run(['-i', 'hybrid-picture.mp4', '-i', str(source), '-filter_complex',
     f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={2594/24}:end={3143/24},asetpts=PTS-STARTPTS[a]',
     '-map', '[v]', '-map', '[a]', '-frames:v', '549', '-c:v', 'libx264',
     '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
     '-b:a', '192k', '-movflags', '+faststart', 'timed-still-board.mp4'])
options = read(OLD/'review-options.json')
options.update(output=OUT.relative_to(BASE).as_posix(), sourceAnimatic=source.relative_to(BASE).as_posix(),
    presentation='Departure shot reversed; all other shots and timing retained',
    continuationNotes='V56: departure-002 reversed over the same 140 frames. Lyrics run forward; original master audio retained. No new generation or credits.')
save(OUT/'review-options.json', options)
subprocess.run([sys.executable, str(REPO/'tools/insert_still_storyboard.py'),
    str(BASE/'project.json'), str(OUT/'review-options.json'), '--version', 'v56'], check=True)

# Preserve prior reviewed metadata except for the explicitly revised departure.
current = read(BASE/'shots/shotlist.json')
register['activeReviewEdit'] = 'v56'
edit = copy.deepcopy(register['reviewEdits']['v55'])
edit.update(source=str(source), video=current['reviewEdits']['v56']['video'],
    type='Existing native assembly with reversed departure shot', newPaidCredits=0,
    presentation=options['presentation'])
register['reviewEdits']['v56'] = edit
shot = next(s for s in register['storyboardProposals'] if s['id']=='departure-002')
ref = (OUT/'departure-reversed-clean.mp4').relative_to(BASE).as_posix()
notes = 'V56: accepted clean departure picture played in reverse so the ship comes out from the station. Same 140 frames (2665–2804), forward lyrics, unchanged music; no new generation.'
retime = dict(operation='reverse', source=shot['motionSelection']['motionRef'], sourceFrames=140,
    firstSourceFrame=140, lastSourceFrame=1, fps=24, priorRetime=shot['motionSelection'].get('retime'))
selection = copy.deepcopy(shot['motionSelection'])
selection.update(id='departure-reversed-v56', motionRef=ref, sourceEditStartFrame=1,
    sourceLeadInFrames=0, availableLeadOutFrames=0, retime=retime,
    status='User-requested reversal; playback review pending', reviewNotes=notes)
shot.setdefault('motionTests', []).append(selection)
shot.update(motionSelection=selection, motionRef=ref, editorialDirection=notes,
    motionReview=dict(usable=True, notes=notes), status='Reversed departure in V56; playback review pending')
shot['stillPreviewNote'] = notes
for placement in shot['nativePlacements']:
    placement.update(motionRef=ref, sourceEditStartFrame=1, direction='reverse')
for s in register['storyboardProposals']:
    if s.get('batch')=='departure-discovery-v01':
        s['animaticPlacement']['animaticVersion']='v56'
        if s['id']=='departure-002':
            s['animaticPlacement'].update(kind='reversed native Kling motion', motionRef=ref,
                retime=retime, nativePlacements=shot['nativePlacements'])
for entry in edit['entries']:
    entry['animaticVersion']='v56'
    if entry['shot']=='departure-002':
        entry.update(kind='reversed native Kling motion', motionRef=ref, retime=retime,
            nativePlacements=shot['nativePlacements'])
seq=register['departureDiscoverySequence']
seq.update(status='V56 departure reversal ready', reviewUrl='http://127.0.0.1:8768/?v=v56',
    motionReviewUrl='http://127.0.0.1:8768/storyboard/departure-discovery-motion-v02/')
seq['motionRequest']['status']='Seven existing takes assembled in V56; departure reversed; no new spending'
save(BASE/'shots/shotlist.json',register)
opening=read(BASE/'generated/animatic/current-opening.json')
for item in opening['shots']:
    if item['id']=='departure-002': item['review']=shot['motionReview']
save(BASE/'generated/animatic/current-opening.json',opening)
save(OUT/'verification.json', dict(fullFrames=5265, passageFrames=549, reversedFrames=140,
    startFrame=2665, endFrameExclusive=2805, fps=24, originalMasterAudio='AAC packets verified identical to V55 by insertion tool', newCredits=0, cumulativeCredits=3384))
(OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Reversed departure — V56</title><style>body{background:#10282e;color:#efdfc0;font:16px system-ui;max-width:1100px;margin:24px auto}video{width:100%}a{color:#9bd9e9}</style><h1>Departure reversal — V56</h1><video controls src="timed-still-board.mp4"></video><p>Departure picture reversed; original timing and forward lyrics retained.</p><a href="/?v=v56">Full V56</a>',encoding='utf-8')
print('V56 reversal complete; no new credits.')
