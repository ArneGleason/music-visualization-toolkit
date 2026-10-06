"""Assemble the proposed continuation with accepted context, audio and lyrics."""
import copy
import html
import json
import pathlib
import subprocess

from lyric_overlay import write_lyrics


def run(args):
    subprocess.run(args,check=True)


def main():
    base=pathlib.Path('projects/a-right-little-something').resolve()
    project=json.loads((base/'project.json').read_text(encoding='utf-8'))
    spec=json.loads((base/'storyboard-space-notes.json').read_text(encoding='utf-8'))
    shots=[s for s in json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))['storyboardProposals'] if s['batch']==spec['id']]
    out=base/spec['output'];fps=project['render']['fps'];start=543;end=shots[-1]['endFrameExclusive']
    assert all(a['endFrameExclusive']==b['startFrame'] for a,b in zip(shots,shots[1:]))
    cmd=['ffmpeg','-y','-v','error','-i',str(base/'generated/animatic/A-Right-Little-Something-opening-motion-v03.mp4')]
    filters=[f'[0:v]trim=start_frame={start-1}:end_frame={shots[0]["startFrame"]-1},setpts=PTS-STARTPTS,scale=960:540,setsar=1[v0]']
    for i,s in enumerate(shots,1):
        cmd+=['-i',str(out/(s['id']+'-handles.mp4'))]
        lead=s['handles']['leadInFrames']
        filters.append(f'[{i}:v]trim=start_frame={lead}:end_frame={lead+s["frames"]},setpts=PTS-STARTPTS,scale=960:540,setsar=1[v{i}]')
    filters.append(''.join(f'[v{i}]' for i in range(len(shots)+1))+f'concat=n={len(shots)+1}:v=1:a=0[v]')
    filters.append(f'[0:a]atrim=start={(start-1)/fps}:end={(end-1)/fps},asetpts=PTS-STARTPTS[a]')
    run(cmd+['-filter_complex',';'.join(filters),'-map','[v]','-map','[a]','-c:v','libx264','-crf','20','-c:a','aac','-frames:v',str(end-start),'-movflags','+faststart',str(out/'blocking-no-lyrics.mp4')])
    data=copy.deepcopy(json.loads((base/'generated/animatic/animatic-data.json').read_text(encoding='utf-8')))
    data['phrases']=[p for p in data['phrases'] if shots[0]['startFrame']<=p['startFrame']<end]
    for p in data['phrases']:
        for item in [p]+p['words']:
            item['startFrame']-=start-1;item['endFrameExclusive']-=start-1
    write_lyrics(data,project['production']['lyricPresentation'],out/'lyrics.ass')
    subtitle_filter="ass='"+str(out/'lyrics.ass').replace('\\','/').replace(':','\\:')+"'"
    run(['ffmpeg','-y','-v','error','-i',str(out/'blocking-no-lyrics.mp4'),'-vf',subtitle_filter,'-c:v','libx264','-crf','20','-c:a','copy','-movflags','+faststart',str(out/'space-notes-review.mp4')])
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(out/'space-notes-review.mp4')]))['streams'][0]
    assert int(probe['nb_frames'])==end-start and probe['r_frame_rate']=='24/1'
    esc=html.escape;cards=[]
    for s in shots:
        illustrations=''
        if s.get('illustratedStates'):
            illustrations='<h3>ImageGen scale states · appearance draft</h3><div class="frames">'+''.join(
                f'<figure><img src="../hologram-v01/{pathlib.Path(i["image"]).name}"><figcaption>{esc(i["id"])}</figcaption></figure>' for i in s['illustratedStates'])+'</div><p><a href="../hologram-v01/">Compare larger images</a> · three held references, not animated zooms.</p>'
        cards.append(f'''<article id="{s['id']}"><h2>{esc(s['title'])}</h2><p class="time">{esc(s['start'])} → {esc(s['end'])} · song frames {s['startFrame']}–{s['endFrameExclusive']-1} · {s['frames']/fps:.2f}s</p>
<p class="lyric">{esc(' / '.join(s['lyrics']))}</p>{illustrations}<div class="frames"><figure><img src="{s['id']}-edit-in.png"><figcaption>Beginning composition</figcaption></figure><figure><img src="{s['id']}-edit-out.png"><figcaption>Ending composition</figcaption></figure></div>
<p>{esc(s['description'])}</p><p><b>Transition:</b> {esc(s['blocking']['transition'])}</p><p><b>Build:</b> {esc(s['generationApproach'])}</p>
<button data-time="{(s['startFrame']-start)/fps}">Review this beat</button><details><summary>Your original note</summary><p>{esc(s['sourceNoteText'])}</p></details></article>''')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Space notes · proposed continuation</title>
<style>:root{color-scheme:dark}body{background:#10262d;color:#eee2c6;font:16px/1.5 system-ui;margin:0}main{max-width:1150px;margin:auto;padding:24px}h1{font-size:26px}h2{font-size:20px}a{color:#9cd9e5}nav{display:flex;flex-wrap:wrap;gap:18px}article{padding:20px;margin:20px 0;background:#19353d;border:1px solid #45636a;border-radius:8px}.frames{display:flex;gap:12px}figure{margin:0;flex:1;min-width:0}img,video{width:100%;background:#07151a}figcaption,.time{color:#a7c3c8;font-size:13px}.lyric{color:#b6edf6}button{background:#315563;border:1px solid #789eaa;color:white;padding:9px;cursor:pointer}details p{white-space:pre-wrap}@media(max-width:700px){.frames{display:block}}</style>
<main><h1>World below → map → longing → window → eyes</h1><nav><a href="/">Animatic & notes</a><a href="space-notes-v01.blend" download>Editable Blender blocking</a>'''
    page+=''.join(f'<a href="#{s["id"]}">{esc(s["title"])}</a>' for s in shots)
    page+='''</nav><p>Proposed continuation · five note beats, four edit shots. The reaction and approach to the boundary are one continuous take. Frame 581 revises the end of the existing window shot. The full animatic now includes these Blender proposals for review; the accepted v03 movie remains available.</p>
<video id="preview" controls preload="metadata" poster="space-006-edit-in.png" src="space-notes-review.mp4"></video><p class="time">Song 22.583–37.958 seconds · 369 frames at 24fps · first 38 frames are accepted opening context. Rough proxies show composition and camera travel; they do not represent Harper’s final acting or appearance.</p>
<p>The map is currently a layout proxy. Its planet → system → local-stars animation and invented labels are the next effect to build. The face close-up is a framing proxy; eye reflections and performance belong in the illustrated pass.</p>'''
    page+=''.join(cards)
    page+='''<p>All generated sources retain 12-frame lead-in and lead-out. The map holds through the gap after “space”; the close-up stops at “Stretch your arms wide.” No direction beyond that boundary is assumed.</p></main>
<script>const v=document.getElementById('preview');for(const b of document.querySelectorAll('button[data-time]'))b.onclick=()=>{v.currentTime=Number(b.dataset.time);v.play();v.scrollIntoView({block:'center',behavior:'smooth'})};document.addEventListener('keydown',e=>{if(e.code==='Space'&&!e.repeat&&!/INPUT|TEXTAREA|BUTTON|VIDEO/.test(e.target.tagName)){e.preventDefault();v.paused?v.play():v.pause()}})</script></html>'''
    (out/'index.html').write_text(page,encoding='utf-8')
    print('Review ready:',out/'index.html')


if __name__=='__main__':
    main()
