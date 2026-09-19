import json, subprocess, time, urllib.request
from pathlib import Path

out = Path(__file__).resolve().parent/'KLING-SWAMP-FROG-001'
task = json.loads((out/'submission.json').read_text(encoding='utf-8'))['body']['generationId']
cli = ['C:/Program Files/nodejs/node.exe','C:/Users/arneg/AppData/Roaming/npm/node_modules/@klingai/cli-global/dist/cli.js']
# Read-only polling, never resubmit. Save promptly because result URLs expire.
for attempt in range(60):
    r = subprocess.run([*cli,'query_tasks',task],capture_output=True,text=True,encoding='utf-8')
    if r.returncode:
        print('Query failed; stopping without retrying generation.',flush=True)
        raise SystemExit(1)
    data = json.loads(r.stdout)
    (out/'result.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    body = data.get('body',{})
    print(body.get('status','unknown'),flush=True)
    works = body.get('works',[])
    urls = [w.get('urlWithoutWatermark',w['url']) for w in works if w.get('url')]
    if urls:
        for i,url in enumerate(urls,1):
            dest = out/f'KLING-SWAMP-FROG-001-{i:02}.mp4'
            urllib.request.urlretrieve(url, dest)
            print(f'SAVED {dest} ({dest.stat().st_size} bytes)',flush=True)
        break
    if str(body.get('status','')).upper() in ('FAILED','FAIL','ERROR','CANCELED','CANCELLED'):
        raise SystemExit('Generation ended without output; see result.json')
    time.sleep(30)
else:
    raise SystemExit('Polling stopped after 30 minutes; task ID retained.')








