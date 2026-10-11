import json
from pathlib import Path

base = Path('projects/a-right-little-something')
def load(path):
    return json.loads(path.read_text(encoding='utf-8'))
def save(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

direction = (base/'LAB-VERSE-DIRECTION.md').read_text(encoding='utf-8')
lock = next(line for line in direction.splitlines() if line.startswith('PROMPT LOCK:'))
rows = [line.split('|')[1:-1] for line in direction.splitlines() if line.startswith('| lab2-')]
data = load(base/'generated/animatic/animatic-data.json')
phrases = {p['id']:p for p in data['phrases']}
ids = ['lyr-021','lyr-022','lyr-023','lyr-025','lyr-026','lyr-027','lyr-028','lyr-029','lyr-030']
starts = [phrases[x]['startFrame'] for x in ids]
end = phrases['lyr-031']['startFrame']
assert starts == [1550,1596,1624,1698,1743,1762,1809,1838,1869]
register = load(base/'shots/shotlist.json')
existing = {s['id'] for s in register['storyboardProposals']}
moves = [
    ([1.10,1.04],[.45,.56],[.4,.4]),
    ([1.12,1.025],[.7,.5],[.4,.45]),
    ([1.12,1.08],[.12,.85],[.5,.5]),
    ([1.10,1.035],[.35,.65],[.45,.45]),
    ([1.04,1.09],[.5,.5],[.4,.4]),
    ([1.20,1.035],[.55,.5],[.5,.5]),
    ([1.08,1.035],[.15,.8],[.45,.45]),
    ([1.10,1.045],[.8,.2],[.45,.45]),
    ([1.15,1.025],[.6,.45],[.5,.5])]
for i,(row,phrase_id) in enumerate(zip(rows,ids)):
    ident, _, description, motion = [x.strip() for x in row]
    stop = starts[i+1] if i < len(starts)-1 else end
    image = f'generated/storyboard/lab-verse-v01/{ident}.png'
    shot = dict(id=ident,batch='lab-verse-v01',title=description.split(':')[0],
        description=description,startPhrase=phrase_id,startFrame=starts[i],endFrameExclusive=stop,
        frames=stop-starts[i],lyrics=[phrases[phrase_id]['text']],promptLock=lock,
        sourceDirection='User October 10: origin flashback, grown by bizarre function-specific robots aboard headquarters lab ship; constraints loosen, fingers solve, concentration, then cosmic exteriors.',
        generationApproach=motion+' Later native footage should provide at least 24 source frames each side; review still animatic first.',
        motionDirection=motion,handles=dict(leadInFrames=24,leadOutFrames=24,status='planned for later native animation'),
        cameraMove=dict(zip(('zoom','panX','panY'),moves[i])),
        startingFrameDraft=dict(id=ident+'-v01',image=image,userSelected=False,
            status='Generated composition draft',generationMode='built-in ImageGen',label=description),
        status='Generated composition draft; review pending')
    if ident not in existing:
        register['storyboardProposals'].append(shot)
save(base/'shots/shotlist.json',register)
spec = dict(id='lab-verse-v01',output='generated/storyboard/lab-verse-v01',
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v25.mp4',
    fadeFrames=4,entryFadeFrames=8,
    entryPlate='generated/storyboard/orbit-blender-v03/hybrid/orbit-composite-handles.mp4',entryPlateFrame=162,
    draftForReview=True,presentation='Existing Kling and Blender sequence through orbit, followed by nine generated stills with purposeful eased camera moves; no native motion in new verse yet.',
    mediaLabel='Kling / Blender orbital flight / lab verse still drafts',
    continuationNotes='V26 extends the accepted v25 through the headquarters origin flashback and Bright night. New verse uses nine generated stills with editorial camera moves, short fades and exact phrase anchors. New imagery awaits user review; later motion notes are canonical. Hold last still to next phrase frame1958 /81.54s. Original master audio and full5265frames preserved.')
save(base/'storyboard-lab-verse-v01.json',spec)
save(base/'generated/storyboard/lab-verse-v01/shot-directions.json',dict(promptLock=lock,shots=[s for s in register['storyboardProposals'] if s.get('batch')==spec['id']]))
print('Registered nine drafts from lyric grid:', starts[0],end)
