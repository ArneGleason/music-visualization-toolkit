"""Render canonical story edit with stills, retained motion, lyric strip and future cards."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps
BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE.parents[1] / 'tools'))
from timeline import MusicalGrid


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clock(frame, fps=24):
    seconds = frame // fps
    return f'{seconds // 60}:{seconds % 60:02}'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--version', type=int, required=True)
    ap.add_argument('--shotlist', type=Path, default=BASE/'shots/shotlist.json')
    args = ap.parse_args()
    tag = f'v{args.version:03}'
    out = BASE/f'generated/wip/previews/story-stills/{tag}'
    out.mkdir(parents=True, exist_ok=True)
    movie = out/f'Secret-Room-story-stills-{tag}.mp4'
    if movie.exists():
        raise ValueError('Use a new version; preview already exists')
    score = json.loads(args.shotlist.read_text())
    project = json.loads((BASE/'project.json').read_text())
    timeline_path = BASE/f'production/story-stills-{tag}/timeline.json'
    timeline = json.loads(timeline_path.read_text())
    grid = MusicalGrid(json.loads((BASE/project['timing']['beatmap']).read_text()))
    fps = score['fps']; shots = score['shots']; total = score['totalFrames']
    assert shots[0]['startFrame'] == 0 and shots[-1]['endFrameExclusive'] == total
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(shots,shots[1:]))
    lyrics = [(round(grid.sec(c['start'])*fps),round(grid.sec(c['end'])*fps),c.get('displayText',c['text'])) for tr in timeline['tracks'] if tr['id']=='lyrics' for c in tr['items'] if c.get('timingStatus')!='unplaced']
    font_path='/System/Library/Fonts/Supplemental/Arial.ttf'
    font={n:ImageFont.truetype(font_path,n) for n in [18,22,27,38]}
    master=BASE/project['sources']['audio']
    proc=subprocess.Popen(['ffmpeg','-v','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(fps),'-i','pipe:0','-i',str(master),'-af',f'apad=whole_dur={total/fps}','-frames:v',str(total),'-t',str(total/fps),'-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',str(movie)],stdin=subprocess.PIPE)
    hashes={}; thumbs=[]; report=['# Story-stills pacing review '+tag,'',score.get('reviewScope','Full master; current artwork followed by explicitly unfinished story cards.')+' All cuts derive from the cached musical grid. Static holds indicate room for acting, not frozen final footage.','','| Time | Length | Image / shot | Direction |','| --- | --- | --- | --- |']
    try:
        for i,s in enumerate(shots):
            assert s['frames']==s['endFrameExclusive']-s['startFrame']
            source=None; decoder=None; still=None
            if s.get('videoSource'):
                source=(BASE/s['videoSource']).resolve()
                first=s['videoEdit']['sourceInFrame']
                decoder=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-vf',f'trim=start_frame={first}:end_frame={first+s["frames"]},setpts=PTS-STARTPTS,scale=1280:720,setsar=1','-frames:v',str(s['frames']),'-f','rawvideo','-pix_fmt','rgb24','pipe:1'],stdout=subprocess.PIPE)
            elif s.get('starterImage'):
                source=(BASE/s['starterImage']).resolve()
                still=ImageOps.fit(Image.open(source).convert('RGB'),(1280,720))
            else:
                assert s.get('storyCard')
                still=Image.new('RGB',(1280,720),'#101c25')
                draw=ImageDraw.Draw(still)
                draw.text((60,120),'FUTURE STORY / NO SHOT GENERATED',font=font[22],fill='#e7b974')
                y=185
                for line in textwrap.wrap(s['title'],48):
                    draw.text((60,y),line,font=font[38],fill='#f3ece0'); y+=46
                y+=28
                for line in textwrap.wrap(s['reviewDirection'],76):
                    draw.text((60,y),line,font=font[27],fill='#cbd5d9'); y+=36
            if source: hashes[str(source)]=sha(source)
            previous=None; pixels=None
            for frame in range(s['startFrame'],s['endFrameExclusive']):
                lyric=next((t for a,b,t in lyrics if a<=frame<b),'')
                key=(frame//fps,lyric)
                if decoder:
                    raw=decoder.stdout.read(1280*720*3)
                    if len(raw)!=1280*720*3: raise RuntimeError('Short source video: '+str(source))
                    card=Image.frombytes('RGB',(1280,720),raw)
                elif key!=previous: card=still.copy()
                if decoder or key!=previous:
                    overlay=Image.new('RGBA',(1280,720)); draw=ImageDraw.Draw(overlay)
                    draw.rectangle((0,0,1280,40),fill=(5,12,18,205))
                    draw.rectangle((0,600,1280,720),fill=(5,12,18,230))
                    label=s.get('imageLabel','MOTION' if decoder else 'STORY CARD')
                    draw.text((18,10),f'{i+1:02}/{len(shots)}  |  {label}  |  {s["title"]}',font=font[18],fill='#f0e7d6')
                    draw.text((1260,10),f'{clock(frame,fps)} / {clock(total,fps)}',font=font[18],fill='#e7b974',anchor='ra')
                    direction=s['reviewDirection'] if not s.get('storyCard') else 'PROVISIONAL STORY SPACE — mechanism and shot design still open'
                    lines=textwrap.wrap(direction,106)
                    for j,line in enumerate(lines[:2]): draw.text((20,610+j*25),line,font=font[22],fill='#eeeeea')
                    draw.text((640,680),lyric,font=font[22],fill='#c6c3b8',anchor='ma')
                    card=Image.alpha_composite(card.convert('RGBA'),overlay).convert('RGB')
                    pixels=card.tobytes(); previous=key
                    if frame==s['startFrame']:
                        thumbs.append(card.resize((320,180)))
                        if i in [0,12,22,30,31,39]: card.save(out/f'check-{i+1:02}.jpg')
                proc.stdin.write(pixels)
            if decoder:
                decoder.stdout.close()
                if decoder.wait(): raise RuntimeError('Source decode failed')
            report.append(f'| {clock(s["startFrame"])}–{clock(s["endFrameExclusive"])} | {s["frames"]/fps:.2f}s | {s.get("imageLabel",s["id"])} — {s["title"]} | {s["reviewDirection"]} |')
            print(f'{i+1}/{len(shots)} {s["title"]}',flush=True)
    finally:
        proc.stdin.close()
    if proc.wait(): raise RuntimeError('Render failed')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,nb_frames,r_frame_rate,width,height:format=duration','-of','json',str(movie)],text=True))
    v=next(s for s in probe['streams'] if s['codec_type']=='video')
    assert int(v['nb_frames'])==total and v['r_frame_rate']==f'{fps}/1'
    assert any(s['codec_type']=='audio' for s in probe['streams'])
    sheet=Image.new('RGB',(1280,180*((len(thumbs)+3)//4)))
    for i,thumb in enumerate(thumbs): sheet.paste(thumb,((i%4)*320,(i//4)*180))
    sheet.save(out/'contact-sheet.jpg')
    (BASE/f'production/story-stills-{tag}/timing-review.md').write_text('\n'.join(report)+'\n')
    (out/'receipt.json').write_text(json.dumps({'fps':fps,'totalFrames':total,'shotCount':len(shots),'sourceHashes':hashes,'masterSHA256':sha(master),'shotlistSHA256':sha(args.shotlist),'probe':probe},indent=2)+'\n')
    snapshot=BASE/f'production/story-stills-{tag}/shotlist.json'
    (out/'.disposable').write_text(f'Reproduce from retained sources and shotlist snapshot into a fresh version folder (or after removing this disposable output):\n./.venv/bin/python3 projects/open-up-the-secret-room/production/render_story_stills.py --version {args.version} --shotlist {snapshot}\n')
    print(movie)

if __name__=='__main__': main()
