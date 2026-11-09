"""Render a review MP4 from shots/shotlist.json and untouched accepted lyric frames."""
import bisect
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'generated/visual-animatic-v001'
FONT = BASE / 'generated/animatic/assets/BarlowSemiCondensed-SemiBold.ttf'
W, H, ART_H = 1280, 720, 600


def load(path):
    return json.loads(path.read_text())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    score = load(BASE / 'shots/shotlist.json')
    timeline_path = BASE / 'timeline.json'
    timing_hash = hashlib.sha256(timeline_path.read_bytes()).hexdigest()
    lines = next(t['items'] for t in load(timeline_path)['tracks'] if t['id'] == 'lyrics')
    shots, fps = score['shots'], score['fps']
    total = score['endFrameExclusive']
    assert shots[0]['startFrame'] == 0
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(shots,shots[1:]))
    assert all(s['frames'] > 0 and (BASE/s['image']).exists() for s in shots)
    assert len({s['promptLock'] for s in shots}) == 1
    # Compare accepted word frames to the previously reviewed timing animatic.
    old = load(BASE / 'generated/animatic/layout.json')
    old_words = {w['id']:(w['onFrame'],w['offFrame']) for page in old for w in page['words']}
    words = [w for line in lines for w in line['words']]
    assert all(old_words[w['id']] == (w['startFrame'],w['endFrameExclusive']) for w in words)
    pictures = []
    tagfont = ImageFont.truetype(str(FONT), 19)
    for shot in shots:
        source = Image.open(BASE/shot['image']).convert('RGB')
        x0,y0,x1,y1 = shot['crop']
        source = source.crop((round(x0*source.width),round(y0*source.height),round(x1*source.width),round(y1*source.height)))
        source = ImageOps.contain(source, (W,ART_H), Image.Resampling.LANCZOS)
        board = Image.new('RGB',(W,H),'#14181e')
        board.paste(source,((W-source.width)//2,(ART_H-source.height)//2))
        if shot['placeholder']:
            d=ImageDraw.Draw(board)
            label='BLOCKING PLACEHOLDER · '+shot['title']
            d.rectangle((0,0,tagfont.getlength(label)+24,29),fill='#242735')
            d.text((12,4),label,font=tagfont,fill='#efdab5')
        pictures.append(board)
    layouts=[]
    for line in lines:
        for size in [38,36,34,32]:
            font=ImageFont.truetype(str(FONT),size)
            rows=[[]];used=0
            for word in line['words']:
                width=font.getlength(word['text']);gap=font.getlength(' ')+3
                if used+width>W-96 and rows[-1]:rows.append([]);used=0
                rows[-1].append((word,width));used+=width+gap
            if len(rows)<=2:break
        assert len(rows)<=2, line['id']
        positions=[]
        for ri,row in enumerate(rows):
            x=(W-sum(width for _,width in row)-gap*(len(row)-1))/2
            y=ART_H+12+(2-len(rows))*21+ri*44
            for word,width in row:
                positions.append((word,x,y));x+=width+gap
        layouts.append((font,positions))
    starts=[s['startFrame'] for s in shots]
    display_starts=[max(0,l['words'][0]['startFrame']-6) for l in lines]
    def frame_at(frame):
        si=bisect.bisect_right(starts,frame)-1
        picture=pictures[si].copy();d=ImageDraw.Draw(picture)
        li=bisect.bisect_right(display_starts,frame)-1
        if li>=0:
            line=lines[li]
            if frame<line['words'][-1]['endFrameExclusive']+8:
                font,positions=layouts[li]
                for word,x,y in positions:
                    a,b=word['startFrame'],word['endFrameExclusive']
                    color='#ffd46b' if a<=frame<b else ('#f4f2ec' if frame>=b else '#a4acb9')
                    d.text((x,y),word['text'],font=font,fill=color)
                    if a<=frame<b:
                        d.line((x,y+40,x+font.getlength(word['text']),y+40),fill=color,width=2)
        return picture
    # Every visual change has an exact integer-frame boundary. Repeat each
    # rendered state rather than re-layout unchanged stills at every frame.
    edges={0,total,*starts,*display_starts}
    edges.update(l['words'][-1]['endFrameExclusive']+8 for l in lines)
    edges.update(f for word in words for f in (word['startFrame'],word['endFrameExclusive']))
    edges=sorted(f for f in edges if 0<=f<=total)
    target=OUT/'Let-the-Phone-Book-Sing-visual-animatic-v001.mp4'
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(fps),'-i','pipe:0','-i',str(BASE/'generated/source/master.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-af','apad','-t',str(total/fps),'-movflags','+faststart',str(target)]
    with (OUT/'render.log').open('w') as log:
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
        try:
            for a,b in zip(edges,edges[1:]):
                raw=frame_at(a).tobytes()
                for _ in range(b-a):proc.stdin.write(raw)
            proc.stdin.close()
            if proc.wait()!=0:raise RuntimeError((OUT/'render.log').read_text())
        finally:
            if proc.poll() is None:proc.kill()
    # Inspectable overview plus full-size samples of the actual rendered layout.
    sheet=Image.new('RGB',(1280,((len(shots)+3)//4)*205),'#14181e')
    for i,shot in enumerate(shots):
        mid=shot['startFrame']+shot['frames']//2
        thumb=frame_at(mid).resize((320,180))
        sheet.paste(thumb,((i%4)*320,(i//4)*205))
        ImageDraw.Draw(sheet).text(((i%4)*320+5,(i//4)*205+181),f"{shot['id']} {shot['startSeconds']:.1f}s {shot['title'][:31]}",font=ImageFont.truetype(str(FONT),13),fill='white')
    sheet.save(OUT/'contact-sheet.jpg',quality=92)
    for frame in [200,340,740,1280,1800,3100,3700]:
        frame_at(frame).save(OUT/f'preview-{frame}.png')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(target)],text=True))
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert int(video['nb_read_frames'])==total
    assert any(s['codec_type']=='audio' for s in probe['streams'])
    assert hashlib.sha256(timeline_path.read_bytes()).hexdigest()==timing_hash
    report={'fps':fps,'frames':total,'durationSeconds':total/fps,'resolution':[W,H],'shots':len(shots),'placeholderShots':sum(s['placeholder'] for s in shots),'acceptedLyricLines':len(lines),'acceptedWordsVerifiedAgainstOriginalAnimatic':len(words),'timelineSha256':timing_hash,'sourceOfTruth':'shots/shotlist.json','status':'Visual blocking draft; new opening and edit await review; no generated motion','audio':'Original master from time zero; final partial frame padded only'}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'shot-review.txt').write_text('\n\n'.join(f"{s['id']} | {s['startSeconds']:.3f}–{s['endSeconds']:.3f} | {s['title']}\n{s['description']}" for s in shots)+'\n')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__':
    main()
