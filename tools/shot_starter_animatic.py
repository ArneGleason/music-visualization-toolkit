"""Build a clean image-first review with small shot labels and timed lyrics."""
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from animatic_media import Artwork


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('project', type=Path)
    args = ap.parse_args()
    base = args.project.resolve().parent
    project = json.loads(args.project.read_text())
    score = json.loads((base/'shots/shotlist.json').read_text())
    shots = score['shots']
    fps = score['fps']
    assert score['frameIndexBase'] == 0
    assert shots[0]['startFrame'] == 0
    assert all(a['endFrameExclusive'] == b['startFrame'] for a,b in zip(shots,shots[1:]))
    compiled = json.loads((base/project['timing']['compiledTimeline']).read_text())
    lyrics = next(t['items'] for t in compiled['tracks'] if t['id']=='lyrics')
    locations = dict(zip(['market','depot','court','relay'], ['market-approach','water-broker-forecourt','split-reunion-court','access-relay-hall']))
    out = base/'generated/storyboard/first-run-starters-v001'
    out.mkdir(parents=True,exist_ok=True)
    font_path = base/'generated/animatic/assets/BarlowSemiCondensed-SemiBold.ttf'
    font = ImageFont.truetype(str(font_path),24)
    small = ImageFont.truetype(str(font_path),22)
    lyric_font = ImageFont.truetype(str(font_path),20)
    width,height = 1920,1080
    total = shots[-1]['endFrameExclusive']
    video = out/'first-run-clean-animatic-v001.mp4'
    pending_video = out/'first-run-clean-animatic-pending.mp4'
    cmd = ['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}','-r',str(fps),'-i','pipe:0','-i',str(base/project['sources']['audio']),'-map','0:v:0','-map','1:a:0','-frames:v',str(total),'-t',str(total/fps),'-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(video)]
    cmd[-1] = str(pending_video)
    proc = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    manifest = []
    artwork = Artwork(base, shots, fps)
    try:
        for shot in shots:
            starter = base/shot['starterImage'] if shot.get('starterImage') else None
            generated = bool(starter and starter.exists())
            source = starter if generated else base/f"generated/environment-development/first-run-v001/{locations[shot['location']]}-v001.png"
            art = ImageOps.contain(Image.open(source).convert('RGB'),(width,1008),Image.Resampling.LANCZOS)
            canvas = Image.new('RGB',(width,height),'#101516')
            canvas.paste(art,((width-art.width)//2,(1008-art.height)//2))
            d = ImageDraw.Draw(canvas)
            label = f"SCENE {shot['sceneId'][1:]} · {shot['sceneName']}    |    SHOT {str(shot['shotNumber']).zfill(2)} · {shot['title']}"
            d.text((24,1018),label,font=font,fill='#ece8df')
            kind = 'STARTER ' + shot.get('starterRevision', 'v001') if generated else 'LOCATION STUDY · SHOT IMAGE PENDING'
            if shot.get('videoSource'): kind = 'KLING 4 · MOTION REVIEW'
            d.text((width-24,1018),kind,font=small,fill='#d7b88a',anchor='ra')
            manifest.append({'shotId':shot['id'],'displayId':shot['displayId'],'source':shot.get('videoSource',str(source.relative_to(base))),'videoEdit':shot.get('videoEdit'),'transitionIn':shot.get('transitionIn'),'generatedStarter':generated,'startFrame':shot['startFrame'],'endFrameExclusive':shot['endFrameExclusive']})
            for frame in range(shot['startFrame'],shot['endFrameExclusive']):
                im = canvas.copy()
                im.paste(artwork.at(shot,frame),(0,0))
                draw = ImageDraw.Draw(im)
                text = next((l['text'] for l in lyrics if l['startFrame'] <= frame < l['endFrame']),'')
                draw.text((width//2,1050),text,font=lyric_font,fill='#c3c8c6',anchor='ma')
                draw.text((width-24,1050),f'{frame/fps:07.3f}s  ·  F{frame:04d}',font=small,fill='#aeb8b7',anchor='ra')
                if frame == shot['startFrame']:
                    im.save(out/f"{shot['id']}-review.png")
                proc.stdin.write(im.tobytes())
    finally:
        proc.stdin.close()
    if proc.wait(): raise RuntimeError('FFmpeg render failed')
    pending_video.replace(video)
    (out/'animatic-manifest.json').write_text(json.dumps({'fps':fps,'frames':total,'frameIndexBase':0,'shots':manifest},indent=2)+'\n')
    print(video)


if __name__ == '__main__':
    main()
