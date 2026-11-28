"""Render scene-level story cards with the full master and a small lyric strip."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from timeline import MusicalGrid


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clock(seconds):
    value = int(seconds)
    return f'{value // 60}:{value % 60:02d}'


def stamp(frame, fps):
    value = frame * 100 // fps
    minutes, value = divmod(value, 6000)
    seconds, fraction = divmod(value, 100)
    return f'{minutes // 60}:{minutes % 60:02d}:{seconds:02d}.{fraction:02d}'


def plain(value):
    return value.replace('\\', '/').replace('{', '(').replace('}', ')')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', type=int, default=1)
    parser.add_argument('--register', action='store_true', help='Install these proposed scene markers in timeline.json')
    args = parser.parse_args()
    version = f'v{args.version:03d}'
    source = BASE / f'production/story-timing-{version}/scenes.json'
    spec = json.loads(source.read_text())
    project = json.loads((BASE / 'project.json').read_text())
    grid = MusicalGrid(json.loads((BASE / project['timing']['beatmap']).read_text()))
    timeline_path = BASE / project['timeline']
    timeline = json.loads(timeline_path.read_text())
    fps = project['render']['fps']
    total = math.ceil(grid.duration * fps)
    out = BASE / f'generated/wip/previews/story-timing/{version}'
    out.mkdir(parents=True, exist_ok=True)
    movie = out / f'Secret-Room-story-timing-{version}.mp4'
    if movie.exists():
        parser.error('Preview already exists; use a new version or remove only a failed render.')
    edges = [round(grid.sec(scene['start']) * fps) for scene in spec['scenes']] + [total]
    assert edges[0] == 0 and edges == sorted(set(edges))
    assert all((b-a)/fps >= 5 for a,b in zip(edges, edges[1:]))
    scenes = []
    for i, (scene, start, end) in enumerate(zip(spec['scenes'], edges, edges[1:])):
        end_position = spec['scenes'][i+1]['start'] if i+1 < len(spec['scenes']) else grid.position(grid.duration).text()
        scenes.append({**scene, 'end': end_position, 'startFrame': start,
                       'endFrameExclusive': end, 'frames': end-start,
                       'text': ' '.join(scene['beats']), 'timingStatus': 'placed',
                       'reviewStatus': 'proposed_scene_timing', 'proposalSource': str(source.relative_to(BASE))})
    if args.register:
        track = next(track for track in timeline['tracks'] if track['id'] == 'scenes')
        unrelated = [item for item in track['items'] if item.get('proposalSource') and not item['proposalSource'].startswith('production/story-timing-')]
        if track['items'] and len(unrelated) != len(track['items']) and any(not item.get('proposalSource', '').startswith('production/story-timing-') for item in track['items']):
            raise ValueError('Existing unrelated scenes require an explicit merge')
        track['items'] = sorted(unrelated + scenes, key=lambda item: grid.sec(item['start']))
        timeline_path.write_text(json.dumps(timeline, indent=2, ensure_ascii=False)+'\n')
    styles = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Small,Arial,20,&H00B4ADA2,&H00B4ADA2,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,60,60,35,1
Style: Title,Arial,40,&H00F0E8DB,&H00F0E8DB,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,7,60,60,94,1
Style: Story,Arial,32,&H00E9E2D5,&H00E9E2D5,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,60,60,180,1
Style: Turn,Arial,24,&H008BC5E8,&H008BC5E8,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,60,60,510,1
Style: Lyric,Arial,25,&H00CDC5B7,&H00CDC5B7,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,0,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    events = []

    def event(start, end, style, text):
        if end > start:
            events.append(f'Dialogue: 0,{stamp(start,fps)},{stamp(end,fps)},{style},,0,0,0,,{text}')

    report = [f'# Story timing {version}', '', 'Proposed scenes, not final shots. All scene starts use the cached DAW grid. The final frame covers the audio tail.', '', '| Scene | Time | Length | On screen | Lyric relationship |', '| --- | --- | --- | --- | --- |']
    for i, scene in enumerate(scenes):
        a,b = scene['startFrame'], scene['endFrameExclusive']
        event(a,b,'Small',f"{scene['act']}   /   SCENE {i+1:02d} OF {len(scenes):02d}   /   STORY PASS {version.upper()}")
        event(a,b,'Title',plain(scene['title']))
        lines = []
        for beat in scene['beats']:
            wrapped = textwrap.wrap(plain(beat), width=73)
            lines.extend(wrapped)
            lines.append('')
        assert len(lines) <= 10, (scene['id'], lines)
        event(a,b,'Story',r'\N'.join(lines).rstrip(r'\N'))
        turn = r'\N'.join(textwrap.wrap('STORY TURN  /  '+plain(scene['turn']), width=90))
        event(a,b,'Turn',turn)
        event(a,b,'Small',r'{\pos(60,680)}'+f"{scene['start']} - {scene['end']}   |   {(b-a)/fps:.1f}s   |   DRAFT SCENE BOUNDARIES - SHOTS COME LATER")
        report.append(f"| {scene['id']} — {scene['title']} | {clock(a/fps)}–{clock(b/fps)} | {(b-a)/fps:.2f}s | {' '.join(scene['beats'])} | {scene['lyricLink']} |")
    for second in range(math.ceil(total/fps)):
        event(second*fps,min((second+1)*fps,total),'Small',r'{\an9\pos(1220,35)}'+f'{clock(second)} / {clock(total/fps)}')
    lyrics = next(track['items'] for track in timeline['tracks'] if track['id']=='lyrics')
    for cue in lyrics:
        if cue.get('timingStatus') == 'unplaced':
            continue
        a,b = (round(grid.sec(cue[key])*fps) for key in ['start','end'])
        line = r'\N'.join(textwrap.wrap(plain(cue.get('displayText',cue['text'])),width=85))
        event(a,b,'Lyric',r'{\pos(640,621)}'+line)
    captions = out/'story.ass'
    captions.write_text(styles+'\n'.join(events)+'\n')
    (source.parent/'scene-timing.json').write_text(json.dumps({'fps':fps,'totalFrames':total,'scenes':scenes},indent=2,ensure_ascii=False)+'\n')
    (BASE/'STORY-TIMELINE.md').write_text('\n'.join(report)+'\n')
    master = (BASE/project['sources']['audio']).resolve()
    # Pillow text cards avoid depending on an FFmpeg build with libass.
    font_path = '/System/Library/Fonts/Supplemental/Arial.ttf'
    bold_path = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
    fonts = {size: ImageFont.truetype(font_path, size) for size in [20,24,25,32]}
    title_font = ImageFont.truetype(bold_path,40)
    lyric_spans = [(round(grid.sec(c['start'])*fps),round(grid.sec(c['end'])*fps),c.get('displayText',c['text'])) for c in lyrics if c.get('timingStatus')!='unplaced']
    command = ['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(fps),'-i','pipe:0','-i',str(master),'-af',f'apad=whole_dur={total/fps}','-frames:v',str(total),'-t',str(total/fps),'-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',str(movie)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    previous_key, pixels, scene_index = None, None, 0
    for frame in range(total):
        while frame >= scenes[scene_index]['endFrameExclusive']:
            scene_index += 1
        scene = scenes[scene_index]
        lyric = next((text for a,b,text in lyric_spans if a <= frame < b), '')
        key = (scene_index,lyric,frame//fps)
        if key != previous_key:
            card = Image.new('RGB',(1280,720),'#101c25')
            draw = ImageDraw.Draw(card)
            draw.line((60,153,1220,153), fill='#b68f53',width=2)
            draw.line((60,583,1220,583), fill='#34424b',width=1)
            draw.text((60,35),f"{scene['act']}  /  SCENE {scene_index+1:02d} OF {len(scenes):02d}  /  STORY PASS {version.upper()}",font=fonts[20],fill='#b4ada2')
            draw.text((1220,35),f'{clock(frame/fps)} / {clock(total/fps)}',anchor='ra',font=fonts[20],fill='#b4ada2')
            draw.text((60,94),scene['title'],font=title_font,fill='#f0e8db')
            y = 185
            for beat in scene['beats']:
                for line in textwrap.wrap(beat,width=73):
                    assert draw.textlength(line,font=fonts[32]) < 1160
                    draw.text((60,y),line,font=fonts[32],fill='#e9e2d5')
                    y += 38
                y += 12
            assert y <= 507, (scene['id'],y)
            for j,line in enumerate(textwrap.wrap('STORY TURN  /  '+scene['turn'],width=90)):
                draw.text((60,515+j*29),line,font=fonts[24],fill='#e8c58b')
            lyric_lines = textwrap.wrap(lyric,width=85)
            for j,line in enumerate(lyric_lines):
                draw.text((640,608+j*29),line,anchor='ma',font=fonts[25],fill='#cdc5b7')
            draw.text((60,680),f"{scene['start']} - {scene['end']}  |  {scene['frames']/fps:.1f}s  |  DRAFT SCENES - SHOTS COME LATER",font=fonts[20],fill='#b4ada2')
            pixels, previous_key = card.tobytes(), key
        process.stdin.write(pixels)
    process.stdin.close()
    if process.wait():
        raise RuntimeError('FFmpeg story render failed')
    probe = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,nb_frames,r_frame_rate,width,height','-of','json',str(movie)],text=True))
    video = next(s for s in probe['streams'] if s['codec_type']=='video')
    assert int(video['nb_frames'])==total and video['r_frame_rate']==f'{fps}/1'
    assert any(s['codec_type']=='audio' for s in probe['streams'])
    selection = '+'.join(f"eq(n,{s['startFrame']+12})" for s in scenes)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(movie),'-vf',f"select='{selection}',scale=640:-1,tile=3x6",'-frames:v','1',str(out/'review-scenes.jpg')],check=True)
    (out/'receipt.json').write_text(json.dumps({'totalFrames':total,'fps':fps,'sceneCount':len(scenes),'sourceSHA256':digest(source),'masterSHA256':digest(master),'timelineSHA256':digest(timeline_path),'probe':probe},indent=2)+'\n')
    (out/'.disposable').write_text(f'Regenerate from retained master, timeline lyrics and scene specification:\n./.venv/bin/python3 projects/open-up-the-secret-room/production/render_story_review.py --version {args.version}\n')
    print(movie)


if __name__ == '__main__':
    main()
