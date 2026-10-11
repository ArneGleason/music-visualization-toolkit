"""Extract labelled native frames to inspect both approved ejection takes."""
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw

OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
plan=json.loads((PROJECT/'kling-escape-ejection-v01.json').read_text(encoding='utf-8'))
target=PROJECT/'generated/storyboard/escape-ejection-motion-v01'
target.mkdir(parents=True,exist_ok=True)
for take in plan['shots']:
    folder=PROJECT/plan['output']/take['id']
    native=next(folder.glob('*-clean.mp4'),None) or next(folder.glob('*.mp4'),None)
    if native is None:
        print(take['shotId'],'not collected yet')
        continue
    frames=[25,61,85,109,137,169] if take['shotId']=='escape-001' else [25,37,61,85,109,121]
    sheet=Image.new('RGB',(1920,784),(20,24,30))
    draw=ImageDraw.Draw(sheet)
    for index,frame in enumerate(frames):
        png=target/f"{take['shotId']}-source-{frame:03}.png"
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(native),'-vf',
            f'select=eq(n\\,{frame-1}),setpts=PTS-STARTPTS','-frames:v','1',str(png)],check=True)
        with Image.open(png) as picture:
            picture=picture.convert('RGB').resize((640,360))
            x,y=(index%3)*640,(index//3)*392
            sheet.paste(picture,(x,y))
            draw.text((x+12,y+365),f"{take['shotId']} source {frame} / {(frame-1)/24:.2f}s",fill='white')
    sheet.save(target/(take['shotId']+'-native-samples.jpg'),quality=95)
    print('Sampled',take['shotId'])
