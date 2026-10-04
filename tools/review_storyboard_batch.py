"""Assemble frame-trimmed Blender reviews and a small storyboard review page."""
import argparse
import html
import json
import pathlib
import subprocess

from timeline import load_project


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=pathlib.Path)
    parser.add_argument('batch',type=pathlib.Path)
    parser.add_argument('--assemble',action='store_true')
    args=parser.parse_args()
    project,base=load_project(args.project)
    spec=json.loads(args.batch.read_text(encoding='utf-8'))
    out=base/spec['output']
    shots=[s for s in json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))['shots'] if s.get('batch')==spec['id']]
    fps=project['render']['fps']
    if args.assemble:
        cmd=['ffmpeg','-y','-v','error']
        filters=[]
        font = pathlib.Path('C:/Windows/Fonts/arial.ttf')
        font_arg = "fontfile='C\\:/Windows/Fonts/arial.ttf':" if font.exists() else ''
        for i,shot in enumerate(shots):
            cmd+=['-i',str(out/(shot['id']+'-handles.mp4'))]
            lead=shot['handles']['leadInFrames']
            filters.append(f"[{i}:v]trim=start_frame={lead}:end_frame={lead+shot['frames']},setpts=PTS-STARTPTS,drawtext={font_arg}text='{shot['id']}':x=12:y=12:fontsize=18:fontcolor=white:box=1:boxcolor=black@0.5[v{i}]")
        cmd+=['-i',str(base/project['sources']['audio'])]
        filters.append(''.join(f'[v{i}]' for i in range(len(shots)))+f'concat=n={len(shots)}:v=1:a=0[video]')
        seconds=sum(s['frames'] for s in shots)/fps
        filters.append(f'[{len(shots)}:a]atrim=start={shots[0]["startSeconds"]}:duration={seconds},asetpts=PTS-STARTPTS[audio]')
        cmd+=['-filter_complex',';'.join(filters),'-map','[video]','-map','[audio]',
              '-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-r',str(fps),
              '-movflags','+faststart',str(out/'opening-edit-review.mp4')]
        subprocess.run(cmd,check=True)
    cards=[]
    for shot in shots:
        ident=shot['id'];h=shot['handles']
        esc=html.escape
        shell_review=f'<p class="timing">Shell review: {esc(shot["shellReview"])}</p>' if shot.get('shellReview') else ''
        illustration = ''
        starting_frame=shot.get('startingFrameRef',f'{ident}-starting-frame-v01.png')
        starting_frame=pathlib.Path(starting_frame).name
        if (out/starting_frame).exists():
            illustration = f'<div class="frames"><figure><img src="{ident}-lead-in.png"><figcaption>Blender start · includes lead-in</figcaption></figure><figure><img src="{starting_frame}"><figcaption>Image Gen start · draft, check continuity</figcaption></figure></div>'
        if shot.get('endingFrameRef'):
            end_frame=pathlib.Path(shot['endingFrameRef']).name
            if (out/end_frame).exists():
                illustration+=f'<figure><img src="{end_frame}"><figcaption>Image Gen edit-end reference · reveal / widening</figcaption></figure>'
        registration=''
        if (out/(ident+'-geodesic-registration.png')).exists():
            registration=f'''<details open><summary>Active shell · bright geometry references</summary>
<p>Ultra-thin clear material. The cyan geodesic network is an optional technological display; it can be faint, glowing or absent. Reference fill lights clarify geometry.</p>
<div class="frames"><figure><img src="{ident}-neutral-registration.png"><figcaption>Ring width · neutral fill</figcaption></figure><figure><img src="{ident}-geodesic-registration.png"><figcaption>Spherical network · 150 hexagons, 12 pentagonal closures</figcaption></figure></div>
<a href="shell-registration-v01.blend" download>Editable shell network and reference lights</a></details>'''
        cards.append(f'''<article id="{ident}"><h2>{ident} · {esc(shot['title'])}</h2>
<p class="timing">Edit {shot['startSeconds']:.3f}–{shot['endSeconds']:.3f} s · {shot['frames']} frames · +{h['leadInFrames']}/{h['leadOutFrames']} handle frames · generated {h['generatedFrames']/fps:.3f} s</p>
{illustration}
{shell_review}
{registration}
<div class="frames"><figure><img src="{ident}-edit-in.png"><figcaption>Edit in</figcaption></figure><figure><img src="{ident}-edit-out.png"><figcaption>Edit out</figcaption></figure></div>
<video controls preload="metadata" src="{ident}-handles.mp4" poster="{ident}-edit-in.png" data-end="{(h['leadInFrames']+shot['frames'])/fps}"></video><button class="play-edit">Play edit only</button><button class="play-handles">Play with handles</button>
<p>{esc(shot['description'])}</p><p class="timing">{esc(shot['blocking']['transition'])}</p>
<details><summary>Original note · {shot['sourceNoteId'][:8]}</summary><p>{esc(shot['sourceNoteText'])}</p></details></article>''')
    page='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Opening storyboard · Blender review</title>
<style>:root{color-scheme:dark}body{margin:0;background:#11282d;color:#f1dfb6;font:15px/1.45 system-ui}main{max-width:1120px;margin:auto;padding:20px}header{position:sticky;top:0;background:#11282d;padding:10px 0;border-bottom:1px solid #39545a;z-index:2}h1{font-size:22px;margin:0}h2{font-size:18px}a{color:#a6d9df}nav{display:flex;gap:16px;flex-wrap:wrap;margin:8px 0}article{background:#193239;padding:18px;margin:18px 0;border:1px solid #39545a;border-radius:6px}.frames{display:flex;gap:12px}figure{margin:0;flex:1;min-width:0}img{width:100%}figcaption,.timing{font-size:13px;color:#a0b6b3}video{width:100%;max-height:430px;background:#0c2024}button{padding:8px;color:inherit;background:#223e44;border:1px solid #527075;margin:6px;cursor:pointer}details p{white-space:pre-wrap}@media(max-width:700px){.frames{display:block}}</style>
<main><header><h1>Opening storyboard · five Blender shots</h1><nav><a href="/">Listening notes</a><a href="opening-storyboard-v01.blend" download>Editable Blender scenes</a>'''
    page+=''.join(f'<a href="#{s["id"]}">{s["id"]}</a>' for s in shots)
    page+='''</nav></header><p>Rebuilt opening scene with the approved thin field shell, faint geodesic network and shared ship geometry. Five regenerated illustration starts; entrance, pullback and widening also have end references. Character and planet in the Blender movies are proxies. Each source clip includes 12 frames before and after the edit. The combined motion preview trims those handles and uses the master audio. Illustration frames are storyboard references; generated video has not yet been tested.</p><video controls preload="metadata" src="opening-edit-review.mp4"></video>'''
    page+=''.join(cards)
    page+='''</main><script>for(const card of document.querySelectorAll('article')){const video=card.querySelector('video');let end=null;card.querySelector('.play-edit').onclick=()=>{video.currentTime=.5;end=Number(video.dataset.end);video.play()};card.querySelector('.play-handles').onclick=()=>{video.currentTime=0;end=null;video.play()};video.ontimeupdate=()=>{if(end!==null&&video.currentTime>=end){video.pause();end=null}}}</script>'''
    (out/'index.html').write_text(page,encoding='utf-8')
    print(out/'index.html')


if __name__=='__main__':main()
