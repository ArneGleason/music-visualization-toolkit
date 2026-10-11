"""Read only the provider's model declarations, omitting account information."""
import json
import subprocess
from pathlib import Path
cli=['C:/Program Files/nodejs/node.exe','C:/Users/arneg/AppData/Roaming/npm/node_modules/@klingai/cli-global/dist/cli.js','who_am_i']
result=subprocess.run(cli,capture_output=True,text=True,encoding='utf-8',check=True)
data=json.loads(result.stdout)
print('Response keys:',list(data))
body=data.get('body',{})
if isinstance(body,dict):
    print('Declaration fields:',list(body))
    for key,value in body.items():
        if any(word in key.lower() for word in ['model','capabilit','tool','declaration']):
            print(key+': '+json.dumps(value))
            (Path(__file__).resolve().parent/('provider-'+key+'.json')).write_text(json.dumps(value,indent=2),encoding='utf-8')
