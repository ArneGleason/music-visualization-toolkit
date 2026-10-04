"""Assemble the native energy field preview at authoritative shot timing."""
import json
from pathlib import Path
import subprocess


def main():
    project = Path('projects/a-right-little-something').resolve()
    dest = project/'generated/storyboard/energy-field-v01'
    shot = next(s for s in json.loads((project/'shots/shotlist.json').read_text())['shots'] if s['id']=='opening-004')
    fps = 24
    lead = shot['handles']['leadInFrames']
    full = lead+shot['frames']+shot['handles']['leadOutFrames']
    master = project/'generated/animatic/A-Right-Little-Something-lyric-timing-v03.mp4'
    assert (dest/f'frames/frame_{full:04}.png').exists(), 'Render not finished'
    checks = []
    for mode, start, count, audio_frame in (
        ('edit', lead, shot['frames'], shot['startFrame']-1),
        ('handles', 0, full, shot['startFrame']-1-lead)):
        output = dest/f'energy-{mode}.mp4'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', str(fps),
            '-i', str(dest/'frames/frame_%04d.png'), '-ss', str(audio_frame/fps), '-i', str(master),
            '-map', '0:v:0', '-map', '1:a:0', '-vf',
            f'trim=start_frame={start}:end_frame={start+count},setpts=PTS-STARTPTS,setsar=1',
            '-t', str(count/fps), '-c:v', 'libx264', '-crf', '18', '-preset', 'fast',
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-movflags', '+faststart', str(output)], check=True)
        check = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate,nb_frames', '-of', 'json', str(output)]))['streams'][0]
        assert check == {'width': 1920, 'height': 1080, 'r_frame_rate': '24/1', 'nb_frames': str(count)}, check
        checks.append({'mode': mode, **check})
    (dest/'review-checks.json').write_text(json.dumps(checks, indent=2)+'\n')
    (dest/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Native field energy test</title>
<style>body{background:#11151b;color:#edf0f4;font:16px system-ui;max-width:1500px;margin:auto;padding:24px}a{color:#a7dafa}h1{font-size:26px}h2{font-size:20px}p,figcaption{line-height:1.5}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}figure{margin:0}img,video{width:100%;display:block;aspect-ratio:16/9;object-fit:contain;background:#000}figcaption{color:#bdc7d5;margin-top:10px}section{border-top:1px solid #43505e;margin-top:24px;padding-top:16px}@media(max-width:850px){.grid{grid-template-columns:1fr}}</style>
<h1>Dots joined by lines · native energy field</h1><p><a href="/">Animatic and listening notes</a> · <a href="../depth-field-experiments-v01/">Previous comparisons</a></p>
<p>Actual Blender motion graphics: fixed junctions and geodesic connections, with traveling waves of brightness. Lines range from almost invisible to gently luminous; the dots remain steady. Only the field display rotates, six degrees over the full 5.083-second render. The camera, ship and distant background stay fixed.</p>
<div class="grid"><figure><video controls playsinline preload="metadata" src="energy-edit.mp4"></video><figcaption>Native Blender field · shot 4 timing · 98 frames, 1080p at 24 fps, matching master audio. Eight-sample preview; fine edges may have render noise.</figcaption></figure><figure><img src="energy-edit-in.png" alt="Thin cyan geodesic field with stable junction dots around the native ship"><figcaption>Dots and lines share the same 3D coordinates. Brightness changes, rather than geometry appearing, breaking or reconnecting.</figcaption></figure></div>
<p><a href="energy-handles.mp4">Full render with half-second lead-in and lead-out</a> · <a href="energy-field-v01.blend" download>Editable Blender scene</a></p>
<section><h2>Earlier Kling result you liked</h2><video controls playsinline preload="metadata" src="../depth-field-experiments-v01/depth-lines-edit.mp4"></video><p>This is Kling-generated motion, with no Blender field animation. It is shot 2, so compare the field behavior rather than the composition or acting. The native test is a separate look experiment and does not replace the animatic.</p></section></html>''', encoding='utf-8')
    print(dest/'index.html')


if __name__ == '__main__':
    main()
