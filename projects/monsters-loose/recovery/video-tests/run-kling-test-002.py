import json, subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
out = root / 'KLING-TEST-002'
out.mkdir(exist_ok=True)
receipt = out / 'submission.json'
if receipt.exists():
    raise SystemExit('Submission receipt exists; query it rather than resubmitting.')
prompt = '''Single continuous five-second illustrated shot. The red-haired zookeeper Harper <<<321495363652188>>> is the woman on the left of the starting image. Preserve her identity using the bound Element. She confidently shows off her lasso to the skeptical boy on the right: with small controlled circular movements of her raised right wrist, she swings the existing open rope loop through two smooth rotations beside and above herself. The loop stays physically connected to the rope in her right hand, with plausible tension, gravity and continuous rope length; her left hand retains the spare coils at her waist. She shifts her weight slightly and gives the boy a knowing smile. The boy stays in place hugging his sketchbook, rolls his eyes once and lifts one eyebrow, unimpressed. The rope remains well clear of him. The camera slowly dollies sideways to the right while gently pulling back, maintaining both full figures and the complete rope loop in frame. Show visible natural parallax between foreground fences, the characters and the distant laboratory. Preserve the richly inked retro 1960s monster-comic drawing, crosshatching and restrained halftone throughout, with teal moonlit shadows, amber lamps and rough matte paving. Preserve the characters' costumes, faces and scale, enclosure geography and signage. No cuts, dialogue, singing, live-action transformation, glossy 3D, extra limbs, duplicated rope loops or new characters. The background is a solid environment revealed by the moving camera, not a flat image sliding behind the characters.'''
args = ['image_to_video', '--image', str(root.parent/'assets'/'ANCH-006-B-v001.png'), '--model', 'kling-video-v3_0', '--duration', '5', '--resolution', '1080p', '--imageCount', '1', '--enable_audio', 'false', '--prefer_multi_shots', 'false', '--elements', json.dumps([{'id':'321495363652188','bindName':'Harper'}]), prompt]
(out/'request.json').write_text(json.dumps({'source':'ANCH-006-B/v001','element':'321495363652188','expected_credits':40,'cli_args':args},indent=2),encoding='utf-8')
(out/'prompt.txt').write_text(prompt,encoding='utf-8')
# Use node directly so Windows shell quoting cannot alter the Element JSON.
result = subprocess.run(['C:/Program Files/nodejs/node.exe','C:/Users/arneg/AppData/Roaming/npm/node_modules/@klingai/cli-global/dist/cli.js',*args],capture_output=True,text=True,encoding='utf-8')
receipt.write_text(result.stdout,encoding='utf-8')
(out/'submission-stderr.txt').write_text(result.stderr,encoding='utf-8')
print(result.stdout)
print('Exit:', result.returncode)
