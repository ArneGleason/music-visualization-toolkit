"""Two static-image auditions with identical edit and unchanged face timing."""
from pathlib import Path
import subprocess
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'out/opening_need_aerial_v1'

def run(args):
    subprocess.run([str(x) for x in args], cwd=ROOT, check=True)

template = (SOURCE / 'render.py').read_text()
for label in ('a', 'b'):
    folder = ROOT / f'out/opening_need_static_{label}_v1'
    folder.mkdir(exist_ok=True)
    image = SOURCE / 'first_frame.png' if label == 'a' else OUT / 'horizon.png'
    code = template.replace("ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent", f"ROOT=Path({str(ROOT)!r});OUT=Path({str(folder)!r})")
    start = code.index('lock=')
    end = code.index('edl=json.loads')
    code = code[:start] + f"run(['ffmpeg','-v','error','-y','-loop','1','-framerate','24','-i',{str(image)!r},'-vf','scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1','-frames:v','42','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'clean.mp4'])\n" + code[end:]
    code = code.replace('opening_need_aerial_v1', folder.name)
    if label == 'a':
        code = code.replace(str(folder / 'first_frame.png').__repr__(), str(image).__repr__())
    code = code.replace('simulated lateral move over new reference still', 'static aerial composition comparison')
    code = code.replace('2D lateral motion over built-in generated aerial still, not Flow footage', 'Static still, no camera movement, composition comparison only')
    exec(compile(code, str(folder / 'render_inherited.py'), 'exec'), {'__file__': str(folder / 'render_inherited.py'), '__name__': '__main__'})

# Consecutive full-phrase A then B, not split-screen, to preserve viewing scale.
run(['ffmpeg','-v','error','-y','-i',ROOT/'out/opening_need_static_a_v1/preview.mp4','-i',ROOT/'out/opening_need_static_b_v1/preview.mp4','-filter_complex','[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]','-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'compare.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'compare.mp4','-f','null','-'])
info = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(OUT/'compare.mp4')]))['streams'][0]
assert int(info['nb_frames']) == 358 and info['r_frame_rate'] == '24/1', info
(OUT/'verification.json').write_text(json.dumps({'frames':358,'fps':24,'order':['A original aerial','B horizon aerial'],'cutaway_song_frames':[183,225],'each_preview_song_frames':[155,334],'camera_motion':'none in either comparison','face_source_clock':'unchanged','owner_approval':'pending'},indent=2))
