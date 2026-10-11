"""Register a planet-only replacement draft while retaining prior experiments."""
import argparse
import copy
import json
import pathlib


def save(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=pathlib.Path)
    parser.add_argument('plan', type=pathlib.Path)
    args = parser.parse_args()
    base = args.project.resolve().parent
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    path = base/'shots/shotlist.json'
    register = json.loads(path.read_text(encoding='utf-8'))
    shot = next(s for s in register['storyboardProposals'] if s['id'] == plan['shot'])
    assert shot['frames'] == plan['editFrames']
    assert shot['promptLock'] == plan['promptLock']
    if not any(h['id'] == 'world-below-ship-exterior' for h in shot.get('directionHistory', [])):
        shot.setdefault('directionHistory', []).append({
            'id': 'world-below-ship-exterior', 'description': shot['description'],
            'blocking': copy.deepcopy(shot['blocking']),
            'blockingReview': copy.deepcopy(shot['blockingReview']),
            'startingFrameDraft': copy.deepcopy(shot['startingFrameDraft']),
            'status': 'Superseded by user: ship continuity distracts across the short cut'})
    for test in shot.get('motionTests', []):
        if test['id'] == 'world-below-ref-v01':
            test['status'] = 'Superseded: user requested a planet-only cutaway'
            test['userSelected'] = False
    shot['title'] = 'The big world below / planet-only cutaway'
    shot['description'] = plan['direction']
    shot['generationApproach'] = plan['nextStep']
    shot['status'] = 'Planet-only composition and drift draft for review'
    shot['blocking'] = {'id': shot['id'], 'kind': 'Blender image-plane review',
                        'description': plan['draftMotion'], 'promptLock': shot['promptLock']}
    shot['blockingReview'] = {'id': plan['id'], 'plan': args.plan.name,
                             'blend': plan['output']+'/'+plan['blendFilename'],
                             'status': 'Motion draft in v09 animatic; final orbit not generated'}
    shot['startingFrameDraft'] = {'id': plan['id'], 'image': plan['image'],
        'status': 'AI composition draft awaiting user review', 'userSelected': False,
        'promptFile': args.plan.name, 'changes': 'Ship and Harper removed; established planet, nebula and lighting retained.'}
    test = {'id': plan['id'], 'plan': args.plan.name,
            'motionRef': plan['output']+'/planet-handles.mp4',
            'status': 'Review draft', 'userSelected': False,
            'draftForReview': True, 'reviewNotes': plan['draftMotion'],
            'creditsConsumed': 0}
    existing = next((t for t in shot.get('motionTests', []) if t['id'] == plan['id']), None)
    if existing:
        existing.update(test)
    else:
        shot.setdefault('motionTests', []).append(test)
    save(path, register)
    print('Registered:', shot['id'], plan['id'])


if __name__ == '__main__':
    main()
