"""Record the user-selected concourse route and append revision-checked notes."""
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen


BASE = Path(__file__).resolve().parents[2]
BATCH = 'station-concourse-v01'
API = 'http://127.0.0.1:8768/api/notes'
now = datetime.now(timezone.utc).isoformat()
shot_path = BASE / 'shots/shotlist.json'
original_shots = shot_path.read_bytes()
shots = json.loads(original_shots)
timing = json.loads((BASE / 'generated/animatic/animatic-data.json').read_text(encoding='utf-8'))
fps = timing['fps']
assert fps == 24
phrases = {p['id']: p for p in timing['phrases']}
words = {w['id']: w for p in timing['phrases'] for w in p['words']}
beats = {(b['bar'], b['beat']): b for b in timing['beats']}

rows = [
    ('Arrival at the transport hub', phrases['lyr-035']['startFrame'],
     'lyr-035 start', 'All the way to the next channel.',
     'The ivory-and-graphite escape pod is already close to a branching station docking ring. Diverse moored craft and a little arriving traffic establish a hub of onward choices. Let the pod enter a docking inlet; imply elapsed travel since the rolling departure.',
     'Wide exterior; one clear pod movement into the station. Cut past the mechanics of docking before the concourse view.'),
    ('Concourse and a brief directory', phrases['lyr-036']['startFrame'],
     'lyr-036 start', 'Turn the channel.',
     'Harper is now on the station promenade after a docking ellipse. A small luminous directory or ship-symbol display briefly orients her; her gaze turns from it to real ships beyond the windows and departure gates. Expose the station geography in the same composition.',
     'One turn of her gaze opens the view along the berths. Keep the directory secondary and quickly readable.'),
    ('A promising departure', phrases['lyr-037']['startFrame'],
     'lyr-037 start', 'I think my movie z\u2019on.',
     'She spots an inviting passenger craft at a real berth. A small interested reaction and a movement toward its entrance suggest that she may have found a good way onward.',
     'Her eyeline motivates the upcoming ship comparisons; avoid squeezing a complete walk to the berth into this short phrase.'),
    ('Flip 1 - sleek shuttle', words['lyr-038-w01']['startFrame'],
     'lyr-038-w01 start', 'Flip,',
     'A real sleek, spacious passenger shuttle seen at its boarding entrance. This is the first distinct transport option in the quick comparison montage.',
     'Hard cut on the first flip. Establish a doorway/boarding-ramp composition that the following options can match.'),
    ('Flip 2 - cramped freighter', words['lyr-038-w02']['startFrame'],
     'lyr-038-w02 start', 'flip,',
     'A bulky freight transport with a narrow, cluttered boarding ramp. Its silhouette and cramped entry read immediately as a different option.',
     'Hard cut on the second flip, retaining the comparable boarding-entrance framing. Editorial montage compresses movement between berths.'),
    ('Flip 3 - terrible ferry and suspect captain', words['lyr-038-w03']['startFrame'],
     'lyr-038-w03 provisional start', 'flip. / Guess',
     'A dreadful little ferry with patched hull, dangling equipment and a dubious ramp. An overly eager captain is already beckoning Harper aboard. Make the ship visibly unappealing at a glance; the captain completes the offer.',
     'Third quick cut reveals the ferry and captain together. Retain this situation through the rejection and into the instrumental; the offer needs more time than this short initial reveal.'),
    ('Guess not - rejection beat', words['lyr-039-w02']['startFrame'],
     'lyr-039-w02 not start; proposed reaction cue', 'Guess not.',
     'Harper assesses the offer, gives a flat, unconvinced look and starts turning away. This marker accents her response on not; it does not redefine the onset of Guess.',
     'Reaction/action marker, not a required new cut. Continue the reaction into the next instrumental marker so it remains readable.'),
    ('Leave the public berths', phrases['lyr-039']['endFrameExclusive'],
     'lyr-039 endFrameExclusive', 'Instrumental begins',
     'Complete the rejection and leave the ferry captain behind. Harper continues beyond the busy public berths toward a quieter peripheral route.',
     'Continue from the rejection, then follow her departure. This boundary can remain inside the same shot; no lip-sync performance during the instrumental.'),
    ('The quiet outer walkway', beats[(38, 1)]['frame'],
     'bar 38 beat 1', 'Instrumental',
     'She follows an outer walkway or service passage beyond the main terminal. Crowds, signs and busy departures fall away. Preserve a legible route through the same station.',
     'A calmer following or lateral view makes the passage feel exploratory. Carry the previous walking direction.'),
    ('A familiar glimmer at the remote berth', beats[(39, 1)]['frame'],
     'bar 39 beat 1', 'Instrumental',
     'At the remote end of the docks, Harper notices a fragment of cyan engine-ring light and an amber platform edge beyond an opening. She slows and changes course toward it.',
     'Reveal only a recognizable fragment first, then connect it to her attention and approach. Save the full spherical silhouette for the next beat.'),
    ('Discover and board the opening ship', beats[(40, 3)]['frame'],
     'bar 40 beat 3', 'Instrumental into All, all calling',
     'Reveal the established spherical personal spacecraft alone at a quiet outlying berth, with open space behind it. Harper crosses the final access bridge and boards; settle with her inside by the next vocal at frame 2595.',
     'Allow the full reveal to breathe before her approach and boarding. Further subdivision within this span remains a blocking decision. Establish a compatible cabin view for All, all calling.'),
]
end_frame = phrases['lyr-040']['startFrame']
assert [r[1] for r in rows] + [end_frame] == [2105, 2139, 2167, 2192, 2203, 2211, 2223, 2229, 2294, 2359, 2458, 2595]
assert not any(s.get('batch') == BATCH for s in shots['storyboardProposals']), 'Route already recorded'

timing_review = ('The third flip and Guess currently share provisional frame 2211; the third flip word has a zero-frame compiled span. Review this region against playback before locking cuts. Frame 2223 is the current not onset and a proposed reaction cue. Existing lyric timing is retained.')
continuity = [
    'Selected route: physical dockside concourse with a brief directory for orientation; the three flip cuts show real ships.',
    'Continue the painted graphic-novel look and established adult Harper identity.',
    'Arrival uses the enclosed ivory-and-graphite ovoid escape pod; discovery uses the established spherical personal ship from the opening.',
    'The spherical ship retains its thin transparent cyan geodesic field, graphite platforms and equatorial band, amber edges and vertical cyan engine ring.',
    'Wardrobe continuity from the escape silver halter outfit to the opening gray outfit remains to be staged before image generation; do not silently change clothing between adjacent views.',
    'Direction is selected; frame anchors are proposed blocking cues, with captain/rejection timing pending playback review.',
]
shots['concourseSequence'] = {
    'id': BATCH, 'selectedOn': '2026-10-11',
    'status': 'User selected concourse route with brief directory; timed direction markers saved',
    'sourceDirection': 'User: go with the concourse path and the recommended small directory orientation, then actual ship options and discovery of the opening ship.',
    'startFrame': rows[0][1], 'endFrameExclusive': end_frame,
    'timingReview': timing_review, 'continuityNotes': continuity,
}
proposals = []
for i, (title, start, basis, lyric, description, motion) in enumerate(rows):
    end = rows[i+1][1] if i+1 < len(rows) else end_frame
    proposals.append({
        'id': f'concourse-{i+1:03d}', 'batch': BATCH,
        'title': title, 'type': 'concept',
        'status': 'User-selected narrative direction; proposed marker and blocking',
        'startFrame': start, 'endFrameExclusive': end, 'frames': end-start,
        'startSeconds': (start-1)/fps, 'endSeconds': (end-1)/fps,
        'timingBasis': basis, 'lyrics': [lyric],
        'description': description, 'motionDirection': motion,
        'sourceNoteId': f'concourse-{i+1:03d}-direction-oct11',
        'handles': {'leadInFrames': 24, 'leadOutFrames': 24,
                    'status': 'Reserve for later native footage where separate shots are generated'},
    })
shots['storyboardProposals'].extend(proposals)

with urlopen(API, timeout=10) as response:
    notes = json.load(response)
original_notes = json.loads(json.dumps(notes))
assert not any(n['id'].startswith('concourse-') for n in notes['notes']), 'Notes already recorded'
for p in proposals:
    text = (f"Concourse / {p['title']}\n\nSelected direction: {p['description']}\n\n"
            f"Staging: {p['motionDirection']}\n\n"
            f"Proposed span: frames {p['startFrame']}-{p['endFrameExclusive']} (end exclusive); "
            f"anchor: {p['timingBasis']}. Canonical direction: shots/shotlist.json, {p['id']}.")
    if p['id'] in ('concourse-006', 'concourse-007'):
        text += '\n\nTiming review: ' + timing_review
    note = {
        'id': p['sourceNoteId'], 'sourceRecording': None,
        'start': p['startSeconds'], 'end': p['startSeconds'], 'kind': 'idea',
        'text': text, 'status': 'open', 'resolution': '',
        'created_at': now, 'updated_at': now,
        'start_frame': p['startFrame'], 'end_frame': p['startFrame'],
        'anchor_label': f"Concourse / frame {p['startFrame']}",
        'sourceShotId': p['id'], 'batch': BATCH,
    }
    notes['notes'].append(note)
notes['notes'].append({
    'id': 'concourse-handoff-direction-oct11', 'sourceRecording': None,
    'start': (end_frame-1)/fps, 'end': (end_frame-1)/fps, 'kind': 'idea',
    'text': 'Concourse / Handoff to All, all calling\n\nBy this cue Harper has found and boarded the spherical ship seen at the beginning. Settle into an established cabin view for the return of the vocal. Resolve the silver-to-gray wardrobe bridge during blocking before creating the new imagery. This is the end of the selected concourse passage; the onward flight is the next direction task.',
    'status': 'open', 'resolution': '', 'created_at': now, 'updated_at': now,
    'start_frame': end_frame, 'end_frame': end_frame,
    'anchor_label': f'Concourse handoff / frame {end_frame}', 'batch': BATCH,
})

backup = BASE / 'generated/review/checkpoints' / ('concourse-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S'))
backup.mkdir(parents=True)
(backup / 'shotlist.json').write_bytes(original_shots)
(backup / 'listening-notes.json').write_text(json.dumps(original_notes, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
assert shot_path.read_bytes() == original_shots, 'Shotlist changed while preparing'
shot_path.write_text(json.dumps(shots, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
request = Request(API, data=json.dumps(notes, ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
with urlopen(request, timeout=10) as response:
    saved = json.load(response)
assert saved['revision'] == original_notes['revision'] + 1
assert saved['notes'][:len(original_notes['notes'])] == original_notes['notes']
assert len(saved['notes']) == len(original_notes['notes']) + 12
print(json.dumps({'storyboardDirections':len(proposals), 'newNotes':12, 'notesRevision':saved['revision'], 'spanFrames':[rows[0][1],end_frame], 'originalNotesPreserved':True}))
