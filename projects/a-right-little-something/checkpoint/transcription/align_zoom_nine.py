import sys,json,pathlib
sys.path.insert(0,str(pathlib.Path('tools').resolve()))
from timeline import load_project
p,b=load_project(pathlib.Path('projects/a-right-little-something/project.json'))
sys.path.insert(0,p['alignmentRuntime']['extensions'])
import whisper,stable_whisper,torch,librosa
torch.set_num_threads(6)
m=stable_whisper.load_model('large-v3-turbo',device='cuda',download_root=p['alignmentRuntime']['modelCache'])
text='Hit zoom. Zoom '+', '.join(['in']*9)+' to see far things big now.'
results=[]
for role in ['lead','leadRenaissance']:
 a=117.5-p['vocalOrigin']['masterSeconds']
 y=whisper.load_audio(p['sources'][role])[int(a*16000):int((124-p['vocalOrigin']['masterSeconds'])*16000)]
 for rate in [1,0.5]:
  z=y if rate==1 else librosa.effects.time_stretch(y,rate=rate)
  r=m.align(z,text,language='en',regroup=False,word_dur_factor=None,max_word_dur=None,nonspeech_skip=None,verbose=None)
  words=[dict(text=w['word'].strip(),start=117.5+w['start']*rate,end=117.5+w['end']*rate) for s in r.to_dict()['segments'] for w in s['words']]
  print(role,rate,words,flush=True)
  results.append(dict(role=role,rate=rate,words=words))
(b/'generated/transcription/zoom-nine.alignment.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
