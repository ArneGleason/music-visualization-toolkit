"""Insert selected native 1080p shot movies into the full song animatic."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path
from lyric_overlay import write_lyrics


def run(args, cwd=None):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', *args], check=True, cwd=cwd)


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-select_streams', 'v:0', '-show_streams', '-of', 'json', str(path)]))['streams'][0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--version', default='v01', choices=['v01', 'v02', 'v03'],
                        help='Keep the earlier sequence available for comparison')
    args = parser.parse_args()
    base = args.project.resolve().parent
    project = json.loads(args.project.read_text(encoding='utf-8'))
    lyric_style = project.get('production', {}).get('lyricPresentation', {})
    root = base / 'generated/animatic'
    data = json.loads((root / 'animatic-data.json').read_text(encoding='utf-8'))
    register = json.loads((base / 'shots/shotlist.json').read_text(encoding='utf-8'))
    shots = [s for s in register['shots'] if s.get('batch') == 'opening-notes-v01']
    assert shots[0]['startFrame'] == 1
    assert all(a['endFrameExclusive'] == b['startFrame'] for a, b in zip(shots, shots[1:]))
    fps, count = data['fps'], data['frames']
    opening_end = shots[-1]['endFrameExclusive'] - 1
    work = root / 'motion-opening-work'
    work.mkdir(exist_ok=True)
    source = root / 'A-Right-Little-Something-lyric-timing-v03.mp4'
    entries = []
    for shot in shots:
        raw = base / shot['motionRef']
        info = probe(raw)
        # Keep native generated pixels. A few pixels of padding accommodate
        # Kling's slightly narrower source aspect ratio without upscaling.
        assert info['height'] == 1080 and info['width'] <= 1920, info
        lead = shot['handles']['leadInFrames']
        length = shot['frames']
        available = int(float(info['duration']) * fps + 0.01)
        assert available >= lead + length + shot['handles']['leadOutFrames']
        filters = (f'fps={fps},trim=start_frame={lead}:end_frame={lead+length},'
                   'setpts=PTS-STARTPTS,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1')
        movie = work / (shot['id'] + '.mp4')
        run(['-i', str(raw), '-vf', filters, '-frames:v', str(length), '-an',
             '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', str(movie)])
        assert int(probe(movie)['nb_frames']) == length
        entries.append({'shot': shot['id'], 'source': str(raw), 'sourceWidth': info['width'],
            'sourceHeight': info['height'], 'startFrame': shot['startFrame'],
            'frames': length, 'sourceEditStartFrame': lead + 1,
            'availableLeadOutFrames': available - lead - length, 'file': movie.name})
    if lyric_style.get('enabled'):
        run(['-f', 'lavfi', '-i', f'color=c=0x0b111c:s=1920x1080:r={fps}',
             '-frames:v', str(count-opening_end), '-an', '-c:v', 'libx264',
             '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', str(work/'remainder.mp4')])
    else:
        run(['-i', str(source), '-vf', f'trim=start_frame={opening_end},setpts=PTS-STARTPTS,'
             'scale=1920:1080,setsar=1', '-frames:v', str(count-opening_end), '-an',
             '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p',
             str(work / 'remainder.mp4')])
    (work / 'concat.txt').write_text(''.join(f"file '{e['file']}'\n" for e in entries)
        + "file 'remainder.mp4'\n", encoding='utf-8')
    final = root / f'A-Right-Little-Something-opening-motion-{args.version}.mp4'
    pending = work / 'video.mp4'
    run(['-f', 'concat', '-safe', '0', '-i', 'concat.txt', '-c', 'copy',
         '-movflags', '+faststart', str(pending)], cwd=work)
    if lyric_style.get('enabled'):
        write_lyrics(data, lyric_style, work/'lyrics.ass')
        fonts = work/'fonts'
        fonts.mkdir(exist_ok=True)
        shutil.copy2(lyric_style['fontFile'], fonts/Path(lyric_style['fontFile']).name)
        lettering = work/'lettered.mp4'
        run(['-i', str(pending), '-vf', 'ass=lyrics.ass:fontsdir=fonts', '-frames:v', str(count),
             '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '17',
             '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(lettering)], cwd=work)
        pending = lettering
    muxed = final.with_name(final.stem + '.rendering.mp4')
    run(['-i', str(pending), '-i', str(source), '-map', '0:v:0', '-map', '1:a:0',
         '-c', 'copy', '-movflags', '+faststart', str(muxed)])
    result = probe(muxed)
    assert int(result['nb_frames']) == count and result['r_frame_rate'] == f'{fps}/1', result
    assert (result['width'], result['height']) == (1920, 1080)
    hashes = [subprocess.check_output(['ffmpeg', '-v', 'error', '-i', str(path),
        '-map', '0:a:0', '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-'])
        for path in (source, muxed)]
    assert hashes[0] == hashes[1], 'Master audio packets changed'
    muxed.replace(final)
    (root / 'motion-insert-manifest.json').write_text(json.dumps({
        'source': str(source), 'video': str(final), 'fps': fps, 'frames': count,
        'openingEndFrameExclusive': opening_end + 1, 'entries': entries,
        'presentation': 'Full-frame 1080p generated opening; small word-timed bottom lyrics' if lyric_style.get('enabled') else 'Full-frame 1080p generated opening; no lyric or shot labels over picture',
        'audio': 'Original AAC packets copied without retiming',
        'remainder': 'Unplanned dark picture with the same bottom lyric style' if lyric_style.get('enabled') else 'Existing lyric timing picture scaled from 720p to the 1080p review canvas'},
        indent=2) + '\n', encoding='utf-8')
    (root / 'current-media.json').write_text(json.dumps({
        'video': final.name + f'?v={final.stat().st_mtime_ns}'}), encoding='utf-8')
    pointer = base / 'generated/review/current-render.json'
    temp = pointer.with_suffix('.tmp')
    temp.write_text(json.dumps({'video': str(final), 'master_start': 1}), encoding='utf-8')
    temp.replace(pointer)
    (root / 'current-opening.json').write_text(json.dumps({
        'version': args.version, 'fps': fps, 'endFrameExclusive': opening_end + 1,
        'shots': [{'id': s['id'], 'title': s['title'], 'startFrame': s['startFrame'],
                   'frames': s['frames'], 'review': s.get('motionReview', {})} for s in shots]},
        indent=2) + '\n', encoding='utf-8')
    print(final, 'frames', count, 'opening', opening_end, flush=True)


if __name__ == '__main__':
    main()
