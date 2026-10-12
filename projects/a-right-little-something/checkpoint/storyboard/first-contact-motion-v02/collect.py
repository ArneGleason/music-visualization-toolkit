"""Collect only already-submitted V63 jobs; never submit or retry paid work."""
import json
from pathlib import Path
import subprocess
import sys
import time
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
ROOT=BASE.parents[1]
PLAN=BASE/'kling-first-contact-motion-v02.json'
plan=json.loads(PLAN.read_text(encoding='utf-8'))
for sweep in range(90):
    rows=[]
    for s in plan['shots']:
        folder=BASE/plan['output']/s['id']
        raw=folder/(s['id']+'-01-clean.mp4')
        if not raw.exists():
            subprocess.run([sys.executable,str(ROOT/'tools/run_kling_test.py'),str(PLAN),'--only',s['id']],check=True)
        result=json.loads((folder/'result.json').read_text(encoding='utf-8')) if (folder/'result.json').exists() else {}
        status='COLLECTED' if raw.exists() else result.get('body',{}).get('status','UNKNOWN')
        rows.append(dict(id=s['id'],status=status))
    credits=sum(json.loads((BASE/plan['output']/s['id']/'submission.json').read_text(encoding='utf-8'))['body']['creditsConsumed'] for s in plan['shots'])
    assert credits==248
    count=sum(r['status']=='COLLECTED' for r in rows)
    (OUT/'generation-status.json').write_text(json.dumps(dict(collected=count,total=6,credits=credits,tasks=rows),indent=2)+'\n',encoding='utf-8')
    print(f'Collected {count}/6; charged {credits} credits',flush=True)
    if any(r['status'] in ['FAILED','CANCELLED','CANCELED','REJECTED'] for r in rows): raise SystemExit('Provider failure; no automatic paid retry')
    if count==6: break
    time.sleep(45)
