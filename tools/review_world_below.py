"""Review the revised exterior blocking alongside the selected interior take."""
import argparse
import copy
import html
import json
import pathlib
import shutil
import subprocess

from lyric_overlay import write_lyrics


def run(args, cwd=None):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *args], cwd=cwd, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=pathlib.Path)
    parser.add_argument('batch', type=pathlib.Path)
    parser.add_argument('--kling-plan', type=pathlib.Path,
                        help='Review generated motion in the same song context')
    args = parser.parse_args()
    base = args.project.resolve().parent
    project = json.loads(args.project.read_text(encoding='utf-8'))
    spec = json.loads(args.batch.read_text(encoding='utf-8'))
    register_path = base / 'shots/shotlist.json'
    register = json.loads(register_path.read_text(encoding='utf-8'))
    shot = next(s for s in register['storyboardProposals'] if s['id'] == 'space-006')
    following = next(s for s in register['storyboardProposals'] if s['id'] == 'space-007')
    kling = (json.loads(args.kling_plan.read_text(encoding='utf-8'))
             if args.kling_plan else None)
    entry = kling['shots'][0] if kling else None
    out = base / (kling['reviewOutput'] if kling else spec['output'])
    out.mkdir(parents=True, exist_ok=True)
    motion = base / spec['output'] / 'space-006-handles.mp4'
    if kling:
        motion = base / kling['output'] / entry['id'] / (entry['id']+'-01-clean.mp4')
        if not motion.exists():
            motion = motion.with_name(entry['id']+'-01.mp4')
        shutil.copy2(base / entry['firstImage'], out / 'starting-frame.png')
        shutil.copy2(base / kling['characterReference']['image'], out / 'harper-reference.png')
    root = base / 'generated/animatic'
    current = json.loads((root / 'current-media.json').read_text())
    source = root / current['video'].split('?', 1)[0]
    data = json.loads((root / 'animatic-data.json').read_text(encoding='utf-8'))
    fps = data['fps']
    first = shot['startFrame'] - fps
    end = following['endFrameExclusive']
    lead = shot['handles']['leadInFrames']
    length = shot['frames']
    captions = copy.deepcopy(data)
    captions['phrases'] = [p for p in captions['phrases']
                           if shot['startFrame'] <= p['startFrame'] < shot['endFrameExclusive']]
    for phrase in captions['phrases']:
        for item in [phrase] + phrase['words']:
            item['startFrame'] -= shot['startFrame'] - 1
            item['endFrameExclusive'] -= shot['startFrame'] - 1
    style = project['production']['lyricPresentation']
    write_lyrics(captions, style, out / 'lyrics.ass')
    fonts = out / 'fonts'
    fonts.mkdir(exist_ok=True)
    shutil.copy2(style['fontFile'], fonts / pathlib.Path(style['fontFile']).name)
    picture_filter = ('pad=1920:1080:(ow-iw)/2:(oh-ih)/2' if kling else 'scale=1920:1080')
    run(['-i', str(motion), '-vf',
         f'trim=start_frame={lead}:end_frame={lead+length},setpts=N/({fps}*TB),'
         + picture_filter + ',setsar=1,ass=lyrics.ass:fontsdir=fonts',
         '-frames:v', str(length), '-an', '-c:v', 'libx264', '-crf', '18',
         '-pix_fmt', 'yuv420p', 'lettered.mp4'], out)
    segments = [('before', first-1, shot['startFrame']-1),
                ('after', shot['endFrameExclusive']-1, end-1)]
    for name, a, b in segments:
        run(['-reinit_filter', '0', '-i', str(source), '-vf',
             f'trim=start_frame={a}:end_frame={b},setpts=N/({fps}*TB),setsar=1',
             '-frames:v', str(b-a), '-an', '-c:v', 'libx264', '-crf', '18',
             str(out / (name + '.mp4'))])
    (out / 'context.txt').write_text(
        "file 'before.mp4'\nfile 'lettered.mp4'\nfile 'after.mp4'\n", encoding='utf-8')
    run(['-f', 'concat', '-safe', '0', '-i', 'context.txt', '-c', 'copy', 'picture.mp4'], out)
    run(['-i', str(out / 'picture.mp4'), '-i', str(source), '-filter_complex',
         f'[1:a]atrim=start={(first-1)/fps}:end={(end-1)/fps},asetpts=PTS-STARTPTS[a]',
         '-map', '0:v:0', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
         '-movflags', '+faststart', str(out / 'world-below-context.mp4')])
    info = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
        '-show_entries', 'stream=nb_read_frames,r_frame_rate,width,height',
        '-of', 'json', str(out / 'world-below-context.mp4')]))['streams'][0]
    assert int(info['nb_read_frames']) == end-first
    assert info['r_frame_rate'] == f'{fps}/1'
    assert (info['width'], info['height']) == (1920, 1080)
    if kling:
        for label, frame in [('edit-in', lead), ('edit-out', lead+length-1)]:
            run(['-i', str(motion), '-vf', f'select=eq(n\\,{frame})',
                 '-frames:v', '1', str(out / ('space-006-'+label+'.png'))])
    esc = html.escape
    page = f'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>World below · revised Blender angle</title>
<style>:root{{color-scheme:dark}}body{{margin:0;background:#10262d;color:#eee2c6;font:16px/1.5 system-ui}}
main{{max-width:1150px;margin:auto;padding:20px}}h1{{font-size:25px}}h2{{font-size:19px}}
a{{color:#9cd9e5}}nav,.controls,.frames{{display:flex;gap:12px;flex-wrap:wrap}}
video,img{{width:100%;background:#07151a}}figure{{margin:0;flex:1;min-width:240px}}
figcaption,.time{{color:#a7c3c8;font-size:13px}}button{{background:#315563;color:white;border:1px solid #789eaa;padding:9px;cursor:pointer}}
article{{background:#19353d;padding:16px;margin:20px 0;border:1px solid #45636a;border-radius:8px}}</style>
<main><h1>World below · different angle, same altitude</h1>
<nav><a href="/">Full animatic & notes</a><a href="../hologram-overlay-v03/">Selected interior display</a>
<a href="world-below-v02.blend" download>Editable Blender scene</a></nav>
<p>“{esc(shot['lyrics'][0])}” · song frames {shot['startFrame']}–{shot['endFrameExclusive']-1} · {length/fps:.2f}s.</p>
<video id="preview" controls preload="auto" poster="space-006-edit-in.png" src="world-below-context.mp4"></video>
<div class="controls"><button data-time="0">Play with preceding shot</button>
<button data-time="1">Play revised exterior</button><button data-time="{1+length/fps}">Play next display shot</button></div>
<p class="time">Context: song {(first-1)/fps:.3f}–{(end-1)/fps:.3f}s · {end-first} frames at {fps}fps.
The new exterior is rough Blender blocking at 1280×720 on a 1080p review canvas; surrounding shots are the selected illustrated animation.</p>
<article><h2>Revised beginning → ending</h2><div class="frames">
<figure><img src="space-006-edit-in.png" alt="Moon-free exterior beginning"><figcaption>Beginning: Harper floats with her hands relaxed.</figcaption></figure>
<figure><img src="space-006-edit-out.png" alt="Moon-free exterior ending"><figcaption>Ending: hands rise toward the upcoming navigation display.</figcaption></figure></div>
<p>{esc(spec['shots'][0]['description'])}</p>
<p>Both moons remain in the shared world and are outside this camera’s frame throughout all 76 source frames, including half-second handles. Ship and planet placement, planet scale and shared sunlight are preserved.</p></article>
<details><summary>Previous camera angle</summary><img src="../space-notes-v01/space-006-edit-in.png" alt="Previous exterior with two moons"></details>
<p>The full animatic remains on its approved v08 selection. This short context preview tests the replacement exterior before ImageGen and clean motion generation.</p></main>
<script>const v=document.getElementById('preview');v.addEventListener('loadedmetadata',()=>{{v.currentTime=1}},{{once:true}});
for(const b of document.querySelectorAll('button[data-time]'))b.onclick=()=>{{v.currentTime=Number(b.dataset.time);v.play()}};
document.addEventListener('keydown',e=>{{if(e.code==='Space'&&!e.repeat&&!/INPUT|TEXTAREA|BUTTON|VIDEO/.test(e.target.tagName)){{e.preventDefault();v.paused?v.play():v.pause()}}}})</script></html>'''
    if kling:
        page = page.replace('World below · revised Blender angle', 'World below · Kling take')
        page = page.replace('World below · different angle, same altitude',
                            'World below · character-referenced Kling take')
        page = page.replace('<a href="world-below-v02.blend" download>Editable Blender scene</a>',
            '<a href="../world-below-v02/">Blender angle</a>')
        page = page.replace('Play revised exterior', 'Play new Kling exterior')
        page = page.replace('The new exterior is rough Blender blocking at 1280×720 on a 1080p review canvas; surrounding shots are the selected illustrated animation.',
            'The new exterior is generated at native 1080p; narrow side padding preserves all pixels. Surrounding shots are the selected illustrated animation.')
        page = page.replace('Beginning: Harper floats with her hands relaxed.',
            'Beginning of the exact song edit.')
        page = page.replace('Ending: hands rise toward the upcoming navigation display.',
            'Last frame before the cut to the interior display.')
        page = page.replace(esc(spec['shots'][0]['description']), esc(kling['reviewChecks']))
        page = page.replace('Both moons remain in the shared world and are outside this camera’s frame throughout all 76 source frames, including half-second handles. Ship and planet placement, planet scale and shared sunlight are preserved.',
            'The generation uses the moon-free starting frame plus the full-body and face references for Harper. No projected display was requested; a Blender light inset can be added later.')
        page = page.replace('This short context preview tests the replacement exterior before ImageGen and clean motion generation.',
            'This context preview tests the generated replacement exterior before selection into the full animatic.')
        page = page.replace('<details><summary>Previous camera angle</summary>',
            '<article><h2>Starting image and Harper reference</h2><div class="frames">'
            '<figure><img src="starting-frame.png" alt="Approved small-Harper starting frame"></figure>'
            '<figure><img src="harper-reference.png" alt="Harper gray-outfit character reference"></figure>'
            '</div></article><details><summary>Previous camera angle</summary>')
        page = page.replace('</main>',
            f'<p><a href="{entry["id"]}-handles.mp4">Full four-second source with song audio</a> · '
            f'<a href="{entry["id"]}-edit.mp4">Exact 52-frame edit</a></p></main>')
    (out / 'index.html').write_text(page, encoding='utf-8')
    shot['description'] = spec['shots'][0]['description']
    if kling:
        test = next(t for t in shot['motionTests'] if t['id'] == entry['id'])
        test.update(status='Generated take awaiting review',
            motionRef=str(motion.relative_to(base)).replace('\\','/'),
            reviewURL='http://127.0.0.1:8768/storyboard/'+out.name+'/',
            contextSource=str(source), fullAnimaticChanged=False)
    else:
        shot['blockingReview'] = {
            'id': 'world-below-v02', 'status': 'Revised Blender draft for review',
            'plan': args.batch.name, 'blend': str(pathlib.PurePosixPath(spec['output']) / spec['blendFilename']),
            'motionRef': str(pathlib.PurePosixPath(spec['output']) / 'space-006-handles.mp4'),
            'reviewURL': 'http://127.0.0.1:8768/storyboard/world-below-v02/',
            'frames': length, 'sourceFrames': shot['handles']['generatedFrames'],
            'moons': 'Unmoved world objects; full silhouettes outside the camera for every source frame',
            'acting': 'Hand-raising anticipation and gentle float before the interior display cut',
            'contextSource': str(source), 'fullAnimaticChanged': False}
    register_path.write_text(json.dumps(register, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print('Context ready:', out / 'index.html', '·', end-first, 'frames')


if __name__ == '__main__':
    main()
