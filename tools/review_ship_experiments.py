"""Build an isolated, frame-counted review of depth and native-ship experiments."""
import html
import json
import subprocess
from pathlib import Path


PROJECT = Path('projects/a-right-little-something').resolve()
DEST = PROJECT / 'generated/storyboard/depth-field-experiments-v01'
MASTER = PROJECT / 'generated/animatic/A-Right-Little-Something-lyric-timing-v03.mp4'


def clip(source, name, shot, sequence=False):
    lead = shot['handles']['leadInFrames']
    count = shot['frames']
    output = DEST / f'{name}-edit.mp4'
    inputs = ['-framerate', '24'] if sequence else []
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *inputs, '-i', str(source),
        '-ss', str((shot['startFrame']-1)/24), '-i', str(MASTER),
        '-map', '0:v:0', '-map', '1:a:0', '-vf',
        f'fps=24,trim=start_frame={lead}:end_frame={lead+count},setpts=PTS-STARTPTS,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1',
        '-t', str(count/24), '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-movflags', '+faststart', str(output)], check=True)
    stream = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-select_streams', 'v:0', '-show_entries', 'stream=width,height,nb_frames,r_frame_rate',
        '-of', 'json', str(output)]))['streams'][0]
    assert stream['nb_frames'] == str(count), stream
    assert (stream['width'], stream['height']) == (1920, 1080), stream
    return stream


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    shots = {s['id']: s for s in json.loads((PROJECT/'shots/shotlist.json').read_text())['shots']}
    plan = json.loads((PROJECT/'kling-depth-field-experiments.json').read_text())
    entries = [('baseline', PROJECT/'generated/kling-opening/completion-v01/opening-002/opening-002-01-clean.mp4',
                'Current shot 2', 'Existing moving-camera version for comparison.')]
    descriptions = {
        'depth-lines': ('Locked camera · lines', 'Distant background stays more stable. This tests a locked camera; it does not establish behavior during an orbit.'),
        'depth-dots': ('Locked camera · dots', 'Dots are subtle and can read as stars. Harper turns away unexpectedly, so this is not a clean comparison of display styles.'),
        'depth-dots-rotating': ('Requested rotating dots', 'Kling restores prominent hexagonal lines. The requested five-degree display-only rotation is not reliably reproduced.')}
    for item in plan['shots']:
        name = item['id']
        entries.append((name, PROJECT/plan['output']/name/f'{name}-01-clean.mp4', *descriptions[name]))
    cards = []
    manifest = []
    for name, source, title, note in entries:
        stream = clip(source, name, shots['opening-002'])
        manifest.append({'id': name, 'source': str(source), 'video': stream, 'retimed': False})
        cards.append(f'<figure id="{name}"><h2>{html.escape(title)}</h2><video controls playsinline preload="metadata" src="{name}-edit.mp4"></video><figcaption>{html.escape(note)}</figcaption></figure>')
    hybrid = PROJECT/'generated/storyboard/hybrid-ship-v01'
    native = ''
    if (hybrid/'frames/frame_0122.png').exists():
        stream = clip(hybrid/'frames/frame_%04d.png', 'hybrid', shots['opening-004'], sequence=True)
        manifest.append({'id': 'hybrid', 'video': stream, 'sourceShot': 'opening-004', 'retimed': False})
        shot = shots['opening-004']
        handle_start = (shot['startFrame']-1-shot['handles']['leadInFrames'])/24
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '24',
            '-i', str(hybrid/'frames/frame_%04d.png'), '-ss', str(handle_start), '-i', str(MASTER),
            '-map', '0:v:0', '-map', '1:a:0', '-frames:v', '122', '-t', str(122/24),
            '-c:v', 'libx264', '-crf', '18', '-preset', 'fast', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-movflags', '+faststart', str(DEST/'hybrid-handles.mp4')], check=True)
        native = '<video controls playsinline preload="metadata" src="hybrid-edit.mp4"></video><p><a href="hybrid-handles.mp4">Full render with half-second handles</a></p>'
    (DEST/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    (DEST/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ship and depth experiments</title><style>
body{background:#11151b;color:#edf0f4;font:16px system-ui;max-width:1500px;margin:auto;padding:24px}a{color:#a7dafa}h1{font-size:26px}h2{font-size:20px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}figure{margin:0}img,video{display:block;width:100%;aspect-ratio:16/9;object-fit:contain;background:#000}p,figcaption{line-height:1.5}figcaption{color:#bdc7d5;margin-top:10px}section{border-top:1px solid #43505e;margin-top:28px;padding-top:18px}@media(max-width:850px){.grid{grid-template-columns:1fr}}</style>
<h1>Ship and distant-world experiments</h1><p><a href="/">Full animatic and listening notes</a> · <a href="../opening-v02/">Current storyboard</a></p>
<p>Separate tests; the current animatic is unchanged. Every motion preview is 1920 × 1080 at 24 fps, with the exact shot frame count and matching master audio. No time stretching.</p>
<section id="hybrid"><h2>Native Blender ship · shot 4</h2><p>The continuous ring, platforms, engine and field are real 3D geometry. Planet, moons and stars share a distant ImageGen plate. Harper is a transparent illustrated card with a small float, not an articulated character. This restrained camera move tests the hybrid approach; large orbits need another actor solution and a broader environment.</p>
<div class="grid"><figure><img src="../hybrid-ship-v01/hybrid-edit-in.png"><figcaption>Native ship look prototype. The metal finish still needs refinement to match the approved illustration.</figcaption></figure><figure>'''+native+'''<figcaption>Exact shot 4 edit · 98 frames. Low-sample preview render; geometry and timing are native.</figcaption></figure></div>
<p><a href="../hybrid-ship-v01/hybrid-ship-v01.blend" download>Download editable Blender experiment</a></p></section>
<section><h2>Kling depth and display comparisons · shot 2</h2><p>Three seven-second generations, 168 credits total. The variants share a single starting frame approach and fixed-camera depth instructions. These edits use 136 frames after a 12-frame lead-in. The native ship test above required no additional Kling generation.</p><div class="grid">'''+''.join(cards)+'''</div></section></html>''', encoding='utf-8')
    print(DEST/'index.html')


if __name__ == '__main__':
    main()
