import json, subprocess
from pathlib import Path
root = Path(__file__).resolve().parent
out = root / 'KLING-TEST-003'
receipt = out / 'submission.json'
if receipt.exists():
    raise SystemExit('Existing receipt; do not resubmit.')
prompt = (out/'prompt.txt').read_text(encoding='utf-8-sig').strip()
args = ['image_to_video', '--image', str(root.parent/'assets'/'ANCH-006-B-photoreal-v002.png'), '--model', 'kling-video-v3_0', '--duration', '5', '--resolution', '1080p', '--imageCount', '1', '--enable_audio', 'false', '--prefer_multi_shots', 'false', prompt]
(out/'request.json').write_text(json.dumps({'source':'ANCH-006-B-photoreal-v002.png','expected_credits_based_on_previous_test':40,'cli_args':args},indent=2),encoding='utf-8')
receipt.write_text('{"local_status":"submission_started"}',encoding='utf-8')
r = subprocess.run(['C:/Program Files/nodejs/node.exe','C:/Users/arneg/AppData/Roaming/npm/node_modules/@klingai/cli-global/dist/cli.js',*args],capture_output=True,text=True,encoding='utf-8')
receipt.write_text(r.stdout,encoding='utf-8')
(out/'submission-stderr.txt').write_text(r.stderr,encoding='utf-8')
print(r.stdout)
print('Exit:',r.returncode)
