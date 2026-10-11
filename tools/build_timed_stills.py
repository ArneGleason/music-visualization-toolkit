"""Render a canonical still-shot batch with eased camera moves and frame fades."""
import argparse
import copy
import json
from pathlib import Path
import shutil

from build_chorus_revision import encode, load, probe, run, save
from lyric_overlay import write_lyrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('batch', type=Path)
    parser.add_argument('--reuse-prepared', action='store_true',
                        help='Reuse copied, unchanged shot chunks after checking their frame counts.')
    args = parser.parse_args()
    base = args.project.resolve().parent
    project, spec = load(args.project), load(args.batch)
    register = load(base/'shots/shotlist.json')
    shots = sorted((s for s in register['storyboardProposals']
                    if s.get('batch') == spec['id']), key=lambda s:s['startFrame'])
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(shots,shots[1:]))
    data = load(base/'generated/animatic/animatic-data.json')
    fps = data['fps']
    start, end = shots[0]['startFrame'], shots[-1]['endFrameExclusive']
    out = base/spec['output']
    out.mkdir(parents=True, exist_ok=True)
    width = spec.get('fadeFrames', 4)
    assert width % 2 == 0
    files, counts = [], []
    for i, shot in enumerate(shots):
        head = width//2 if i else 0
        count = shot['frames'] + head + (width//2 if i < len(shots)-1 else 0)
        move = spec.get('cameraMoves',{}).get(shot['id'],shot['cameraMove'])
        t = f'min(1,max(0,on/{count-1}))'
        ease = f'(({t})*({t})*(3-2*({t})))'
        def expr(values):
            return f'{values[0]}+({values[1]}-{values[0]})*{ease}'
        z,x,y = [expr(move[k]) for k in ('zoom','panX','panY')]
        vf = (f"scale=3840:2160,setsar=1,zoompan=z='{z}':"
              f"x='(iw-iw/zoom)*({x})':y='(ih-ih/zoom)*({y})':d=1:s=1920x1080:fps={fps}")
        target = out/(shot['id']+'.mp4')
        if not args.reuse_prepared or not target.exists():
            if spec.get('useMotion') and shot['id'] in spec.get('motionShotIds',[s['id'] for s in shots]):
                selection = shot['motionSelection']
                source = base/selection['motionRef']
                lead = selection['sourceEditStartFrame']-1-head
                assert lead >= 0 and int(probe(source)['nb_frames']) >= lead+count
                inputs = ['-i',str(source)]
                vf = f'fps={fps},trim=start_frame={lead}:end_frame={lead+count},setpts=N/({fps}*TB),pad=1920:1080:(ow-iw)/2:(oh-ih)/2,'+vf
            else:
                inputs = ['-loop','1','-framerate',str(fps),'-i',str(base/shot['startingFrameDraft']['image'])]
            encode([*inputs,'-vf',vf],count,target)
        assert int(probe(target)['nb_frames']) == count
        files.append(target)
        counts.append(count)
    inputs, chain = [], []
    for i, file in enumerate(files):
        inputs += ['-i',str(file)]
        chain.append(f'[{i}:v]settb=1/{fps},setpts=N,fps={fps},format=yuv444p[v{i}]')
    total, previous = counts[0], 'v0'
    for i in range(1,len(files)):
        name = f'x{i}'
        chain.append(f'[{previous}][v{i}]xfade=transition=fade:duration={width/fps}:offset={(total-width)/fps}[{name}]')
        total += counts[i]-width
        previous = name
    assert total == end-start
    encode([*inputs,'-filter_complex_threads','2','-filter_complex',';'.join(chain),
            '-map',f'[{previous}]'],total,out/'picture.mp4')
    # Entry dissolve uses a clean outgoing plate frame, so old burned lyrics
    # cannot ghost into the flashback. The incoming cue stays at its grid frame.
    picture = out/'picture.mp4'
    if spec.get('entryPlate'):
        count = spec['entryFadeFrames']
        run(['-i',str(base/spec['entryPlate']),'-vf',
             f"select=eq(n\\,{spec['entryPlateFrame']-1}),setpts=N/({fps}*TB)",
             '-frames:v','1',str(out/'entry.png')])
        graph = (f'[0:v]format=gbrp[a];[1:v]format=gbrp[b];'
                 f"[a][b]blend=all_expr='A*min(1,N/{count})+B*(1-min(1,N/{count}))':shortest=1,format=yuv420p[v]")
        encode(['-i',str(picture),'-loop','1','-framerate',str(fps),'-i',str(out/'entry.png'),
                '-filter_complex',graph,'-map','[v]'],total,out/'entry-picture.mp4')
        picture = out/'entry-picture.mp4'
    captions = copy.deepcopy(data)
    captions['phrases'] = [p for p in captions['phrases'] if start <= p['startFrame'] < end]
    for phrase in captions['phrases']:
        for item in [phrase]+phrase['words']:
            item['startFrame'] -= start-1
            item['endFrameExclusive'] -= start-1
    style = project['production']['lyricPresentation']
    write_lyrics(captions,style,out/'lyrics.ass')
    (out/'fonts').mkdir(exist_ok=True)
    shutil.copy2(style['fontFile'],out/'fonts'/Path(style['fontFile']).name)
    source = base/spec['sourceAnimatic']
    run(['-i',str(picture),'-i',str(source),'-filter_complex',
         f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={(start-1)/fps}:end={(end-1)/fps},asetpts=PTS-STARTPTS[a]',
         '-map','[v]','-map','[a]','-frames:v',str(total),'-c:v','libx264','-preset','fast',
         '-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',
         'timed-still-board.mp4'],out)
    assert int(probe(out/'timed-still-board.mp4')['nb_frames']) == total
    save(out/'timing-check.json',dict(startFrame=start,endFrameExclusive=end,frames=total,
         fps=fps,fadeFrames=width,entryFadeFrames=spec.get('entryFadeFrames',0),
         shots=[dict(id=s['id'],startFrame=s['startFrame'],frames=s['frames'],
                     sourceKind='native motion with editorial pan' if spec.get('useMotion') and s['id'] in spec.get('motionShotIds',[x['id'] for x in shots]) else 'generated still with editorial pan') for s in shots]))
    print('Timed stills ready:',total,'frames')


if __name__ == '__main__':
    main()
