"""Save the selected departure/zoom route, preserving the accepted V50 edit."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen

BASE = Path(__file__).resolve().parents[2]
BATCH = 'departure-discovery-v01'
API = 'http://127.0.0.1:8768/api/notes'
now = datetime.now(timezone.utc).isoformat()
path = BASE/'shots/shotlist.json'
original = path.read_bytes()
register = json.loads(original)
timing = json.loads((BASE/'generated/animatic/animatic-data.json').read_text(encoding='utf-8'))
phrases = {p['id']:p for p in timing['phrases']}
words = {w['id']:w for p in timing['phrases'] for w in p['words']}
assert timing['fps'] == 24 and register['activeReviewEdit'] == 'v50'
assert not any(s.get('batch') == BATCH for s in register['storyboardProposals'])

rows = [
    ('1A', 'Sign for the ship', phrases['lyr-040']['startFrame'], 'lyr-040 start',
     'Medium two-shot at the berth. A clearly different owner offers an illuminated transfer panel. Harper signs with a fingertip; the owner releases a compact control token into her hand. One legible agreement and handover establishes permission to take the ship.',
     'Keep the existing berth and survival coverall. Owner is distinct from the rejected ferry captain. Cut past boarding mechanics into departure; no invented view through the ship port.'),
    ('2A', 'Careful undocking into the bigger sky', phrases['lyr-041']['startFrame'], 'lyr-041 start',
     'One continuous exterior shot through To the bigger sky beyond and Everything so far aways. The spherical ship backs carefully clear of the berth, makes a small steering correction and turns outward. Camera retreats increasingly far until the station becomes a tiny point.',
     'Ship moves cautiously like backing out a new vehicle; camera provides most of the apparent speed. No extra near-identical cut at Everything. Preserve recognizable ship geometry before the vast pullback.'),
    ('3A', 'Select a distant target', phrases['lyr-042']['endFrameExclusive'], 'lyr-042 end; gap before Hit zoom',
     'Interior side-profile medium. Harper studies a distant point through the virtual dome. A sparse holographic finger control appears beneath her raised hand. She selects the point and gives one precise input on Hit zoom.',
     'Use the pause before Hit zoom to establish her hand and the dome. Match the accepted opening cabin rather than inventing an interior. Keep the same warm-gray coverall. Carry through the first Zoom into the first in cue.'),
    ('4A', 'Nine distinct magnification steps', words['lyr-044-w02']['startFrame'], 'first performed in cue',
     'Nine near-static optical views, each with a substantial magnification change on its performed in cue. Progress from dense starfield through isolated stellar neighbourhood, target system and orbital regions toward the distant planetary disc. Target remains anchored for readability.',
     'Clean rhythmic steps, not nine character shots. Large changes in scale and information density prevent stuttering. Avoid full-screen white flashes, unnecessary interface clutter and small zoom resets. Final planet geography resolves on big now after the nine cues.'),
    ('5A', 'Reveal the new jungle world', words['lyr-044-w11']['startFrame'], 'to see far things tail after ninth in',
     'Finish resolving the target through To see far things. On big now reveal a clean full-frame portrait of a wholly different planet. Hold through the first part of So far and so long aways, allowing the reveal to register.',
     'Selected design direction: vast dark-emerald jungle continent, copper-coloured inland seas, broad ivory storm systems. Distinct from the opening turquoise world with peach clouds and dark islands. This is a magnified remote view, not instantaneous arrival. Exact surface design awaits still review.'),
    ('6B', 'Distance within the dome', words['lyr-045-w05']['startFrame'], 'long in lyr-045',
     'Wide cabin view from a distinctly different angle. The magnified planet occupies the virtual dome while Harper is small below it. A sparse route graphic unfolds over an enormous span, making remaining distance apparent without explanatory text.',
     'Hard change of composition from full-frame planet to wide cabin. Keep the remote planet visibly part of the dome display; ship has not arrived. Hold through the gap before the affirmation.'),
    ('7A', 'Quiet affirmation', phrases['lyr-046']['startFrame'], 'lyr-046 start',
     'Three-quarter frontal close reaction. Harper studies the discovery; concentration settles into quiet satisfaction, a small breath or almost-nod rather than another broad smile.',
     'Affirm finding somewhere worth going. This does not imply she has already helped the planet. A clear wide-to-close change from the preceding cabin shot.'),
    ('8B', 'Confirm the course', phrases['lyr-047']['startFrame'], 'lyr-047 start through lyr-048',
     'Tight hand-and-control insert. On Something and With it all you did right, Harper confirms the destination. Scattered search marks resolve into one purposeful course; her hand settles.',
     'One shot across both phrases. Cut from the small decisive action to the expansive jungle setting at the second chorus. Actual arrival, travel ellipse and chorus action remain to be planned.'),
]
end = phrases['lyr-049']['startFrame']
assert [r[2] for r in rows]+[end] == [2595,2665,2805,2873,2920,2994,3039,3081,3144]
proposals = []
for i,(choice,title,start,basis,description,motion) in enumerate(rows):
    stop = rows[i+1][2] if i+1 < len(rows) else end
    proposals.append(dict(id=f'departure-{i+1:03d}',batch=BATCH,title=title,type='concept',
        selectedOption=choice,status='User-selected direction; stills and motion not generated',
        startFrame=start,endFrameExclusive=stop,frames=stop-start,startSeconds=(start-1)/24,
        endSeconds=(stop-1)/24,timingBasis=basis,description=description,motionDirection=motion,
        sourceNoteId=f'departure-{i+1:03d}-direction-oct11'))
cue_words = [w for w in phrases['lyr-044']['words'] if w.get('zoomCue')]
cues = [dict(cue=w['zoomCue'],startFrame=w['startFrame'],
             endFrameExclusive=cue_words[i+1]['startFrame'] if i+1<len(cue_words) else 2920,
             timingBasis=w['id']) for i,w in enumerate(cue_words)]
assert len(cues)==9 and sum(c['endFrameExclusive']-c['startFrame'] for c in cues)==47
proposals[3]['magnificationCues']=cues
proposals[4]['planetRevealFrame']=words['lyr-044-w15']['startFrame']
assert proposals[4]['planetRevealFrame']==2946
register['storyboardProposals'].extend(proposals)
register['departureDiscoverySequence']=dict(id=BATCH,selectedOn='2026-10-11',
    selectedPath=[r[0] for r in rows],status='Selected text direction; timing markers saved',
    startFrame=2595,endFrameExclusive=3144,frames=549,
    sourceDirection='User selected the full preferred path, explicitly choosing nine-step 4A after considering 4B.',
    magnificationCues=cues,planetRevealFrame=2946,
    continuityNotes=['Preserve established adult Harper, gray survival coverall, spherical ship and accepted opening cabin.',
        'Dome magnifies a remote target; no instantaneous travel to the new planet.',
        'Adjacent main shots change viewpoint, subject or scale decisively; nine zoom cuts intentionally retain target anchoring.',
        'Planet design direction selected; exact stills and second-chorus arrival/action remain undeveloped.'],
    generationStatus='No images or videos generated; no new spending')
register['reviewEdits']['v50'].update(userSelected=True,status='User accepted on 2026-10-11')
for entry in register['reviewEdits']['v50']['entries']:
    entry['userSelected']=True
for shot in register['storyboardProposals']:
    if shot.get('batch') == 'station-concourse-v05':
        shot['status']='User accepted in V50 on 2026-10-11'
        for key in ['motionSelection','animaticPlacement']:
            if key in shot:
                shot[key]['userSelected']=True
register['concourseSequence']['handoff']='At frame2595 Harper is still outside. The selected continuation starts with an owner signing/handover, then cuts past boarding to careful undocking.'

with urlopen(API,timeout=10) as response:
    notes=json.load(response)
original_notes=json.loads(json.dumps(notes))
assert not any(n.get('batch')==BATCH for n in notes['notes'])
for p in proposals:
    text=f"Departure / {p['title']} ({p['selectedOption']})\n\nSelected direction: {p['description']}\n\nStaging: {p['motionDirection']}\n\nFrames {p['startFrame']}–{p['endFrameExclusive']} (end exclusive); {p['timingBasis']}. Selected text plan; stills and motion not generated."
    if p.get('magnificationCues'):
        text+='\n\nNine in cue frames: '+', '.join(str(c['startFrame']) for c in cues)+'. Each is a separate magnification step.'
    if p.get('planetRevealFrame'):
        text+='\n\nFull planet reveal on big at frame2946; now begins frame2953.'
    notes['notes'].append(dict(id=p['sourceNoteId'],sourceRecording=None,start=p['startSeconds'],end=p['endSeconds'],
        kind='idea',text=text,status='open',resolution='',created_at=now,updated_at=now,
        start_frame=p['startFrame'],end_frame=p['endFrameExclusive'],anchor_label=f"Departure / frame {p['startFrame']}",
        sourceShotId=p['id'],batch=BATCH))
for note in notes['notes']:
    if note['id']=='concourse-handoff-direction-oct11':
        note['text']='Concourse / Handoff to All, all calling\n\nV50 accepted. Harper remains outside after approaching the ship. The selected next scene is an owner signing/handover at frame2595, then careful undocking at2665. Boarding is elided between shots; preserve the established cabin and gray survival coverall.'
        note['updated_at']=now
backup=BASE/'generated/review/checkpoints'/('departure-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S'))
backup.mkdir(parents=True)
(backup/'shotlist.json').write_bytes(original)
(backup/'listening-notes.json').write_text(json.dumps(original_notes,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert path.read_bytes()==original
path.write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
request=Request(API,data=json.dumps(notes,ensure_ascii=False).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
with urlopen(request,timeout=10) as response:
    saved=json.load(response)
assert saved['revision']==original_notes['revision']+1
assert len(saved['notes'])==len(original_notes['notes'])+8
print('Saved 8 selected directions, 9 zoom cues and V50 acceptance. Notes revision',saved['revision'])
