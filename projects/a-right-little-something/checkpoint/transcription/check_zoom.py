import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path('tools').resolve()))
from timeline import load_project
p,b=load_project(pathlib.Path('projects/a-right-little-something/project.json'))
sys.path.insert(0,p['alignmentRuntime']['extensions'])
import torch, whisper, librosa
torch.set_num_threads(6)
m=whisper.load_model('large-v3-turbo',device='cuda',download_root=p['alignmentRuntime']['modelCache'])
results=[]
for role in ['lead','leadRenaissance','audio']:
    offset=0 if role=='audio' else p['vocalOrigin']['masterSeconds']
    a=117-offset
    y=whisper.load_audio(p['sources'][role])[int(a*16000):int((125-offset)*16000)]
    for speed in [1,0.65]:
        z=y if speed==1 else librosa.effects.time_stretch(y,rate=speed)
        r=m.transcribe(z,language='en',word_timestamps=True,condition_on_previous_text=False,temperature=0,verbose=False)
        words=[dict(text=w['word'],start=117+w['start']*speed,end=117+w['end']*speed) for s in r['segments'] for w in s.get('words',[])]
        results.append(dict(role=role,speed=speed,text=r['text'],words=words))
        print(role,speed,r['text'],words,flush=True)
(b/'generated/transcription/zoom-local.raw.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
