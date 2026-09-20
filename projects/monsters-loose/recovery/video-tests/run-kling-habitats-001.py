import json,subprocess
from pathlib import Path
o=Path(__file__).resolve().parent/'KLING-HABITATS-001'
if (o/'submission.json').exists():raise SystemExit('Already submitted; do not duplicate')
a=json.loads((o/'request.json').read_text())['cli_args'];(o/'submission.json').write_text('{"local_status":"submission_started"}')
r=subprocess.run(['C:/Program Files/nodejs/node.exe','C:/Users/arneg/AppData/Roaming/npm/node_modules/@klingai/cli-global/dist/cli.js',*a],capture_output=True,text=True,encoding='utf-8');(o/'submission.json').write_text(r.stdout);(o/'submission-stderr.txt').write_text(r.stderr);print(r.stdout)
