"""Diagnostic contact sheets only, never used as effect inputs."""
from pathlib import Path
import subprocess,json
O=Path(__file__).resolve().parent
for item in json.loads((O/'batch3_previews.json').read_text()):
    count=item['song_frames'][1]-item['song_frames'][0]
    frames=[round(i*(count-1)/7) for i in range(8)]
    select='+'.join(f'eq(n\\,{f})' for f in frames)
    target=O/f"batch3_{item['name']}_contact.jpg"
    if not target.exists():subprocess.run(['ffmpeg','-v','error','-n','-i',item['file'],'-vf',f'select={select},scale=320:180,tile=4x2','-frames:v','1',str(target)],check=True)
print('Diagnostic frame sequences ready.')
