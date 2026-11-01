"""Build calibrated cast reference plates and a common-scale lineup from a register."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PAPER = '#f6f1e8'
INK = '#293d3e'
ACCENT = '#9b5035'


def font(project, size):
    return ImageFont.truetype(str(project / 'generated/animatic/assets/BarlowSemiCondensed-SemiBold.ttf'), size)


def artwork(project, row, pixels_per_cm):
    image = Image.open(project / row['image']).convert('RGB')
    crown = row['crownY'] * image.height
    ground = row['groundY'] * image.height
    assert 0 <= crown < ground <= image.height
    scale = row['heightCm'] * row['poseFactor'] * pixels_per_cm / (ground - crown)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    return resized, round(ground * scale)


def ruler(draw, project, x, baseline, ppcm, maximum=220):
    draw.line((x, baseline, x, baseline - maximum * ppcm), fill=INK, width=2)
    for cm in range(0, maximum + 1, 10):
        y = round(baseline - cm * ppcm)
        length = 25 if cm % 50 == 0 else 12
        draw.line((x - length, y, x, y), fill=INK, width=2)
        if cm % 50 == 0:
            draw.text((x - 35, y), str(cm), font=font(project, 25), fill=INK, anchor='rm')
    draw.text((x - 20, baseline - maximum * ppcm - 40), 'cm', font=font(project, 26), fill=INK, anchor='mm')


def build(project, register, output):
    rows = register['characters']
    output.mkdir(parents=True, exist_ok=True)
    plates = output / 'plates'
    plates.mkdir(exist_ok=True)
    manifest = []
    for row in rows:
        ppcm, baseline = 6.2, 1630
        art, ground = artwork(project, row, ppcm)
        width = max(1400, art.width + 230)
        footer = max(1700, baseline + art.height - ground + 35)
        plate = Image.new('RGB', (width, footer + 150), PAPER)
        plate.paste(art, (200 + (width - 220 - art.width) // 2, baseline - ground))
        draw = ImageDraw.Draw(plate)
        draw.text((55, 35), f"{row['id']}  /  {row['name']}", font=font(project, 43), fill=INK)
        draw.text((55, 100), f"STANDING HEIGHT  {row['heightCm']} cm  /  PROPOSED", font=font(project, 30), fill=ACCENT)
        ruler(draw, project, 125, baseline, ppcm)
        y = round(baseline - row['heightCm'] * ppcm)
        draw.line((128, y, 185, y), fill=ACCENT, width=4)
        draw.polygon([(185, y), (174, y - 7), (174, y + 7)], fill=ACCENT)
        draw.text((145, y - 18), str(row['heightCm']), font=font(project, 24), fill=ACCENT, anchor='mb')
        draw.line((200, baseline, width - 30, baseline), fill=INK, width=2)
        draw.text((55, footer + 25), 'DESIGN SCALE / Crown excludes hair, headgear and equipment.', font=font(project, 27), fill=INK)
        note = 'Posed stature is approximate; standing-height marker is the design target.'
        if row['poseFactor'] != 1:
            note = f"Lean / stoop allowance: {round((1-row['poseFactor'])*100)}%. Standing height remains {row['heightCm']} cm."
        draw.text((55, footer + 70), note, font=font(project, 26), fill=INK)
        dest = plates / f"{row['id']}-height-reference.png"
        plate.save(dest)
        label = 'new reference' if row.get('newReference') else ('revised' if row['revised'] else 'retained')
        manifest.append({'id': row['id'], 'index': row['id'], 'title': f"{row['name']} · {row['heightCm']} cm proposed · {label}", 'src': f'../plates/{dest.name}', 'href': f'../plates/{dest.name}'})

    # Each rectangular artwork keeps its original background and pixels. Only
    # uniform scaling is used; no automatic masking distorts delicate anatomy.
    ppcm, baseline = 4.0, 1100
    arts = [artwork(project, row, ppcm) for row in rows]
    widths = [max(330, art.width + 18) for art, _ in arts]
    label_y = max(1170, baseline + max(art.height - ground for art, ground in arts) + 45)
    lineup = Image.new('RGB', (sum(widths) + 180, label_y + 150), PAPER)
    draw = ImageDraw.Draw(lineup)
    draw.text((45, 28), register.get('title', 'TOGETHER ANYWAYS / SUPPORTING CAST / HEIGHT & SILHOUETTE STUDY v004'), font=font(project, 42), fill=INK)
    draw.text((45, 90), 'One scale: 4 pixels per cm. Proposed standing heights; posed stature calibrated approximately. Original backgrounds retained.', font=font(project, 28), fill=INK)
    ruler(draw, project, 120, baseline, ppcm)
    x = 160
    for row, (art, ground), width in zip(rows, arts, widths):
        lineup.paste(art, (x + (width - art.width) // 2, baseline - ground))
        draw = ImageDraw.Draw(lineup)
        y = round(baseline - row['heightCm'] * ppcm)
        draw.line((x + 8, y, x + 32, y), fill=ACCENT, width=3)
        draw.text((x + width // 2, label_y), f"{row['id']} / {row['heightCm']} cm", font=font(project, 33), fill=INK, anchor='mm')
        draw.text((x + width // 2, label_y + 50), row['name'], font=font(project, 27), fill=INK, anchor='mm')
        x += width
    draw.line((160, baseline, lineup.width - 20, baseline), fill=INK, width=3)
    lineup.save(output / 'cast-lineup.png')
    preview = lineup.copy()
    preview.thumbnail((2600, 900))
    preview.save(output / 'cast-lineup-preview.png')
    manifest.insert(0, {'id': 'lineup', 'index': 'ALL', 'title': 'Shared-scale lineup · click for full-resolution image', 'src': '../cast-lineup-preview.png', 'href': '../cast-lineup.png'})
    (output / 'review-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    hashes = {r['id']: hashlib.sha256((project / r['image']).read_bytes()).hexdigest() for r in rows}
    (output / 'validation.json').write_text(json.dumps({'portraits': len(rows), 'revised': sum(r['revised'] for r in rows), 'heightRangeCm': [min(r['heightCm'] for r in rows), max(r['heightCm'] for r in rows)], 'sourceHashes': hashes, 'lineupSize': list(lineup.size), 'heightApproval': 'pending', 'calibration': 'manual approximate posed stature'}, indent=2) + '\n')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('register', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--renderer', type=Path, required=True, help='Creative Production review_renderer.py')
    args = parser.parse_args()
    register = json.loads(args.register.read_text())
    manifest = build(args.project, register, args.output)
    spec = importlib.util.spec_from_file_location('review_renderer', args.renderer)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    review = args.output / 'review'
    review.mkdir(exist_ok=True)
    module.build_review_html(review, manifest, {'preset': 'image-wall', 'showCaptions': True, 'showPrompts': False, 'minTileWidth': 330, 'output': 'cast-board.html', 'title': 'Together Anyways · silhouette and height proposals'})
    comparison = []
    for row in register['characters']:
        if not row['revised']:
            continue
        for key, label in [('source', 'previous'), ('image', 'revised')]:
            src = Path(os.path.relpath(args.project / row[key], review)).as_posix()
            comparison.append({'index': row['id'], 'title': f"{row['name']} · {label} artwork (individually framed)", 'src': src, 'href': src})
    module.build_review_html(review, comparison, {'preset': 'image-wall', 'showCaptions': True, 'showPrompts': False, 'minTileWidth': 330, 'output': 'comparison-board.html', 'title': 'Together Anyways · silhouette before and after'})
    print(review / 'cast-board.html')


if __name__ == '__main__':
    main()
