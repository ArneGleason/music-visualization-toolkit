"""Register the still-review assets and exact presentation frames."""
import hashlib
import json
from pathlib import Path
from PIL import Image

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
def read(path):
    return json.loads(path.read_text(encoding='utf-8'))
def save(path,data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

inputs=read(OUT/'generation-input.json')
register=read(BASE/'shots/shotlist.json')
assert register['activeReviewEdit']=='v50'
shots={s['id']:s for s in register['storyboardProposals'] if s.get('batch')==inputs['batch']}
items={i['id']:i for i in inputs['items']}
framing=read(OUT/'render-framing.json') if (OUT/'render-framing.json').exists() else {}
for item in items.values():
    path=OUT/item['image']
    assert path.is_file() and path.stat().st_size>0,path
    with Image.open(path) as im:
        item.update(nativeWidth=im.width,nativeHeight=im.height,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    actual=OUT/(item['id']+'.prompt.txt')
    item['actualPrompt']=actual.read_text(encoding='utf-8') if actual.exists() else item['prompt']
    assert inputs['promptLock'] in item['actualPrompt'],item['id']

def segment(asset,start,end):
    result=dict(asset=asset,image=(OUT/items[asset]['image']).relative_to(BASE).as_posix(),
                startFrame=start,endFrameExclusive=end,frames=end-start)
    if asset in framing:
        result['editorialFraming']=framing[asset]
    return result

by_shot={
    'departure-001':[segment('signing',2595,2665)],
    'departure-002':[segment('undocking',2665,2753),segment('distant-station',2753,2805)],
    'departure-003':[segment('target-profile',2805,2873)],
    'departure-004':[segment(f'zoom-{c["cue"]:02d}',c['startFrame'],c['endFrameExclusive']) for c in shots['departure-004']['magnificationCues']],
    'departure-005':[segment('zoom-09',2920,2946),segment('planet-reveal',2946,2994)],
    'departure-006':[segment('cabin-distance',2994,3039)],
    'departure-007':[segment('affirmation',3039,3081)],
    'departure-008':[segment('confirm-course',3081,3144)],
}
for sid,segments in by_shot.items():
    shot=shots[sid]
    assert segments[0]['startFrame']==shot['startFrame']
    assert segments[-1]['endFrameExclusive']==shot['endFrameExclusive']
    assert sum(s['frames'] for s in segments)==shot['frames']
    item=items[segments[0]['asset']]
    shot.update(storyboardSegments=segments,promptLock=inputs['promptLock'],imagePrompt=item['actualPrompt'],
        startingFrameDraft=dict(id=item['boardItemId'],image=segments[0]['image'],userSelected=False,
            status='Generated still for timing review',generationMode='built-in ImageGen',
            nativeWidth=item['nativeWidth'],nativeHeight=item['nativeHeight']),
        status='Generated stills; timing review draft')
shots['departure-002']['stillPreviewNote']='Two held keyframes with a short dissolve preview the start/end of the planned continuous pullback. This is not final camera motion.'
register['departureDiscoverySequence'].update(status='Generated stills prepared for V51 timing review',
    generationStatus='17 built-in ImageGen stills; no Kling submission or charge',boardId=inputs['boardId'])
save(BASE/'shots/shotlist.json',register)
segments=[s for sid in by_shot for s in by_shot[sid]]
assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(segments,segments[1:]))
assert sum(s['frames'] for s in segments)==549
save(OUT/'review-options.json',dict(id=inputs['batch'],output=OUT.relative_to(BASE).as_posix(),
    sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v50.mp4',useMotion=False,draftForReview=True,
    presentation='Selected departure/discovery route with nine distinct held optical zoom views; still timing preview.',
    mediaLabel='Departure and jungle discovery / still timing review',
    continuationNotes='V51 adds selected route 1A-2A-3A-4A-5A-6B-7A-8B at2595–3144. Seventeen generated stills, nine separately timed zoom images, planet reveal2946. Undocking has two held pullback keyframes with a brief dissolve; native movement is not yet generated. V50 content and original master audio retained. No Kling spending.'))
save(OUT/'timing-check.json',dict(fps=24,startFrame=2595,endFrameExclusive=3144,frames=549,
    segments=segments,zoomCues=shots['departure-004']['magnificationCues'],planetRevealFrame=2946,
    pullbackPreviewDissolve=dict(startFrame=2747,endFrameExclusive=2759,frames=12)))
save(OUT/'review-manifest.json',dict(boardId=inputs['boardId'],animaticVersion='v51',tool='built-in ImageGen',
    status='Stills for timing review',items=list(items.values())))
board=OUT/'board'
board.mkdir(exist_ok=True)
ordered=['signing','undocking','distant-station','target-profile']+[f'zoom-{i:02d}' for i in range(1,10)]+['planet-reveal','cabin-distance','affirmation','confirm-course']
save(OUT/'gallery-manifest.json',[dict(id=i,src='../'+items[i]['image'],title=items[i]['title'],
    prompt=items[i]['actualPrompt'],output=items[i]['image']) for i in ordered])
print('Prepared 17 stills, 18 timed holds, 549 frames')
