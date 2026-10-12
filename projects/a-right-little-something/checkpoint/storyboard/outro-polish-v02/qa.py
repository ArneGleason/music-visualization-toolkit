"""Check V65 timing and sample the assembled edit for visual review."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageStat

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

before = read(OUT/'prior-shotlist.json')
after = read(BASE/'shots/shotlist.json')
old = {s['id']: s for s in before['storyboardProposals']}
new = {s['id']: s for s in after['storyboardProposals']}
timing_keys = ['startFrame', 'endFrameExclusive', 'frames']
for sid, shot in old.items():
    placement = shot.get('animaticPlacement', {})
    for key in timing_keys:
        assert placement.get(key) == new[sid].get('animaticPlacement', {}).get(key), (sid, key)
assert old['contact-028-travel']['motionSelection'] == new['contact-028-travel']['motionSelection']

# Sample visible foreground interiors, avoiding silhouettes and glass. The
# keyed alpha can retain slight transparency, so the background may contribute
# small pixel differences even though the foreground graph is unchanged.
original = Image.open(OUT.parent/'first-contact-motion-v02/travel-frames/frame_0017.png').convert('RGB')
revised = Image.open(OUT/'travel-frames/frame_0017.png').convert('RGB')
regions = {'Harper suit': (884, 448, 920, 480),
           'Harper face': (950, 410, 967, 427),
           'Ship hull': (800, 630, 880, 660),
           'Engine core': (440, 600, 452, 622)}
pixel_checks = {}
for name, box in regions.items():
    delta = ImageChops.difference(original.crop(box), revised.crop(box))
    pixel_checks[name] = {'maxDifference': max(v[1] for v in delta.getextrema()),
                          'meanDifference': ImageStat.Stat(delta).mean}

movie = BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v65.mp4'
frames = [3173, 4446, 4483, 4567, 4620, 4666, 4764, 5035, 5137, 5161, 5185, 5210, 5265]
samples = OUT/'assembled-qa'
samples.mkdir(exist_ok=True)
select = '+'.join(f'eq(n,{f-1})' for f in frames)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-reinit_filter', '0', '-i', str(movie),
                '-vf', 'select='+select.replace(',', r'\,'), '-fps_mode', 'vfr',
                '-pix_fmt', 'yuvj420p', '-color_range', 'pc', '-q:v', '2',
                str(samples/'sample-%02d.jpg')], check=True)
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 19)
sheet = Image.new('RGB', (1280, ((len(frames)+1)//2)*390), (14,24,32))
draw = ImageDraw.Draw(sheet)
for i, frame in enumerate(frames):
    path = samples/f'sample-{i+1:02d}.jpg'
    image = Image.open(path)
    image.thumbnail((640,360))
    x, y = (i%2)*640, (i//2)*390
    sheet.paste(image, (x,y+30))
    draw.text((x+10,y+4), f'Frame {frame} / {(frame-1)/24:.3f}s', font=font, fill='white')
sheet.save(OUT/'v65-assembled-contact-sheet.jpg', quality=92)
record = {'timelineComparedToV64': 'All storyboard placement boundaries identical',
          'reversedTravel28': 'Exact V64 selection preserved',
          'foregroundInteriorPixelChecks': pixel_checks,
          'assembledSampleFrames': frames,
          'visualReview': 'Pending inspection of contact sheet and final title'}
(OUT/'qa-observations.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record, indent=2))
