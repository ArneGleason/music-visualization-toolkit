"""Check that only the intended overlap frames were changed before encoding."""
import json
from pathlib import Path
import subprocess
from PIL import Image

OUT=Path(__file__).resolve().parent
manifest=json.loads((OUT/'timing-check.json').read_text())
expected={f-2873+1 for t in manifest['transitions'] for f in range(t['startFrame'],t['startFrame']+t['frames'])}
source=OUT.with_name('departure-discovery-motion-v01')/'zoom-stills.mp4'
process=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
changed=[]
for frame in range(1,74):
    raw=process.stdout.read(1920*1080*3)
    assert len(raw)==1920*1080*3
    if raw != Image.open(OUT/'frames'/f'{frame:03d}.png').convert('RGB').tobytes():
        changed.append(frame)
assert not process.stdout.read(1)
assert process.wait()==0
assert set(changed)==expected,(changed,expected)
manifest['pixelCheck']=dict(expectedChangedFrames=sorted(expected),actualChangedFrames=changed,
    unchangedFrames=73-len(changed),result='All 59 non-transition frames identical before encoding')
(OUT/'timing-check.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Verified: exactly 14 transition frames changed; 59 other frames pixel-identical before encoding.')
