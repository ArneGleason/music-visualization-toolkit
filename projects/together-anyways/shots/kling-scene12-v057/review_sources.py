"""Build labeled half-second contact sheets for downloaded Scene 12 sources."""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

project = Path(__file__).resolve().parents[2]
output = project / 'generated/kling-scene12-v057'
for video in sorted(output.glob('S12-*.mp4')):
    dest = output / (video.stem + '-contact.jpg')
    if dest.exists():
        continue
    frames = output / (video.stem + '-frames')
    frames.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-vf',
                    'fps=2,scale=480:-1', str(frames / '%03d.jpg')], check=True)
    files = sorted(frames.glob('*.jpg'))
    board = Image.new('RGB', (1920, 300*((len(files)+3)//4)), '#18221e')
    draw = ImageDraw.Draw(board)
    for i, path in enumerate(files):
        x, y = i%4*480, i//4*300
        board.paste(Image.open(path), (x,y+25))
        draw.text((x+8,y+5), f'{video.stem} source ~{i/2:.1f}s', fill='white')
    board.save(dest)
    print(dest)
