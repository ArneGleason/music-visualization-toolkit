"""Merge a note-driven storyboard batch into a project's authoritative shotlist."""
import json
import pathlib
import copy

from timeline import MusicalGrid


def plan_musical_batch(project_file, spec, merge):
    """Plan from compiled lyric frames or musical positions without note fixtures."""
    base = pathlib.Path(project_file).resolve().parent
    project = json.loads(pathlib.Path(project_file).read_text(encoding='utf-8'))
    compiled = json.loads((base/project['timing']['compiledTimeline']).read_text(encoding='utf-8'))
    grid = MusicalGrid(json.loads((base/project['timing']['beatmap']).read_text(encoding='utf-8')))
    fps = project['render']['fps']
    phrases = {item['id']:item for track in compiled['tracks'] if track['type']=='lyrics' for item in track['items']}

    def anchor(value):
        if value == 'master-start':
            return 0
        if ':' in value:
            phrase, edge = value.split(':')
            if edge not in ('start', 'end'):
                raise ValueError(f'Unknown phrase edge: {edge}')
            return phrases[phrase][edge+'Frame']
        return round(grid.sec(value)*fps)

    path = base/'shots/shotlist.json'
    if path.exists() and not merge:
        raise ValueError('An existing shotlist requires --merge')
    doc = json.loads(path.read_text()) if path.exists() else {'schemaVersion':1,'shots':[]}
    if doc.get('shots') and doc.get('frameIndexBase') != 0:
        raise ValueError('Cannot merge zero-based anchors into an unmarked or one-based shotlist')
    edges = [anchor(s['startAnchor']) for s in spec['shots']] + [anchor(spec['endAnchor'])]
    if edges != sorted(set(edges)):
        raise ValueError('Shot anchors must be distinct and ascending')
    previous = {s['id']:s for s in doc['shots']}
    for item, start, end in zip(spec['shots'], edges, edges[1:]):
        shot = dict(previous.get(item['id'], {}))
        # Preserve authored creative changes on every merge; the batch seeds only
        # missing fields. Timing remains derived from the selected musical anchors.
        for key, value in item.items():
            shot.setdefault(key, copy.deepcopy(value))
        shot.setdefault('promptLock', spec['promptLock'])
        shot.setdefault('status', 'blocking_proposal_pending_animatic_review')
        shot.update(batch=spec['id'], startFrame=start, endFrameExclusive=end,
                    frames=end-start, startSeconds=start/fps, endSeconds=end/fps,
                    start=grid.position(start/fps).text(), end=grid.position(end/fps).text())
        previous[shot['id']] = shot
    doc.update(fps=fps, frameIndexBase=0, endFrameExclusive=edges[-1],
               status='Partial first-run blocking proposal; review before generated shot footage',
               shots=sorted(previous.values(), key=lambda s:s['startFrame']))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n')
    temporary.replace(path)
    print(f"Merged {len(spec['shots'])} musical-anchor shots, ending at frame {edges[-1]} exclusive")


def frame_anchor(item, frame_key, seconds_key, fps):
    if item.get(frame_key) is not None:
        return item[frame_key]
    if item.get(seconds_key) is None:
        raise ValueError('Batch notes need a frame or second anchor')
    return round(item[seconds_key]*fps)+1


def plan(project_file, batch_file, merge):
    base = pathlib.Path(project_file).resolve().parent
    project = json.loads(pathlib.Path(project_file).read_text(encoding='utf-8'))
    spec = json.loads(pathlib.Path(batch_file).read_text(encoding='utf-8'))
    if spec.get('format') == 'musical-anchors-v1':
        return plan_musical_batch(project_file, spec, merge)
    path = base/'shots/shotlist.json'
    if path.exists() and not merge:
        raise ValueError('An existing shotlist requires --merge')
    doc = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'schemaVersion':1,'shots':[]}
    notes = json.loads((base/'generated/review/listening-notes.json').read_text(encoding='utf-8'))
    by_id = {n['id']:n for n in notes['notes']}
    fps = project['render']['fps']
    grid = MusicalGrid(json.loads((base/project['timing']['beatmap']).read_text(encoding='utf-8')))
    preview = json.loads((base/'generated/animatic/animatic-data.json').read_text(encoding='utf-8'))
    end_phrase = next(p for p in preview['phrases'] if p['id']==spec['endPhrase'])
    phrases = {p['id']:p for p in preview['phrases']}
    starts = [frame_anchor(phrases[s['startPhrase']], 'startFrame', 'start', fps)
              if s.get('startPhrase') else
              frame_anchor(by_id[s['noteId']], 'start_frame', 'start', fps)
              for s in spec['shots']]
    if starts != sorted(set(starts)):
        raise ValueError('Batch notes need distinct ascending anchors')
    edges = starts+[frame_anchor(end_phrase, 'startFrame', 'start', fps)]
    register_key = 'storyboardProposals' if spec.get('proposal') else 'shots'
    previous = {s['id']:s for s in doc.get(register_key, [])}
    for sid in spec.get('supersedes', []):
        if sid in previous:
            retired = previous.pop(sid)
            retired['supersededByBatch'] = spec['id']
            doc.setdefault('supersededStoryboardProposals', []).append(retired)
    for i, blocking in enumerate(spec['shots']):
        a,b = edges[i:i+2]
        if b<=a:
            raise ValueError('Shot has no frames')
        note = by_id.get(blocking.get('noteId'))
        if note is None and not blocking.get('sourceDirection'):
            raise ValueError('A phrase-anchored shot needs its authored source direction')
        shot = dict(previous.get(blocking['id'], {}))
        if blocking.get('replaceCreative') and shot and shot.get('batch') != spec['id']:
            shot.setdefault('directionHistory', []).append({
                'supersededByBatch':spec['id'],
                **{k:copy.deepcopy(shot[k]) for k in
                   ('title','description','blocking','generationApproach','editGroup',
                    'startFrame','endFrameExclusive') if k in shot}})
        for key in ('title','description'):
            if blocking.get('replaceCreative'):
                shot[key] = blocking[key]
            else:
                shot.setdefault(key, blocking[key])
        shot.update(id=blocking['id'], batch=spec['id'], type='storyboard',
                    sourceNoteId=note['id'] if note else None,
                    sourceNoteText=note['text'] if note else None,
                    sourceNotesRevision=notes['revision'] if note else None,
                    start=str(grid.position((a-1)/fps)), end=str(grid.position((b-1)/fps)),
                    startFrame=a, endFrameExclusive=b, frames=b-a,
                    startSeconds=(a-1)/fps, endSeconds=(b-1)/fps,
                    handles={'leadInFrames':spec['handlesFrames'], 'leadOutFrames':spec['handlesFrames'],
                             'generatedFrames':b-a+2*spec['handlesFrames'],
                             'editInLocalFrame':spec['handlesFrames']+1,
                             'editOutLocalFrameExclusive':spec['handlesFrames']+1+b-a,
                             'sourceStartFrame':a-spec['handlesFrames'],
                             'sourceEndFrameExclusive':b+spec['handlesFrames']},
                    blocking=blocking, status=shot.get('status','Blender composition draft; review before image generation'))
        if blocking.get('sourceDirection'):
            shot['sourceDirection'] = blocking['sourceDirection']
            shot['directionSource'] = 'User conversation; phrase anchors from existing timing grid'
        for key in ('promptLock', 'generationApproach', 'continuity', 'editGroup', 'lyrics'):
            if key in blocking:
                shot[key] = blocking[key]
        previous[shot['id']] = shot
    doc[register_key] = sorted(previous.values(), key=lambda s:s.get('startFrame',0))
    if not spec.get('proposal'):
        doc['status'] = 'Partial creative plan; opening note batch plus preserved nine-zoom concept'
    doc['fps'] = fps
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    temp.replace(path)
    print(f"Merged {len(spec['shots'])} note shots; {len(doc['shots'])} total shots. Handles: {spec['handlesFrames']} frames each side.")
