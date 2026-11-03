"""Render a full-frame 1080p shot edit with a discreet closing credit."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from animatic_media import Artwork


def closing_credit(image, frame, total, fps, font_path, title, copyright_text):
    start = total - round(3 * fps)
    if frame < start:
        return image
    opacity = min(1, (frame - start) / max(1, round(.5 * fps) - 1))
    overlay = Image.new('RGBA', image.size)
    draw = ImageDraw.Draw(overlay)
    for text, size, y in ((title, 28, 976), (copyright_text, 19, 1012)):
        font = ImageFont.truetype(str(font_path), size)
        draw.text((960, y+2), text, font=font, anchor='mt',
                  fill=(0, 0, 0, round(170*opacity)), stroke_width=2)
        draw.text((960, y), text, font=font, anchor='mt',
                  fill=(242, 238, 225, round(235*opacity)))
    return Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--copyright', required=True)
    parser.add_argument('--preview-only', action='store_true')
    args = parser.parse_args()
    base = args.project.resolve().parent
    project = json.loads(args.project.read_text())
    shotlist = base/'shots/shotlist.json'
    score = json.loads(shotlist.read_text())
    shots, fps = score['shots'], score['fps']
    assert score['frameIndexBase'] == 0 and shots[0]['startFrame'] == 0
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(shots,shots[1:]))
    assert all(s['endFrameExclusive']-s['startFrame'] == s['frames'] for s in shots)
    total = shots[-1]['endFrameExclusive']
    art = Artwork(base, shots, fps, full_frame=True)
    font = base/'generated/animatic/assets/BarlowSemiCondensed-SemiBold.ttf'
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    def render(shot, frame):
        return closing_credit(art.at(shot, frame), frame, total, fps,
                              font, args.title, args.copyright)
    render(shots[-1],total-1).save(output.with_suffix('.closing.png'))
    if args.preview_only:
        return
    pending = output.with_name(output.stem+'-pending.mp4')
    command = ['ffmpeg','-y','-hide_banner','-loglevel','error',
               '-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r',str(fps),
               '-i','pipe:0','-i',str(base/project['sources']['audio']),
               '-map','0:v:0','-map','1:a:0','-frames:v',str(total),'-t',str(total/fps),
               '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',
               '-c:a','aac','-b:a','320k','-movflags','+faststart',str(pending)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for shot in shots:
            print(f"Rendering {shot['displayId']} ({shot['startFrame']}/{total})", flush=True)
            for frame in range(shot['startFrame'], shot['endFrameExclusive']):
                proc.stdin.write(render(shot,frame).tobytes())
    except BaseException:
        proc.kill()
        proc.wait()
        raise
    finally:
        proc.stdin.close()
    if proc.wait():
        raise RuntimeError('FFmpeg render failed')
    pending.replace(output)
    manifest = {'width':1920,'height':1080,'fps':fps,'frames':total,
                'shotlistSHA256':hashlib.sha256(shotlist.read_bytes()).hexdigest(),
                'title':args.title,'copyright':args.copyright,
                'creditStartFrame':total-round(3*fps),'shots':shots}
    output.with_suffix('.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(output, flush=True)


if __name__ == '__main__':
    main()
