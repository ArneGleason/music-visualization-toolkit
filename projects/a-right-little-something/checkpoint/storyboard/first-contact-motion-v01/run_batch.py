"""Submit each authorized take once, or collect outstanding takes read-only."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
ROOT = BASE.parents[1]
PLAN = BASE/'kling-first-contact-motion-v01.json'
CLI = ['C:/Program Files/nodejs/node.exe',
       'C:/Users/arneg/AppData/Roaming/npm/node_modules/@klingai/cli-global/dist/cli.js']


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def cli_read(command, filename):
    proc = subprocess.run(CLI+[command],capture_output=True,text=True,encoding='utf-8')
    if proc.returncode:
        raise RuntimeError(proc.stderr[:1000])
    data = json.loads(proc.stdout)
    assert data.get('ok'), data
    save(OUT/filename, data)
    return data['body']


def snapshot(plan):
    rows=[]
    for shot in plan['shots']:
        folder=BASE/plan['output']/shot['id']
        submission=folder/'submission.json'
        result=folder/'result.json'
        row=dict(id=shot['id'],status='NOT_SUBMITTED',credits=0)
        if submission.exists():
            data=read(submission)
            body=data.get('body',{})
            row.update(status=body.get('status','SUBMISSION_ERROR'),
                       credits=body.get('creditsConsumed',0),generationId=body.get('generationId'))
        if result.exists():
            row['status']=read(result).get('body',{}).get('status',row['status'])
        raw=folder/(shot['id']+'-01-clean.mp4')
        if raw.is_file() and raw.stat().st_size>0:
            row.update(status='COLLECTED',motionRef=raw.relative_to(BASE).as_posix())
        rows.append(row)
    data=dict(credits=sum(r['credits'] for r in rows),submitted=sum(bool(r.get('generationId')) for r in rows),
              collected=sum(r['status']=='COLLECTED' for r in rows),total=len(rows),tasks=rows)
    save(OUT/'generation-status.json',data)
    return data


parser=argparse.ArgumentParser()
parser.add_argument('mode',choices=['submit','collect','status'])
args=parser.parse_args()
plan=read(PLAN)
assert len(plan['shots'])==37 and sum(s['estimatedCredits'] for s in plan['shots'])==1528
if args.mode=='submit':
    cli_read('who_am_i','live-models.json')
    account=cli_read('account','account-before.json')
    state=snapshot(plan)
    need=sum(s['estimatedCredits'] for s,r in zip(plan['shots'],state['tasks']) if not r.get('generationId'))
    assert account['availableRemainCredits']>=need, 'Insufficient balance; no new submission'
    for shot in plan['shots']:
        assert hashlib.sha256((BASE/shot['firstImage']).read_bytes()).hexdigest()==shot['firstImageSha256']
        folder=BASE/plan['output']/shot['id']
        if (folder/'request.json').exists():
            assert (folder/'submission.json').exists(), 'Uncertain prior attempt; do not retry'
            assert read(folder/'submission.json').get('body',{}).get('generationId'), 'Uncertain prior attempt; do not retry'
            continue
        assert snapshot(plan)['credits']+shot['estimatedCredits']<=plan['submissionCreditLimit']
        subprocess.run([sys.executable,str(ROOT/'tools/run_kling_test.py'),str(PLAN),
                        '--submit','--only',shot['id']],check=True)
        body=read(folder/'submission.json')['body']
        assert body['creditsConsumed']==shot['estimatedCredits'], 'Rate changed; stop batch'
        state=snapshot(plan)
        print(f"Submitted {state['submitted']}/37; charged {state['credits']} credits",flush=True)
    cli_read('account','account-after-submission.json')
    plan.update(status='All37 source videos submitted; collecting results',actualCredits=snapshot(plan)['credits'])
    save(PLAN,plan)
elif args.mode=='collect':
    failures=0
    while True:
        state=snapshot(plan)
        pending=[r for r in state['tasks'] if r.get('generationId') and r['status']!='COLLECTED']
        if not pending:
            break
        for row in pending:
            proc=subprocess.run([sys.executable,str(ROOT/'tools/run_kling_test.py'),str(PLAN),
                                 '--only',row['id']],capture_output=True,text=True,encoding='utf-8')
            if proc.returncode:
                failures+=1
                print(row['id'],'collection error; no resubmission',proc.stderr[-500:],flush=True)
                if failures>=5:
                    raise SystemExit('Repeated collection errors; persisted task IDs remain safe')
            else:
                print(proc.stdout.strip(),flush=True)
        state=snapshot(plan)
        print(f"Collected {state['collected']}/{state['submitted']}; charged {state['credits']} credits",flush=True)
        terminal=[r for r in state['tasks'] if r['status'] in ('FAILED','CANCELED','CANCELLED','REJECTED')]
        if terminal:
            print('Provider failures; no automatic paid retries:',json.dumps(terminal),flush=True)
            break
        if state['collected']==state['submitted']:
            break
        time.sleep(40)
    if state['collected']==37:
        plan.update(status='All37 source videos collected; motion review pending',actualCredits=state['credits'])
        save(PLAN,plan)
else:
    state=snapshot(plan)
    print(json.dumps({k:v for k,v in state.items() if k!='tasks'}))
