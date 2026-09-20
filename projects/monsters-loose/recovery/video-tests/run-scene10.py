import json,subprocess,concurrent.futures,sys,urllib.request,time
from pathlib import Path
root=Path(__file__).resolve().parent
cli=['C:/Program Files/nodejs/node.exe','C:/Users/arneg/AppData/Roaming/npm/node_modules/@klingai/cli-global/dist/cli.js']
names=['count5','count3','count2','duel','flight','landing']
def run(name):
 out=root/('KLING-SCENE10-'+name.upper()+'-001')
 if sys.argv[1]=='submit':
  if (out/'submission.json').exists():return name+' already submitted'
  args=json.loads((out/'request.json').read_text())['cli_args']
  (out/'submission.json').write_text('{"local_status":"submission_started"}')
  p=subprocess.run([*cli,*args],capture_output=True,text=True,encoding='utf-8')
  (out/'submission.json').write_text(p.stdout,encoding='utf-8');(out/'submission-stderr.txt').write_text(p.stderr,encoding='utf-8')
  return name+': '+p.stdout
 task=json.loads((out/'submission.json').read_text())['body']['generationId']
 dest=out/(out.name+'-01.mp4')
 if dest.exists():return name+' already collected'
 for attempt in range(60):
  p=subprocess.run([*cli,'query_tasks',task],capture_output=True,text=True,encoding='utf-8')
  if p.returncode or not p.stdout.strip():
   time.sleep(30)
   continue
  data=json.loads(p.stdout);(out/'result.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
  body=data.get('body',{});works=body.get('works',[])
  urls=[w.get('urlWithoutWatermark') or w.get('url') for w in works]
  if urls and urls[0]:
   urllib.request.urlretrieve(urls[0],dest)
   return name+' SAVED '+str(dest)
  if body.get('status','').upper() in ['FAILED','ERROR','CANCELED','CANCELLED']:return name+' FAILED'
  time.sleep(30)
 return name+' pending'
if len(sys.argv)>2:names=sys.argv[2:]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for f in concurrent.futures.as_completed([pool.submit(run,n) for n in names]):
  print(f.result(),flush=True)
