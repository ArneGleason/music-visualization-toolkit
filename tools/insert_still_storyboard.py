"""Place a reviewed still storyboard into the current animatic by exact frames."""
import argparse
import copy
import json
import pathlib
import subprocess

from insert_selected_motion import probe, run


def save(path, data):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=pathlib.Path)
    parser.add_argument('batch', type=pathlib.Path)
    parser.add_argument('--version', required=True)
    args = parser.parse_args()
    base = args.project.resolve().parent
    project = json.loads(args.project.read_text(encoding='utf-8'))
    spec = json.loads(args.batch.read_text(encoding='utf-8'))
    register_path = base/'shots/shotlist.json'
    register = json.loads(register_path.read_text(encoding='utf-8'))
    selected_ids = set(spec['shotIds']) if spec.get('shotIds') else None
    shots = sorted([s for s in register['storyboardProposals'] if s.get('batch') == spec['id']
                    and (selected_ids is None or s['id'] in selected_ids)],
                   key=lambda s:s['startFrame'])
    if selected_ids is not None:
        assert {s['id'] for s in shots} == selected_ids, 'Unknown shot IDs in insert'
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(shots,shots[1:]))
    start, end = shots[0]['startFrame'], shots[-1]['endFrameExclusive']
    root = base/'generated/animatic'
    current = json.loads((root/'current-media.json').read_text(encoding='utf-8'))
    source = base/spec['sourceAnimatic'] if spec.get('sourceAnimatic') else root/current['video'].split('?',1)[0]
    final = root/f'A-Right-Little-Something-selected-motion-{args.version}.mp4'
    if source == final:
        source = pathlib.Path(register['reviewEdits'][args.version]['source'])
    board = base/spec['output']/'timed-still-board.mp4'
    data = json.loads((root/'animatic-data.json').read_text(encoding='utf-8'))
    fps, count = data['fps'], data['frames']
    info = probe(board)
    assert int(info['nb_frames']) == end-start
    assert (info['width'],info['height'],info['r_frame_rate']) == (1920,1080,f'{fps}/1')
    work = root/('selected-stills-'+args.version)
    work.mkdir(exist_ok=True)
    # The reviewed board already contains the exact word-timed bottom lyrics.
    run(['-i',str(board),'-map','0:v:0','-an','-c:v','copy',str(work/'stills.mp4')])
    pieces = ['stills.mp4']
    for name,a,b in [('before',0,start-1),('after',end-1,count)]:
        if b <= a:
            continue
        run(['-reinit_filter','0','-i',str(source),'-vf',
             f'trim=start_frame={a}:end_frame={b},setpts=N/({fps}*TB),setsar=1',
             '-frames:v',str(b-a),'-r',str(fps),'-an','-c:v','libx264',
             '-preset','fast','-crf','18',str(work/(name+'.mp4'))])
        if name == 'before':
            pieces.insert(0, name+'.mp4')
        else:
            pieces.append(name+'.mp4')
    (work/'concat.txt').write_text(''.join(f"file '{name}'\n" for name in pieces),encoding='utf-8')
    run(['-f','concat','-safe','0','-i','concat.txt','-c','copy','picture.mp4'],cwd=work)
    pending = final.with_name(final.stem+'.rendering.mp4')
    run(['-i',str(work/'picture.mp4'),'-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c','copy','-movflags','+faststart',str(pending)])
    result = probe(pending)
    assert int(result['nb_frames']) == count
    assert (result['width'],result['height'],result['r_frame_rate']) == (1920,1080,f'{fps}/1')
    hashes = [subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0',
              '-c','copy','-f','hash','-hash','sha256','-']) for p in (source,pending)]
    assert hashes[0] == hashes[1], 'Original master AAC packets changed'
    pending.replace(final)
    entries = []
    for s in shots:
        if spec.get('useMotion') and s['id'] in spec.get('motionShotIds',[x['id'] for x in shots]):
            selection = s['motionSelection']
            placement = dict(kind='native Kling motion with editorial pan',
                motionRef=selection['motionRef'],userSelected=False,
                startFrame=s['startFrame'],endFrameExclusive=s['endFrameExclusive'],
                frames=s['frames'],animaticVersion=args.version,
                sourceEditStartFrame=selection['sourceEditStartFrame'])
            s['animaticPlacement']=placement
            s['status']='Native motion draft in animatic; user review pending'
            entries.append(dict(shot=s['id'],**placement))
            continue
        selection = copy.deepcopy(s['startingFrameDraft'])
        draft = spec.get('draftForReview', False)
        selection.update(userSelected=not draft,status='Generated draft for animatic review' if draft else 'User directed still selection for animatic')
        if s['id'] == 'space-009':
            selection['status'] = 'User-approved v03 keeper'
        s['startingFrameDraft'] = selection
        s['startingFrameSelection'] = copy.deepcopy(selection)
        s['status'] = 'Draft still in animatic; clean motion not generated' if draft else 'Selected still in animatic; clean motion not generated'
        placement = dict(kind='still with editorial pan' if s.get('cameraMove') else 'static still',image=selection['image'],userSelected=not draft,
                         startFrame=s['startFrame'],endFrameExclusive=s['endFrameExclusive'],
                         frames=s['frames'],animaticVersion=args.version)
        s['animaticPlacement'] = placement
        s['motionReview'] = {'notes':'Selected still storyboard; no clean animation yet. '+s['description']}
        entries.append(dict(shot=s['id'],**placement))
    register.setdefault('reviewEdits',{})[args.version] = dict(
        source=str(source),video=str(final),batch=spec['id'],startFrame=start,
        endFrameExclusive=end,frames=count,fps=fps,entries=entries,
        presentation=spec.get('presentation','Accepted Kling opening and hologram followed by selected still storyboard'),
        audio='Original master AAC packets preserved',type='still storyboard insert')
    register['activeReviewEdit'] = args.version
    save(register_path,register)
    save(root/'current-media.json',{'video':final.name+f'?v={final.stat().st_mtime_ns}'})
    save(base/'generated/review/current-render.json',{'video':str(final),'master_start':1})
    opening = json.loads((root/'current-opening.json').read_text(encoding='utf-8'))
    retained = []
    for prior in opening['shots']:
        prior_end = prior['startFrame']+prior['frames']
        if prior['startFrame'] < start:
            if prior_end > start:
                prior['frames'] = start-prior['startFrame']
            retained.append(prior)
        elif prior['startFrame'] >= end:
            retained.append(prior)
    opening['shots'] = retained
    opening['shots'] += [dict(id=s['id'],title=s['title'],startFrame=s['startFrame'],
                             frames=s['frames'],review=s['motionReview']) for s in shots]
    opening['shots'].sort(key=lambda s:s['startFrame'])
    opening.update(version=args.version,mediaLabel=spec.get('mediaLabel','Kling animation / selected still storyboard'),endFrameExclusive=end)
    save(root/'current-opening.json',opening)
    project['production'].update(animatic=str(final.relative_to(base)).replace('\\','/'),
        continuationNotes=spec.get('continuationNotes', 'V11 contains selected stills at 737–1169: inlet, keeper V03 portrait without hand/window, and one continuous VR coast scene. Accepted Kling planet at 581–632 and hologram composite at 633–736 remain. Clean motion for the three new shots is not generated. Next unplanned scene begins at Do something, frame 1170.'))
    save(args.project,project)
    print('Ready:',final,'·',count,'frames · master audio verified')


if __name__ == '__main__':
    main()
