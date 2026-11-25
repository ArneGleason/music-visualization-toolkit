"""Make labelled reference comparisons from retained Together Anyways sources."""
import json
import html
import os
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE.parent / 'together-anyways'
OUT = BASE / 'generated/wip/previews/face-reference-mining/v002'
IDS = ['ta-002', 'ta-004b', 'ta-006', 'ta-010',
       'ta-014', 'ta-017', 'ta-017b', 'ta-024',
       'S08-SH01', 'S09-SH03', 'S09-SH04', 'S11-SH03B',
       'S11-SH04', 'S12-SH02', 'S12-SH07B', 'S14-SH02']


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shots = json.loads((SOURCE / 'shots/shotlist.json').read_text())['shots']
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 22)
    register = []
    for index, shot_id in enumerate(IDS, 1):
        shot = next(s for s in shots if s['id'] == shot_id)
        frame = shot['videoEdit']['sourceInFrame'] + shot['frames']//2
        target = OUT / f'{shot_id}-motion.png'
        subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
                        '-i', str(SOURCE / shot['videoSource']), '-vf',
                        f'select=eq(n\\,{frame})', '-frames:v', '1', str(target)], check=True)
        early = shot['videoEdit']['sourceInFrame']
        subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error',
                        '-i', str(SOURCE / shot['videoSource']), '-vf',
                        f'select=eq(n\\,{early})', '-frames:v', '1', str(OUT / f'{shot_id}-early.png')], check=True)
        register.append({'index': f'{index:02}', 'id': shot_id, 'title': shot['title'],
                         'starter': str(Path('../together-anyways') / shot['starterImage']),
                         'video': str(Path('../together-anyways') / shot['videoSource']),
                         'sourceFrame': frame, 'earlySourceFrame': early,
                         'status': 'unranked_candidate_not_selected'})
    for mode in ['starter', 'motion']:
        for page in range(4):
            sheet = Image.new('RGB', (1440, 900), '#15212a')
            draw = ImageDraw.Draw(sheet)
            for cell, entry in enumerate(register[page*4:page*4+4]):
                x, y = (cell % 2)*720, (cell//2)*450
                path = BASE / entry['starter'] if mode == 'starter' else OUT / f"{entry['id']}-motion.png"
                with Image.open(path) as source:
                    picture = ImageOps.contain(source.convert('RGB'), (704, 396))
                    sheet.paste(picture, (x+8+(704-picture.width)//2, y+8+(396-picture.height)//2))
                suffix = 'A / starter' if mode == 'starter' else f"C / motion frame {entry['sourceFrame']}"
                draw.text((x+12, y+410), f"{entry['index']}{suffix} | {entry['id']} | {entry['title'][:29]}", font=font, fill='#f3e8d2')
            sheet.save(OUT / f'{mode}-page-{page+1}.jpg', quality=94)
    register_path = BASE / 'production/face-reference-candidates-v002.json'
    register_path.write_text(json.dumps(register, indent=2)+'\n')
    sections = []
    for entry in register:
        cards = []
        for suffix, label, path in [
            ('A', 'Original starter', BASE / entry['starter']),
            ('B', f"First selected motion frame {entry['earlySourceFrame']}", OUT / f"{entry['id']}-early.png"),
            ('C', f"Mid-edit motion frame {entry['sourceFrame']}", OUT / f"{entry['id']}-motion.png")]:
            url = html.escape(os.path.relpath(path, OUT), quote=True)
            cards.append(f'<figure><a href="{url}"><img src="{url}" loading="lazy"></a><figcaption><b>{entry["index"]}{suffix}</b> — {label}</figcaption></figure>')
        video = html.escape(os.path.relpath(BASE / entry['video'], OUT), quote=True)
        sections.append(f'<section id="shot-{entry["index"]}"><h2>{entry["index"]} · {html.escape(entry["title"])} <small>{entry["id"]}</small></h2><div class="row">'+''.join(cards)+f'</div><a href="{video}">Open original source clip</a></section>')
    page = '''<!doctype html><meta charset="utf-8"><title>Harper and Taffy reference index</title>
<style>body{background:#14212b;color:#f1e8d6;font:18px system-ui;margin:32px}h1{font-size:32px}small{color:#bac6cc;font-size:16px}a{color:#e9bc70}.row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}figure{margin:0}img{width:100%;height:auto}figcaption{padding:8px 0}section{padding:20px 0;border-bottom:1px solid #53616b}@media(max-width:900px){.row{grid-template-columns:1fr}}</style>
<h1>Harper &amp; Taffy — reference selection index</h1>
<p>16 unranked close / medium character setups. Pick exact image IDs, for example: Harper 08A, Taffy 07B. Click any image for full resolution.</p>
<p>A = original starter · B = first frame selected in the old edit · C = midpoint of that edit. These are samples, not quality approvals; faces may be obscured in some motion frames.</p>
'''+''.join(sections)
    (OUT / 'index.html').write_text(page)
    (OUT / '.disposable').write_text('Reproduce from retained original starter images and MP4s:\n./.venv/bin/python3 projects/open-up-the-secret-room/production/mine_face_references.py\n')
    print(OUT)


if __name__ == '__main__':
    main()
