from pathlib import Path
import json,html
P=Path(__file__).resolve().parents[2];N=Path(__file__).resolve().parent;O=P/'generated/kling-scene06-v042'
d=json.loads((N/'batch.json').read_text());cards=[]
active={s['id']:s for s in json.loads((P/'shots/shotlist.json').read_text())['shots']}
for s in d['shots']:
 s=dict(s)
 current=active[s['shotId']]
 s['sourceInFrame']=current['videoEdit']['sourceInFrame']
 s['editFrames']=current['frames']
 cards.append(f'<section><h2>{s["displayId"]}</h2><video controls loop preload="metadata" src="{s["shotId"]}.mp4"></video><p>Source in: {s["sourceInFrame"]/24:.3f}s · Edit: {s["editFrames"]} frames / {s["editFrames"]/24:.3f}s</p><details><summary>Direction</summary><p>{html.escape(s["prompt"])}</p></details></section>')
(O/'review.html').write_text('<!doctype html><html><meta charset="utf-8"><title>Scene6 motion review</title><style>body{font:17px system-ui;background:#17201c;color:#eee;margin:30px}main{display:grid;grid-template-columns:1fr 1fr;gap:24px}video{width:100%}p{white-space:pre-wrap}a{color:#9ed7ca}</style><h1>Scene6 · News and recognition</h1><a href="http://127.0.0.1:8767/">Full-song animatic</a><main>'+''.join(cards)+'</main></html>')
