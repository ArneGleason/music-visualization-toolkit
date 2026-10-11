import json
import pathlib
import urllib.request
from datetime import datetime, timezone

base = pathlib.Path(__file__).resolve().parents[2]
data = json.loads((base / 'generated/animatic/animatic-data.json').read_text(encoding='utf-8'))
phrases = {p['id']: p for p in data['phrases']}
direction = ('User direction October 10: only chorus 1 and chorus 2. Chorus 1 begins around 43.5s on How much can you do with it all? Harper intends to positively influence worlds with nascent life and accelerate their progress; consequences remain ambiguous. Plan a general arc, not a cut per lyric. Explore jump-cut or zoom-out-blur entry, zoom blurs or fades within the chorus, and one-second handles each side. A/B ideas below are assistant proposals for discussion, not selected imagery.')
ideas = [
    ('chorus1-01', 'lyr-015', 'Chorus 1 / What is her mission?',
     'A — Living-world invitation: zoom out from the coast tide into an immense shallow basin of nascent alien colonies; Harper is small at its edge, studying a stalled living pattern. Match the curved tide to the colony shape. Her attention conveys care before any intervention.',
     'B — Worlds in her care: jump or zoom-out blur into an oblique view of Harper beside several enlarged living-world projections. Each contains a distinct simple ecosystem rather than an abstract planet icon. She studies their differences and chooses one; this reads as a mission with multiple destinations.',
     'Entry alternatives: a decisive jump cut on the question, or a brief zoom-out blur linking tide/basin to world/projection. This proposes replacing the tail of space-011 from frame 1046; retain its accepted still and v11 until a branch is selected.'),
    ('chorus1-02', 'lyr-016', 'Do something / Little something: a modest intervention',
     'A — Open a channel: one quiet gesture redirects a small trickle of water toward a dormant fan-frond colony. The flow travels through the scene; first one organism opens, then its neighbors respond. Hold through Little something rather than cutting for both phrases.',
     'B — Offer a catalyst: she releases a tiny luminous seed-like instrument into a young alien habitat. Local creatures approach it and reorganize their activity in their own way. Keep the catalyst modest; its light becomes a transition anchor, not an explosion or instant advanced civilization.',
     'Possible gentle dissolve between intention and response, or a short matched zoom blur toward the small intervention. A can continue the same world; B can follow either mission framing.'),
    ('chorus1-03', 'lyr-018', 'You’re something / A right little something: agency and uncertainty',
     'A — The world answers back: pull back from the opening colony to Harper, now dwarfed by spreading life. At one edge the new growth diverts water from another patch. She notices and pauses: hopeful response with an unresolved ecological cost, not a disaster reveal.',
     'B — The result exceeds the plan: the catalyst starts a beautiful branching pattern; living inhabitants reroute it into something different from her intended design. A close reaction shows fascination and a trace of doubt. A right little something can refer to her, the catalyst, or the unpredictable living result.',
     'Let the intervention develop across both phrases. Avoid separate literal illustrations for each something. Carry a light pulse or branching shape toward the orbit passage.'),
    ('chorus1-04', 'lyr-020', 'Out here in orbit / first cosmic expansion',
     'A — Ripples become routes: lift away from the living branching pattern until its curves match orbital arcs around the world. Harper’s tiny ship enters a broad stellar composition; a faint outgoing arc suggests the next destination.',
     'B — A constellation of visits: fade from her attentive face into several star systems at different depths, with sparse flowing paths joining their worlds. One pulse leaves the current system. Keep this cosmic and painterly; no route labels, checklist, or dense dashboard.',
     'Move from local care into scale and distance. Allow the sung line and its tail to breathe in one composition; matched zoom blur or dissolve are alternatives.'),
    ('chorus1-05', 'echo-001', 'Orbit echo / exploration and interference',
     'A — Echoing visits: the initial orbital ripple repeats at two or three increasingly distant star systems. Each pulse meets a different living-world pattern; one opens, one bends it, one absorbs it. This hints that identical good intentions have different effects.',
     'B — An unfinished itinerary: a delicate branching exploration path grows across a cosmic field. Some branches remain dim and unvisited; one slowly curls back toward its source. The pattern can resemble both navigation and a living neural/mycelial network without explaining which it is.',
     'Carry through the echo and instrumental space up to I’m just a creature of nature at frame 1550. Return to intimate Harper coverage there. Test soft overlaps or repeat zoom blurs at musical accents, not an automatic cut for every echo.')
]
with urllib.request.urlopen('http://127.0.0.1:8768/api/notes') as response:
    doc = json.load(response)
original = json.loads(json.dumps(doc))
now = datetime.now(timezone.utc).isoformat()
shots = []
for ident, phrase_id, title, a, b, transition in ideas:
    p = phrases[phrase_id]
    frame = p['startFrame']
    text = f'{title}\n\n{direction}\n\n{a}\n\n{b}\n\nCut/continuity: {transition}\n\nBranches may be mixed; these are imagery markers, not locked cuts. Reserve 24-frame lead-in and lead-out handles for new chorus footage.'
    note_id = ident + '-ideas-oct10'
    if not any(n['id'] == note_id for n in doc['notes']):
        doc['notes'].append(dict(id=note_id, sourceRecording=None, start=(frame-1)/24, end=(frame-1)/24, kind='idea', text=text, status='open', resolution='', created_at=now, updated_at=now, start_frame=frame, end_frame=frame, anchor_label=f'Chorus 1 · frame {frame} · {(frame-1)/24:.2f}s'))
    shots.append(dict(id=ident, noteId=note_id, startPhrase=phrase_id, title=title, description=a+'\n\n'+b, sourceDirection=direction, transition=transition, alternatives={'A': a, 'B': b}, selection=None, generationApproach='Ideas only; select imagery and review animatic before generation. New chorus sources reserve 24 frames each side.', status='A/B imagery proposal; no branch selected'))
request = urllib.request.Request('http://127.0.0.1:8768/api/notes', data=json.dumps(doc).encode(), headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(request) as response:
    saved = json.load(response)
assert saved['notes'][:len(original['notes'])] == original['notes']
spec = dict(id='chorus1-ideas-v01', proposal=True, handlesFrames=24, endPhrase='lyr-021', sourceDirection=direction, shots=shots)
(base / 'storyboard-chorus1-ideas-v01.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f"Saved five A/B markers; notes revision {saved['revision']}. Preserved all {len(original['notes'])} existing notes.")
