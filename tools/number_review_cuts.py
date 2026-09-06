"""Add frame-exact numbered badges to an existing rough, preserving its audio."""
import argparse
import json
import pathlib
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='out/rough_v04_sync_noflash_720p.mp4')
    parser.add_argument('--out', default='out/rough_v04_numbered_720p.mp4')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    source, target = ROOT/args.input, ROOT/args.out
    if target.exists() and not args.force:
        raise FileExistsError(target)
    data = json.loads((ROOT/'shots/shotlist.json').read_text())
    shots, fps = data['shots'], data['fps']
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error',
        '-select_streams','v:0','-show_entries','stream=nb_frames,avg_frame_rate,height,start_time',
        '-of','json',str(source)]))['streams'][0]
    from fractions import Fraction
    total = round(shots[-1]['end_sec']*fps)
    assert int(probe['nb_frames']) == total and float(Fraction(probe['avg_frame_rate'])) == fps
    size = round(44*int(probe['height'])/720)
    margin = round(18*int(probe['height'])/720)
    scale = 4
    font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',round(size*.49*scale))
    origin_us = round(float(probe.get('start_time',0))*1000000)
    command = ['ffmpeg','-y' if args.force else '-n','-v','error','-i',str(source),'-f','rawvideo',
        '-pixel_format','rgba','-video_size',f'{size}x{size}','-framerate',str(fps),
        '-i','pipe:0','-filter_complex',
        f'[1:v]settb=AVTB,setpts=PTS+{origin_us}[badge];'
        f'[0:v][badge]overlay=x=main_w-overlay_w-{margin}:y={margin}:eof_action=repeat[v]',
        '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','fast','-crf','17',
        '-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(total),'-movflags','+faststart',str(target)]
    rows, previous = [], 0
    process = subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for number, shot in enumerate(shots,1):
            start,end = round(shot['start_sec']*fps),round(shot['end_sec']*fps)
            assert start == previous and end > start
            badge = Image.new('RGBA',(size*scale,size*scale))
            draw = ImageDraw.Draw(badge)
            draw.ellipse((2,2,size*scale-3,size*scale-3),fill=(0,0,0,235))
            draw.text((size*scale/2,size*scale/2),str(number),font=font,
                      fill='white',anchor='mm')
            pixels = badge.resize((size,size),Image.Resampling.LANCZOS).tobytes()
            for _ in range(end-start):
                process.stdin.write(pixels)
            time = f'{start//(fps*60):02d}:{(start//fps)%60:02d}.{round(start%fps/fps*1000):03d}'
            rows.append(f"| {number} | {shot['id']} | {time} | {start}:{end} | {shot['setup']} |")
            previous=end
    finally:
        process.stdin.close()
    if process.wait():
        raise RuntimeError('Numbered preview encode failed')
    actual = json.loads(subprocess.check_output(['ffprobe','-v','error',
        '-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(target)]))
    assert int(actual['streams'][0]['nb_frames']) == total
    target.with_suffix('.md').write_text('# Numbered rough review\n\n'
        f'Movie: `{target.name}`. Numbers are specific to this version; use this lookup\n'
        'when translating review notes to stable project shot IDs. 24 fps, end-exclusive ranges.\n\n'
        '| Cut number | Shot ID | Starts at | Song frames | Setup |\n'
        '| --- | --- | --- | --- | --- |\n'+'\n'.join(rows)+'\n',encoding='utf-8')
    print(f'Wrote {target}: {len(shots)} numbered cuts; original audio copied.')


if __name__=='__main__':
    main()
