"""Measure guided luminous points and make editable foreground holdout plates.

Runs with the project Python/Pillow. No network or video generation. Tracks only
visible display lights near hand-authored guides, not the background star field.
"""
import argparse
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageChops, ImageDraw, ImageFilter


def interpolate(keys, frame):
    if frame <= keys[0][0]:
        return keys[0][1:]
    for left, right in zip(keys, keys[1:]):
        if frame <= right[0]:
            t = (frame-left[0])/(right[0]-left[0])
            return [a+(b-a)*t for a, b in zip(left[1:], right[1:])]
    return keys[-1][1:]


def measure(image, expected, radius, color):
    x, y = expected
    pixels = image.load()
    candidates = []
    for py in range(max(0, round(y)-radius), min(image.height, round(y)+radius+1)):
        for px in range(max(0, round(x)-radius), min(image.width, round(x)+radius+1)):
            if (px-x)**2+(py-y)**2 > radius**2:
                continue
            r, g, b = pixels[px, py]
            strength = min(g, b)-r*.45 if color == 'cyan' else min(r, g)-b*.45
            if strength > 85 and (max(r, g, b) > 165):
                candidates.append((px, py, strength))
    if not candidates:
        return [x, y], False, 0
    # Use the compact luminous core, rather than a centroid of adjoining beams.
    peak = max(candidates, key=lambda p: p[2]-.025*((p[0]-x)**2+(p[1]-y)**2))
    core = [(px, py, w) for px, py, w in candidates if (px-peak[0])**2+(py-peak[1])**2 < 36]
    total = sum(w*w for _, _, w in core)
    centre = [sum(p[i]*p[2]**2 for p in core)/total for i in (0, 1)]
    return centre, True, math.dist(centre, expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    args = parser.parse_args()
    project = args.plan.resolve().parent
    plan = json.loads(args.plan.read_text())
    register = json.loads((project/'shots/shotlist.json').read_text(encoding='utf-8'))
    shot = next(s for s in register['storyboardProposals'] if s['id'] == plan['shotId'])
    fps = register.get('fps', 24)
    dest = project/plan['output']
    source_dir = dest/'source'
    source_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(project/plan['source']),
        '-vf', f'fps={fps},pad={plan["width"]}:{plan["height"]}:2:0,setsar=1',
        '-frames:v', str(plan['sourceFrames']), str(source_dir/'frame_%04d.png')], check=True)
    measured = {s['id']: [] for s in plan['systems']}
    mask_dir = dest/'holdout'
    mask_dir.mkdir(exist_ok=True)
    tint_dir = dest/'star-tint'
    if plan.get('tintSourceStarCores'):
        tint_dir.mkdir(exist_ok=True)
    guides_used = 0
    errors = []
    for frame in range(plan['renderStartFrame'], plan['sourceFrames']+1):
        image = Image.open(source_dir/f'frame_{frame:04d}.png').convert('RGB')
        for system in plan['systems']:
            expected = interpolate(system['guides'], frame)
            if frame >= system['birthFrame']:
                centre, found, error = measure(image, expected, system['searchRadiusPx'], system['trackingColor'])
                guides_used += not found
                if found:
                    errors.append(error)
            else:
                centre, found = expected, False
            measured[system['id']].append({'frame': frame, 'pixel': centre, 'measured': found})
        matte = Image.new('L', image.size)
        draw = ImageDraw.Draw(matte)
        for holdout in plan['holdouts']:
            keys = [[k['frame'], *[v for p in k['points'] for v in p]] for k in holdout['keys']]
            coords = interpolate(keys, frame)
            draw.polygon(list(zip(coords[::2], coords[1::2])), fill=255)
        soft_matte=matte.filter(ImageFilter.GaussianBlur(plan['composite']['matteFeatherPx']))
        soft_matte.save(mask_dir/f'frame_{frame:04d}.png')
        if plan.get('tintSourceStarCores'):
            tint=Image.new('RGB',image.size,'white')
            visible=ImageChops.invert(soft_matte)
            for system in plan['systems']:
                t=max(0,min(1,(frame-system['birthFrame'])/system['unfoldFrames']))
                if not t:
                    continue
                x,y=measured[system['id']][-1]['pixel']
                radius=system.get('starSizePx',3.5)*1.4+3
                spot=Image.new('L',image.size)
                ImageDraw.Draw(spot).ellipse((x-radius,y-radius,x+radius,y+radius),fill=round(255*t*t*(3-2*t)))
                spot=ImageChops.multiply(spot.filter(ImageFilter.GaussianBlur(radius*.23)),visible)
                color=tuple(round(255*max(.06,c)) for c in system['displayColor'])
                tint.paste(color,(0,0,image.width,image.height),spot)
            tint.save(tint_dir/f'frame_{frame:04d}.png')
        if frame in (101, 113, 125, 144):
            overlay = Image.new('RGBA', image.size)
            marks = ImageDraw.Draw(overlay)
            marks.bitmap((0, 0), matte, fill=(255, 50, 85, 75))
            for system in plan['systems']:
                if frame >= system['birthFrame']:
                    x, y = measured[system['id']][-1]['pixel']
                    marks.ellipse((x-7, y-7, x+7, y+7), outline=(120,255,220), width=2)
                    marks.text((x+9, y), system['id'], fill='white')
            Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB').save(dest/f'tracking-{frame:04d}.png')
    data = {'fps': fps, 'songStartFrame': shot['startFrame'], 'editFrames': shot['frames'],
        'leadInFrames': shot['handles']['leadInFrames'], 'sourceFrames': plan['sourceFrames'],
        'systems': measured, 'tracking': {'method': 'Guided color-core centroid per source frame',
        'guideFallbacks': guides_used, 'meanGuideCorrectionPx': sum(errors)/len(errors),
        'maxGuideCorrectionPx': max(errors), 'depth': plan['depthMethod'],
        'matte': 'Interpolated hand-authored foreground polygon; coarse experiment, not a finished roto'}}
    (dest/'tracking.json').write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(data['tracking'], indent=2))


if __name__ == '__main__':
    main()
