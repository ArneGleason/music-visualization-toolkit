"""Build a clearly labelled, frame-timed still storyboard with master audio."""
import argparse
import copy
import html
import json
import pathlib
import shutil
import subprocess

from lyric_overlay import write_lyrics


def run(args, cwd):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *args], cwd=cwd, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=pathlib.Path)
    parser.add_argument('batch', type=pathlib.Path)
    args = parser.parse_args()
    base = args.project.resolve().parent
    project = json.loads(args.project.read_text(encoding='utf-8'))
    spec = json.loads(args.batch.read_text(encoding='utf-8'))
    register = json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))
    shots = sorted([s for s in register['storyboardProposals'] if s['batch'] == spec['id']],
                   key=lambda s:s['startFrame'])
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(shots, shots[1:]))
    out = base/spec['output']
    out.mkdir(parents=True, exist_ok=True)
    root = base/'generated/animatic'
    current = json.loads((root/'current-media.json').read_text(encoding='utf-8'))
    source = root/current['video'].split('?', 1)[0]
    data = json.loads((root/'animatic-data.json').read_text(encoding='utf-8'))
    fps = data['fps']
    start, end = shots[0]['startFrame'], shots[-1]['endFrameExclusive']
    entries = []
    cards = []
    controls = []
    esc = html.escape
    for s in shots:
        image = base/s['startingFrameDraft']['image']
        name = s['id']+'.mp4'
        run(['-loop','1','-framerate',str(fps),'-i',str(image),
             '-vf','scale=1920:1080,setsar=1','-frames:v',str(s['frames']),
             '-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',name], out)
        entries.append(name)
        time = (s['startFrame']-start)/fps
        controls.append(f'<button data-time="{time}">{(s["startFrame"]-1)/fps:.2f}s · {esc(s["id"])}</button>')
        motion = s['generationApproach']
        reference = s['startingFrameDraft']
        label = reference.get('label', image.name)
        alias = reference.get('sourceAlias')
        reference_text = label + (f' · original source {alias}' if alias else '')
        previous_image = reference.get('previousImage')
        previous_link = (f'<p class="muted">Previous reference: <a href="{esc(pathlib.PurePosixPath(previous_image).name, quote=True)}">'
                         f'{esc(pathlib.PurePosixPath(previous_image).name)}</a></p>'
                         if previous_image else '')
        cards.append(f'''<article id="{s['id']}"><h2>{esc(s['id'])} · {esc(s['title'])}</h2>
<p class="muted">Song frames {s['startFrame']}–{s['endFrameExclusive']-1} · {s['frames']/fps:.2f}s · {s['handles']['leadInFrames']/fps:g}s lead-in / {s['handles']['leadOutFrames']/fps:g}s lead-out handles</p>
<img src="{image.name}" alt="{esc(s['title'], quote=True)}">
<p class="muted">Still: {esc(reference_text)} · <a href="{image.name}">{esc(image.name)}</a></p>
{previous_link}
<p><strong>{esc(' / '.join(s['lyrics']))}</strong></p><p>{esc(s['description'])}</p>
<details><summary>Planned motion and generation</summary><p>{esc(motion)}</p></details></article>''')
    (out/'concat.txt').write_text(''.join(f"file '{n}'\n" for n in entries), encoding='utf-8')
    run(['-f','concat','-safe','0','-i','concat.txt','-c','copy','picture.mp4'], out)
    captions = copy.deepcopy(data)
    captions['phrases'] = [p for p in captions['phrases'] if start <= p['startFrame'] < end]
    for phrase in captions['phrases']:
        for item in [phrase]+phrase['words']:
            item['startFrame'] -= start-1
            item['endFrameExclusive'] -= start-1
    style = project['production']['lyricPresentation']
    write_lyrics(captions, style, out/'lyrics.ass')
    fonts = out/'fonts'
    fonts.mkdir(exist_ok=True)
    shutil.copy2(style['fontFile'], fonts/pathlib.Path(style['fontFile']).name)
    run(['-i','picture.mp4','-i',str(source),'-filter_complex',
         f'[0:v]ass=lyrics.ass:fontsdir=fonts[v];[1:a]atrim=start={(start-1)/fps}:end={(end-1)/fps},asetpts=PTS-STARTPTS[a]',
         '-map','[v]','-map','[a]','-frames:v',str(end-start),'-c:v','libx264',
         '-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
         '-movflags','+faststart','timed-still-board.mp4'], out)
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
        '-show_entries','stream=nb_frames,width,height,r_frame_rate','-of','json',
        str(out/'timed-still-board.mp4')]))['streams'][0]
    assert int(probe['nb_frames']) == end-start and probe['r_frame_rate'] == f'{fps}/1'
    assert (probe['width'],probe['height']) == (1920,1080)
    page = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Window to alien coast · still storyboard</title>
<style>:root{color-scheme:dark}body{margin:0;background:#11282d;color:#f1dfb6;font:16px/1.5 system-ui}
main{max-width:1100px;margin:auto;padding:20px}h1{font-size:25px}h2{font-size:20px}a{color:#a7dafa}
video,img{display:block;width:100%;background:#07151a}.controls{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
button{background:#315563;border:1px solid #789eaa;color:white;padding:9px;cursor:pointer}
article{padding:16px;background:#193239;border:1px solid #45636a;border-radius:7px;margin:22px 0}
.muted{color:#a0b6b3}.label{border-left:4px solid #ff754d;padding:10px;background:#193239}</style>
<main><h1>Window → alien coast</h1><nav><a href="/">Full animatic & notes</a> · <a href="../kling-planet-cutaway-v01/">Accepted planet take</a></nav>
<p class="label"><strong>STILL STORYBOARD · ImageGen composition drafts</strong><br>Three still images held to the lyric timing. This preview contains no Kling animation or simulated tide movement. The full animatic remains on accepted v10.</p>
'''+f'<p>Song {(start-1)/fps:.2f}–{(end-1)/fps:.2f}s · {end-start} frames · {fps} fps. Small bottom lyrics retain the performed wording.</p>\n'+'''
<video id="preview" controls preload="metadata" src="timed-still-board.mp4"></video><div class="controls">
'''+''.join(controls)+'''</div><p>Sequence: interior map → narrow ship-free inlet → intimate ship portrait → one continuous projected shore experience. The inlet is an AI-proposed confinement metaphor. Coast flora/fauna and projection scale are design drafts for review.</p>
'''+''.join(cards)+'''<p>“Stretch your arms wide” opens her gesture. “And change the tide” brings broad shallow water fronts across the long beach. “How much can you do with it all?” holds the same scene as she experiences it. No new cut or scale jump between these beats. The next scene, “Do something,” remains unplanned.</p></main>
<script>const v=document.querySelector('#preview');for(const b of document.querySelectorAll('button[data-time]'))b.onclick=()=>{v.currentTime=Number(b.dataset.time);v.play()};
document.addEventListener('keydown',e=>{if(e.code==='Space'&&!e.repeat&&!e.target.isContentEditable&&!/INPUT|TEXTAREA|BUTTON|VIDEO/.test(e.target.tagName)){e.preventDefault();v.paused?v.play():v.pause()}})</script></html>'''
    if spec.get('reviewIntro'):
        title = esc(spec.get('title', 'Still storyboard'))
        page = page.replace('Window to alien coast · still storyboard', title)
        page = page.replace('Window → alien coast', title)
        intro_start = page.index('<p class="label">')
        intro_end = page.index('</p>', intro_start)+4
        page = page[:intro_start] + '<p class="label"><strong>STILL STORYBOARD · ImageGen composition drafts</strong><br>' + esc(spec['reviewIntro']) + '</p>' + page[intro_end:]
        sequence_start = page.index('<p>Sequence:')
        sequence_end = page.index('</p>', sequence_start)+4
        page = page[:sequence_start] + page[sequence_end:]
        footer_start = page.index('<p>“Stretch your arms wide”')
        footer_end = page.index('</p>', footer_start)+4
        page = page[:footer_start] + page[footer_end:]
    if spec.get('assembledStills'):
        page = page.replace('The full animatic remains on accepted v10.',
            f'These selected stills are now placed in full animatic {html.escape(spec["animaticVersion"])}; clean motion is not generated yet.')
    (out/'index.html').write_text(page, encoding='utf-8')
    (out/'manifest.json').write_text(json.dumps({'type':'static still storyboard','sourceAudio':str(source),
        'startFrame':start,'endFrameExclusive':end,'fps':fps,'frames':end-start,
        'shots':[{k:s[k] for k in ('id','startFrame','endFrameExclusive','frames')} for s in shots],
        'fullAnimaticChanged':False},indent=2)+'\n',encoding='utf-8')
    print('Timed still board:', out/'index.html')


if __name__ == '__main__':
    main()
