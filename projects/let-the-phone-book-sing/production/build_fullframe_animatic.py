"""Full-frame review layout, removable timed lyric overlay, native opening plate."""
import argparse
import bisect
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'generated/visual-animatic-v006'
FPS=24

def overlay_lyrics(source,target,lines,total):
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',34)
    starts=[max(0,l['words'][0]['startFrame']-6) for l in lines]
    layouts=[]
    for line in lines:
        rows=[[]];used=0;gap=font.getlength(' ')
        for word in line['words']:
            width=font.getlength(word['text'])
            if used+width>1740 and rows[-1]:rows.append([]);used=0
            rows[-1].append((word,width));used+=width+gap
        positions=[]
        for ri,row in enumerate(rows):
            x=(1920-sum(w for _,w in row)-gap*(len(row)-1))/2
            y=120-38-42*(len(rows)-ri)
            for word,width in row:positions.append((word,x,y));x+=width+gap
        layouts.append(positions)
    dec=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-frames:v',str(total),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    enc=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','24','-i','-', '-i',str(source),'-map','0:v','-map','1:a','-frames:v',str(total),'-c:v','libx264','-preset','fast','-crf','18','-c:a','copy','-movflags','+faststart',str(target)],stdin=subprocess.PIPE)
    cache={}
    for frame in range(total):
        raw=dec.stdout.read(1920*1080*3);assert len(raw)==1920*1080*3
        li=bisect.bisect_right(starts,frame)-1
        active=li>=0 and frame<lines[li]['words'][-1]['endFrameExclusive']+8
        if active:
            positions=layouts[li];colors=tuple('#ffd46b' if w['startFrame']<=frame<w['endFrameExclusive'] else ('white' if frame>=w['endFrameExclusive'] else '#d5d5d5') for w,x,y in positions)
            key=(li,colors)
            if key not in cache:
                patch=Image.new('RGBA',(1920,120));draw=ImageDraw.Draw(patch)
                for (w,x,y),color in zip(positions,colors):draw.text((x,y),w['text'],font=font,fill=color,stroke_width=2,stroke_fill='#141118')
                cache[key]=patch
            picture=Image.frombytes('RGB',(1920,1080),raw);picture.paste(cache[key],(0,960),cache[key]);raw=picture.tobytes()
            if frame in [82,330,410]:picture.save(OUT/f'layout-frame-{frame}.jpg')
        enc.stdin.write(raw)
    dec.stdout.close();dec.wait();enc.stdin.close();assert enc.wait()==0

def stamp(frame):
    # ASS has centisecond precision; edges round from accepted integer frames.
    cs=round(frame*100/FPS)
    return f'{cs//360000}:{cs//6000%60:02}:{cs//100%60:02}.{cs%100:02}'

def subtitles(lines,total):
    header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,34,&H00FFFFFF,&H00FFFFFF,&H00141118,&H80000000,0,0,0,0,100,100,0,0,1,2,1,2,90,90,38,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    events=[]
    for line in lines:
        words=line['words'];start=max(0,words[0]['startFrame']-6);end=min(total,words[-1]['endFrameExclusive']+8)
        if start>=end:continue
        edges=sorted({start,end,*[f for w in words for f in (w['startFrame'],w['endFrameExclusive']) if start<f<end]})
        for a,b in zip(edges,edges[1:]):
            parts=[]
            for w in words:
                color='&H006BD4FF&' if w['startFrame']<=a<w['endFrameExclusive'] else ('&H00FFFFFF&' if a>=w['endFrameExclusive'] else '&H00D5D5D5&')
                text=w['text'].replace('{','').replace('}','').replace('\\','')
                parts.append('{\\c'+color+'}'+text)
            events.append(f'Dialogue: 0,{stamp(a)},{stamp(b)},Default,,0,0,0,,'+ ' '.join(parts))
    return header+'\n'.join(events)+'\n'

def main():
    global OUT
    parser=argparse.ArgumentParser();parser.add_argument('--belle',action='store_true');parser.add_argument('--version',default='v006');parser.add_argument('--preview-end',type=int,default=437);parser.add_argument('--dissolve-frames',type=int,choices=[0,4],default=0);args=parser.parse_args()
    OUT=BASE/f'generated/visual-animatic-{args.version}'
    OUT.mkdir(exist_ok=True);assets=OUT/'frames';assets.mkdir(exist_ok=True)
    timeline=BASE/'timeline.json';before=hashlib.sha256(timeline.read_bytes()).hexdigest()
    score=json.loads((BASE/'shots/shotlist.json').read_text());total=score['endFrameExclusive']
    lines=next(t['items'] for t in json.loads(timeline.read_text())['tracks'] if t['id']=='lyrics')
    seq=[]
    for s in score['shots']:
        im=Image.open(BASE/s['image']).convert('RGB');x0,y0,x1,y1=s['crop'];im=im.crop((round(x0*im.width),round(y0*im.height),round(x1*im.width),round(y1*im.height)))
        im=ImageOps.fit(im,(1920,1080),Image.Resampling.LANCZOS)
        if s['placeholder']:
            ImageDraw.Draw(im).text((20,18),'BLOCKING PLACEHOLDER — '+s['title'],font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',23),fill='white',stroke_width=2,stroke_fill='#15151c')
        file=assets/(s['id']+'.png');im.save(file)
        seq.extend(["file '"+str(file.resolve())+"'","option framerate 24",f"duration {s['frames']/FPS:.9f}"])
    seq.extend([seq[-3],"option framerate 24"]);(OUT/'stills.ffconcat').write_text('\n'.join(seq)+'\n')
    (OUT/'lyrics.ass').write_text(subtitles(lines,total))
    inputs=['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(OUT/'stills.ffconcat')]
    filters=['[0:v]fps=24,format=yuv420p[base]'];prev='base';n=1
    for insert in score['reviewVideoInserts']:
        if insert['id']=='belle-continuous' and not args.belle:continue
        inputs+=['-i',str(BASE/insert['source'])]
        start,end=insert['startFrame'],insert['endFrameExclusive'];offset=insert['sourceOffsetFrames']
        filters.append(f'[{n}:v]fps=24,trim=start_frame={offset}:end_frame={offset+end-start},setpts=PTS-STARTPTS+{start}/24/TB,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[p{n}]')
        filters.append(f"[{prev}][p{n}]overlay=0:0:eof_action=pass:enable='gte(n,{start})*lt(n,{end})'[v{n}]")
        prev=f'v{n}';n+=1
    filters.append(f'[{prev}]null[final]')
    inputs+=['-i',str(BASE/'generated/source/master.wav')]
    clean=OUT/f'Let-the-Phone-Book-Sing-fullframe-clean-{args.version}.mp4'
    subprocess.run(inputs+['-filter_complex',';'.join(filters),'-map','[final]','-map',f'{n}:a','-frames:v',str(total),'-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','320k','-af','apad','-t',str(total/FPS),'-movflags','+faststart',str(clean)],check=True)
    if args.dissolve_frames:
        from review_dissolves import apply_dissolves
        hardcuts=clean.with_name(clean.stem+'-hardcuts.mp4')
        clean.rename(hardcuts)
        apply_dissolves(hardcuts,clean,score,assets,BASE,total,args.dissolve_frames)
    review=OUT/f'Let-the-Phone-Book-Sing-fullframe-lyrics-{args.version}.mp4'
    overlay_lyrics(clean,review,lines,total)
    for source,name in [(review,'opening-sequence-review.mp4'),(clean,'opening-sequence-clean.mp4')]:
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-frames:v',str(args.preview_end),'-c:v','libx264','-preset','fast','-crf','18','-c:a','copy','-t',str(args.preview_end/FPS),'-movflags','+faststart',str(OUT/name)],check=True)
    assert hashlib.sha256(timeline.read_bytes()).hexdigest()==before
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=width,height,nb_read_frames','-of','json',str(review)]))
    assert int(probe['streams'][0]['nb_read_frames'])==total
    (OUT/'validation.json').write_text(json.dumps(dict(video=probe,timelineSha256=before,lyrics='Removable ASS overlay; accepted word frames preserved, gold active word; no footer.',opening='Approved sing-echo-v002',belleContinuous=args.belle,knownTemporaryMedia='Original lower-resolution chorus test retained; remaining scenes are still blocking.'),indent=2)+'\n')
    print(review)
if __name__=='__main__':main()
