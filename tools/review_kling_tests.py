"""Make frame-counted, master-audio reviews of collected Kling opening tests."""
import argparse
import html
import json
import shutil
import subprocess
from pathlib import Path


def run(args):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *args], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    project = args.plan.resolve().parent
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    shots = {s['id']: s for s in json.loads(
        (project / 'shots/shotlist.json').read_text(encoding='utf-8'))['shots']}
    fps = plan['fps']
    dest = project / plan.get('reviewOutput','generated/storyboard/kling-opening-v01')
    dest.mkdir(parents=True, exist_ok=True)
    master = project / 'generated/animatic/A-Right-Little-Something-lyric-timing-v03.mp4'
    cards = []
    manifest = []
    for entry in plan['shots']:
        sid = entry['id']
        shot = shots.get(sid, {'title': entry.get('title',sid),
            'startFrame':entry.get('startFrame'), 'frames':entry.get('editFrames'),
            'handles':{'leadInFrames':entry.get('leadInFrames',12),
                       'leadOutFrames':entry.get('leadOutFrames',12)}})
        raw = project / plan['output'] / sid / f'{sid}-01.mp4'
        clean = raw.with_name(f'{sid}-01-clean.mp4')
        if clean.exists():
            raw = clean
        if not raw.exists():
            continue
        probe = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
            '-show_streams', '-show_format', '-of', 'json', str(raw)]))
        lead = shot['handles']['leadInFrames']
        length = shot['frames']
        full_frames = entry['duration'] * fps
        assert full_frames >= lead + length + shot['handles']['leadOutFrames']
        for mode, start, count, song_frame in (
            ('edit', lead, length, shot['startFrame'] - 1),
            ('handles', 0, full_frames, shot['startFrame'] - 1 - lead)):
            movie = dest / f'{sid}-{mode}.mp4'
            filters = (f'fps={fps},trim=start_frame={start}:end_frame={start+count},'
                       'setpts=PTS-STARTPTS,setsar=1')
            run(['-i', str(raw), '-ss', str(song_frame / fps), '-i', str(master),
                 '-map', '0:v:0', '-map', '1:a:0', '-vf', filters,
                 '-t', str(count / fps), '-c:v', 'libx264', '-preset', 'fast',
                 '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
                 '-movflags', '+faststart', str(movie)])
            check = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
                '-select_streams', 'v:0', '-show_entries', 'stream=nb_frames,r_frame_rate',
                '-of', 'json', str(movie)]))['streams'][0]
            assert int(check['nb_frames']) == count, (sid, mode, check)
        shutil.copy2(project / entry['firstImage'], dest / f'{sid}-reference.png')
        manifest.append({'id': sid, 'source': str(raw), 'sourceProbe': probe,
            'fps': fps, 'editFrames': length, 'leadInFrames': lead,
            'availableLeadOutFrames': full_frames-lead-length,
            'songStartFrame': shot['startFrame'], 'retimed': False})
        cards.append(f'''<section id="{sid}"><h2>{sid} · {html.escape(shot['title'])}</h2>
<div class="compare"><figure><img src="{sid}-reference.png"><figcaption>Image Gen starting reference</figcaption></figure>
<figure><video controls preload="metadata" playsinline src="{sid}-edit.mp4"></video><figcaption>Kling · exact song edit · {length} frames at {fps} fps</figcaption></figure></div>
<p><a href="{sid}-handles.mp4">Play all {entry['duration']} seconds with handles and song audio</a> · <a href="{sid}-edit.mp4">Open exact edit</a></p>
<p>{html.escape(entry.get('reviewNotes',plan.get('reviewChecks','Check the field lines, uninterrupted metal ring, stable limbs and moons. For the pullback, watch the intermediate geometry as well as the destination.')))}</p></section>''')
    (dest / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    for comparison in plan.get('comparisons',[]):
        cards.append(f'''<section><h2>{html.escape(comparison['title'])}</h2>
<video controls preload="metadata" playsinline src="{html.escape(comparison['src'],quote=True)}"></video>
<p>{html.escape(comparison.get('notes',''))}</p></section>''')
    page=('''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Opening · Kling motion tests</title><style>
body{background:#11151b;color:#ecedf0;font:16px system-ui;max-width:1500px;margin:auto;padding:24px}
a{color:#a7dafa}h1{font-size:26px}h2{font-size:20px}section{padding:20px 0;border-top:1px solid #3b4653}
.compare{display:grid;grid-template-columns:1fr 1fr;gap:16px}figure{margin:0}img,video{display:block;width:100%;aspect-ratio:16/9;object-fit:contain;background:#000}
figcaption{color:#b3becb;margin-top:8px}p{line-height:1.5}@media(max-width:900px){.compare{grid-template-columns:1fr}}
</style><h1>Opening scene · Kling motion tests</h1>
<p>Two 1080p five-second generations, 80 credits total. The videos below use the existing master at each shot's exact frame positions. No time stretching. These are tests; the approved storyboard animatic is still available.</p>
<p><a href="/">Listening notes / full animatic</a> · <a href="../opening-v02/">Opening storyboard</a></p>'''
        + '\n'.join(cards))
    if plan.get('reviewTitle'):
        page=page.replace('Opening scene · Kling motion tests',html.escape(plan['reviewTitle']))
        page=page.replace('Two 1080p five-second generations, 80 credits total.',html.escape(plan['reviewSummary']))
    (dest/'index.html').write_text(page,encoding='utf-8')
    print(dest / 'index.html')


if __name__ == '__main__':
    main()
