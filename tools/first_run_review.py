"""Render location-reference shot cards and an audio timing review from a shotlist.

Cards deliberately show source locations and cast references, not invented
finished shot compositions. Frame boundaries come only from shots/shotlist.json.
"""
import argparse
import importlib.util
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('project', type=Path)
    ap.add_argument('--renderer', type=Path, required=True)
    ap.add_argument('--video', action='store_true')
    args = ap.parse_args()
    base = args.project.resolve().parent
    project = json.loads(args.project.read_text())
    score = json.loads((base/'shots/shotlist.json').read_text())
    shots = [s for s in score['shots'] if s['batch']=='first-run-v001']
    fps = score['fps']
    assert score['frameIndexBase'] == 0 and shots[0]['startFrame'] == 0
    assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(shots,shots[1:]))
    compiled = json.loads((base/project['timing']['compiledTimeline']).read_text())
    lyrics = next(t['items'] for t in compiled['tracks'] if t['id']=='lyrics')
    cast = {}
    for register in ['supporting-refs-v004','core-threat-refs-v001']:
        for row in json.loads((base/f'character-development/{register}/height-register.json').read_text())['characters']:
            cast[row['id']] = row
    locations = dict(zip(['market','depot','court','relay'], ['market-approach','water-broker-forecourt','split-reunion-court','access-relay-hall']))
    out = base/'generated/storyboard/first-run-v001'
    cards = out/'cards'
    cards.mkdir(parents=True,exist_ok=True)
    font_path = base/'generated/animatic/assets/BarlowSemiCondensed-SemiBold.ttf'
    def font(size): return ImageFont.truetype(str(font_path),size)
    def paragraph(draw, text, x, y, width, size=28, color='#293d3e'):
        words=text.split();line='';f=font(size)
        for word in words:
            candidate=(line+' '+word).strip()
            if line and draw.textlength(candidate,font=f)>width:
                draw.text((x,y),line,font=f,fill=color);y+=size+8;line=word
            else:line=candidate
        if line:draw.text((x,y),line,font=f,fill=color);y+=size+8
        return y
    manifest=[];text_score=[];video_cards=[]
    for shot in shots:
        im=Image.new('RGB',(1920,1080),'#f6f1e8');d=ImageDraw.Draw(im)
        d.text((42,25),f"{shot['id'].upper()}  /  {shot['title']}",font=font(43),fill='#293d3e')
        timing=f"{shot['startSeconds']:.3f}–{shot['endSeconds']:.3f}s  |  {shot['frames']} frames  |  {fps} fps"
        d.text((42,83),timing,font=font(26),fill='#9b5035')
        env=Image.open(base/f"generated/environment-development/first-run-v001/{locations[shot['location']]}-v001.png").convert('RGB')
        env=ImageOps.contain(env,(1230,650),Image.Resampling.LANCZOS)
        im.paste(env,(42+(1230-env.width)//2,150+(650-env.height)//2))
        d.text((42,815),'LOCATION REFERENCE / Camera and actor placement described at right',font=font(25),fill='#293d3e')
        x=42
        for cid in shot['cast']:
            art=Image.open(base/cast[cid]['image']).convert('RGB')
            art=ImageOps.contain(art,(160,175),Image.Resampling.LANCZOS)
            im.paste(art,(x,855));d.text((x,1035),cid,font=font(24),fill='#293d3e');x+=210
        y=150
        y=paragraph(d,'CAMERA INTENT',1320,y,550,24,'#9b5035')
        y=paragraph(d,shot['camera'],1320,y,550,31)+22
        y=paragraph(d,'BLOCKING',1320,y,550,24,'#9b5035')
        y=paragraph(d,shot['description'],1320,y,550,30)+22
        cue=' / '.join(l['text'] for l in lyrics if shot['startFrame'] <= l['startFrame'] < shot['endFrameExclusive']) or 'Instrumental / held action'
        y=paragraph(d,'LYRIC CUE',1320,y,550,24,'#9b5035')
        y=paragraph(d,cue,1320,y,550,27)+22
        y=paragraph(d,'CONTINUITY',1320,y,550,24,'#9b5035')
        y=paragraph(d,shot['continuity'],1320,y,550,25)
        if y>990:raise ValueError(f"Text overflow in {shot['id']}: {y}")
        d.text((1320,1035),'PLANNING CARD / NOT STAGED SHOT ART',font=font(23),fill='#9b5035')
        path=cards/(shot['id']+'.png');im.save(path)
        video_cards.append((im.resize((1280,720),Image.Resampling.LANCZOS),shot['frames']))
        manifest.append({'index':shot['id'],'title':shot['title']+' · '+timing,'src':'../cards/'+path.name,'href':'../cards/'+path.name})
        text_score += [shot['id']+' / '+shot['title'],timing,'Musical: '+shot['start']+' → '+shot['end'],'Camera: '+shot['camera'],'Cast: '+', '.join(shot['cast']),'Action: '+shot['description'],'Lyric: '+cue,'Continuity: '+shot['continuity'],'']
    (base/'shots/first-run-shot-score.txt').write_text('\n'.join(text_score)+'\n')
    spec=importlib.util.spec_from_file_location('review_renderer',args.renderer);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    review=out/'review';review.mkdir(exist_ok=True)
    module.build_review_html(review,manifest,{'preset':'image-wall','showCaptions':True,'showPrompts':False,'minTileWidth':600,'title':'Together Anyways · first-run shot plan','output':'shot-board.html'})
    if args.video:
        total=sum(n for _,n in video_cards)
        command=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(fps),'-i','pipe:0','-i',str(base/'generated/animatic/assets/master.wav'),'-map','0:v:0','-map','1:a:0','-frames:v',str(total),'-t',str(total/fps),'-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out/'first-run-planning-animatic.mp4')]
        proc=subprocess.Popen(command,stdin=subprocess.PIPE)
        try:
            for image,count in video_cards:
                frame=image.tobytes()
                for _ in range(count):proc.stdin.write(frame)
        finally:proc.stdin.close()
        if proc.wait():raise RuntimeError('FFmpeg render failed')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f"Rendered {len(shots)} planning cards; {sum(s['frames'] for s in shots)} frames")


if __name__=='__main__':main()
