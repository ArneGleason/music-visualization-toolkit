"""Merge a note-driven storyboard batch into a project's authoritative shotlist."""
import json
import pathlib

from timeline import MusicalGrid


def plan(project_file, batch_file, merge):
    base = pathlib.Path(project_file).resolve().parent
    project = json.loads(pathlib.Path(project_file).read_text(encoding='utf-8'))
    spec = json.loads(pathlib.Path(batch_file).read_text(encoding='utf-8'))
    path = base/'shots/shotlist.json'
    if path.exists() and not merge:
        raise ValueError('An existing shotlist requires --merge')
    doc = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'schemaVersion':1,'shots':[]}
    notes = json.loads((base/'generated/review/listening-notes.json').read_text(encoding='utf-8'))
    by_id = {n['id']:n for n in notes['notes']}
    fps = project['render']['fps']
    grid = MusicalGrid(json.loads((base/project['timing']['beatmap']).read_text(encoding='utf-8')))
    preview = json.loads((base/'generated/animatic/animatic-data.json').read_text(encoding='utf-8'))
    end = next(p['start'] for p in preview['phrases'] if p['id']==spec['endPhrase'])
    starts = [by_id[s['noteId']]['start'] for s in spec['shots']]
    if any(t is None for t in starts) or starts != sorted(set(starts)):
        raise ValueError('Batch notes need distinct ascending anchors')
    edges = [round(t*fps)+1 for t in starts+[end]]
    previous = {s['id']:s for s in doc['shots']}
    for i, blocking in enumerate(spec['shots']):
        a,b = edges[i:i+2]
        if b<=a:
            raise ValueError('Shot has no frames')
        note = by_id[blocking['noteId']]
        shot = dict(previous.get(blocking['id'], {}))
        for key in ('title','description'):
            shot.setdefault(key, blocking[key])
        shot.update(id=blocking['id'], batch=spec['id'], type='storyboard',
                    sourceNoteId=note['id'], sourceNoteText=note['text'], sourceNotesRevision=notes['revision'],
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
        previous[shot['id']] = shot
    doc['shots'] = sorted(previous.values(), key=lambda s:s.get('startFrame',0))
    doc['status'] = 'Partial creative plan; opening note batch plus preserved nine-zoom concept'
    doc['fps'] = fps
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    temp.replace(path)
    print(f"Merged {len(spec['shots'])} note shots; {len(doc['shots'])} total shots. Handles: {spec['handlesFrames']} frames each side.")
