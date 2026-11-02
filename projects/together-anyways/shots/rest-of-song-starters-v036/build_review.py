"""Build the local review board without changing the active edit."""
from pathlib import Path
import json
import html

PROJECT = Path(__file__).resolve().parents[2]
NOTES = Path(__file__).resolve().parent
OUT = PROJECT / 'generated/storyboard/rest-of-song-starters-v036'
proposal = json.loads((PROJECT / 'shots/rest-of-song-v024/proposal.json').read_text())
scene_names = {s['id']: s['name'] for s in proposal['scenes']}
shots = []
for item in proposal['shots']:
    row = dict(item)
    row['sceneName'] = scene_names[row['sceneId']]
    row['starterImage'] = f"generated/storyboard/rest-of-song-starters-v036/{row['id']}.png"
    row['imageUrl'] = f"../{row['id']}.png"
    row['status'] = 'generated_pending_user_review' if (PROJECT / row['starterImage']).is_file() else 'generating'
    row['reviewNote'] = {'S09-SH02': 'The original cartridge reads larger than the nominal prop reference; review its scale across the repair sequence.', 'S14-SH03': 'Correct entry position retained, but the large intake shows warm interior light and reads like a second doorway. Correct that duct before motion.', 'S14-SH01': 'The closed-hatch correction also flattened the visible intake recess. Review ship geometry before motion generation.'}.get(row['id'], '')
    row['referenceFrameMode'] = 'start'
    row['videoHandles'] = {'fps': 24, 'inFrames': 24, 'outFrames': 24, 'requestedSourceFrames': row['frames'] + 48}
    shots.append(row)
manifest = {'version': 'v036', 'status': 'starter_frames_for_review', 'fps': 24,
            'note': 'Approved story direction, new stills pending review. Existing shotlist remains active edit authority. No video generation or animatic change.',
            'scenes': proposal['scenes'], 'shots': shots}
(NOTES / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
ready = sum(s['status'] != 'generating' for s in shots)
sections = []
for scene in proposal['scenes']:
    cards = []
    for i, shot in enumerate(shots):
        if shot['sceneId'] != scene['id']:
            continue
        content = f'<img loading="lazy" src="{shot["imageUrl"]}" alt="{html.escape(shot["id"]+" "+shot["title"])}">' if shot['status'] != 'generating' else '<div class="pending">Generating</div>'
        cards.append(f'<button class="card" data-i="{i}">{content}<span><b>{shot["id"]}</b> · {shot["frames"]/24:.2f}s<br>{html.escape(shot["title"])}</span></button>')
    sections.append(f'<section id="{scene["id"]}"><h2>{scene["id"]} · {html.escape(scene["name"])}</h2><p>{html.escape(scene["purpose"])}</p><div class="grid">'+''.join(cards)+'</div></section>')
nav = ''.join(f'<a href="#{s["id"]}">{s["id"]}</a>' for s in proposal['scenes'])
page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Together Anyways · remaining-story starters</title><style>
*{box-sizing:border-box}body{margin:0;background:#151918;color:#eeeae2;font:16px system-ui}header{padding:22px 4vw;border-bottom:1px solid #44534e}header p{color:#c6c7bd}h1{margin:0;font-size:27px}nav{position:sticky;top:0;z-index:3;display:flex;gap:12px;padding:12px 4vw;background:#202725;box-shadow:0 2px 8px #0006}a{color:#a8d7cb}main{padding:0 4vw 50px}section{scroll-margin-top:65px;margin:32px 0 50px}section>p{color:#b8c5bf;max-width:1000px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:18px}.card{padding:0;text-align:left;cursor:pointer;color:inherit;background:#242d29;border:1px solid #40534b;border-radius:6px;overflow:hidden;font:inherit}.card:hover,.card:focus-visible{outline:2px solid #eac480}.card img,.pending{width:100%;aspect-ratio:16/9;object-fit:contain;background:#080b0a;display:block}.card span{display:block;padding:13px;line-height:1.5}.pending{display:grid;place-items:center;color:#b4b9b3}dialog{padding:0;background:#101412;color:#eee;border:1px solid #6b8177;width:min(1500px,98vw);max-height:97vh}dialog::backdrop{background:#000d}.bar{display:flex;align-items:center;gap:12px;padding:12px 16px;flex-wrap:wrap}.bar button{background:#35473f;color:#fff;border:1px solid #657e71;padding:9px 14px;border-radius:4px;font:inherit;cursor:pointer}#image{display:block;width:100%;max-height:70vh;object-fit:contain;background:#000}#details{padding:4px 20px 18px;line-height:1.5;max-width:1250px}#details p{margin:7px 0}#position{margin-left:auto}.muted{color:#adc3b7}#clean{margin-left:12px}@media(max-width:500px){.grid{grid-template-columns:1fr}h1{font-size:22px}}</style></head><body><header><h1>Together Anyways · Scenes 7–14</h1><p>READY / 38 clean starter frames · v036 · Click a frame to review. Use ← / → to compare adjacent shots.</p><p>Each frame sets up the next action. Timings and lyric indexes are retained; these stills have not replaced the active animatic.</p></header><nav>NAV</nav><main>SECTIONS</main><dialog id="viewer"><div class="bar"><button id="prev" aria-label="Previous shot">← Previous</button><button id="next" aria-label="Next shot">Next →</button><strong id="title"></strong><span id="position"></span><button id="close">Close</button></div><img id="image" alt=""><div id="details"></div></dialog><script>
const shots=DATA; let index=0; const viewer=document.getElementById('viewer');
function time(frame){const sec=frame/24;return Math.floor(sec/60)+':'+(sec%60).toFixed(3).padStart(6,'0')}
function show(i){index=Math.max(0,Math.min(shots.length-1,i));const s=shots[index];document.getElementById('image').src=s.imageUrl;document.getElementById('image').alt=s.id+' '+s.title;document.getElementById('title').textContent=s.id+' · '+s.title;document.getElementById('position').textContent=(index+1)+' / '+shots.length;const d=document.getElementById('details');d.replaceChildren();for(const text of [s.sceneName+' · '+time(s.startFrame)+'–'+time(s.endFrameExclusive)+' · '+s.frames+' frames / '+(s.frames/24).toFixed(3)+' seconds · '+s.indexes.join(', '),'Planned action: '+s.action]){const p=document.createElement('p');p.textContent=text;d.append(p)}if(s.reviewNote){const p=document.createElement('p');p.textContent='Review note: '+s.reviewNote;p.style.color='#edc584';d.append(p)}const a=document.createElement('a');a.href=s.imageUrl;a.target='_blank';a.textContent='Open clean full-resolution frame';d.append(a);document.getElementById('prev').disabled=index===0;document.getElementById('next').disabled=index===shots.length-1;if(!viewer.open)viewer.showModal();history.replaceState(null,'','#'+s.id)}
document.querySelectorAll('.card').forEach(el=>el.addEventListener('click',()=>show(Number(el.dataset.i))));document.getElementById('prev').onclick=()=>show(index-1);document.getElementById('next').onclick=()=>show(index+1);document.getElementById('close').onclick=()=>viewer.close();document.addEventListener('keydown',e=>{if(!viewer.open)return;if(e.key==='ArrowRight'){e.preventDefault();show(index+1)}if(e.key==='ArrowLeft'){e.preventDefault();show(index-1)}});const initial=shots.findIndex(s=>'#'+s.id===location.hash);if(initial>=0)show(initial);
</script></body></html>'''
page = page.replace('READY',str(ready)).replace('NAV',nav).replace('SECTIONS',''.join(sections)).replace('DATA',json.dumps(shots).replace('</','<\\/'))
(OUT / 'review').mkdir(exist_ok=True)
(OUT / 'review/shot-board.html').write_text(page)
print(f'{ready}/38 ready; review and manifest updated')
