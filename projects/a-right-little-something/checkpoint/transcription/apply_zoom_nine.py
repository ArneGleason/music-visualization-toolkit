import json,pathlib,sys
sys.path.insert(0,str(pathlib.Path('tools').resolve()))
from timeline import MusicalGrid
b=pathlib.Path('projects/a-right-little-something')
cuefile=b/'lyrics/zoom-cues.json';doc=json.loads(cuefile.read_text());cues=doc['cues']
adjustfile=b/'lyrics/performed-adjustments.json';adjust=json.loads(adjustfile.read_text(encoding='utf-8'))
words=[dict(text='Zoom',start=119.43,end=cues[0]['masterSeconds'],edgeSource='localized Whisper; checked against vocal energy')]
for i,c in enumerate(cues):
 end=cues[i+1]['masterSeconds'] if i<8 else 121.63
 words.append(dict(text='in,' if i<8 else 'in',start=c['masterSeconds'],end=end,edgeSource=c['basis'],zoomCue=i+1))
words.extend([dict(text=t,start=a,end=z,edgeSource='original lead/master localized Whisper') for t,a,z in [('to',121.63,121.74),('see',121.74,121.96),('far',121.96,122.34)]])
adjust['lyr-044']=dict(text='Zoom '+', '.join(['in']*9)+' to see far',
                     reviewStatus='Nine repetitions confirmed by user; independently measured vowel attacks need listening verification',
                     recognitionBasis='User performed wording; original-lead acoustic attacks and processed-stem cross-check, not equal interpolation',words=words)
adjustfile.write_text(json.dumps(adjust,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
shotfile=b/'shots/shotlist.json';shots=json.loads(shotfile.read_text(encoding='utf-8'))
grid=MusicalGrid(json.loads((b/'generated/beatmap.json').read_text(encoding='utf-8')))
def frame(t):return round(grid.sec(grid.position(t))*24)+1
a,z=frame(117.90),frame(122.34)
shot=dict(id='telescope-zoom-nine',section='section-7',type='concept',setup='sphere-telescope-pov',
          start=grid.position(117.90).text(),end=grid.position(122.34).text(),startFrame=a,endFrameExclusive=z,frames=z-a,
          lyric=doc['lyric'],status='creative intent captured; onset review before final animation',
          description="Her point of view through the spacecraft sphere. A distant dot stays centered. Each of nine sung 'in's triggers another progressive magnification, revealing a planet in a faraway stellar system. The inside of the transparent sphere acts as a telescope display: the image she appears to see through it is optically projected/magnified, as though looking directly at the distant planet. Keep a continuous viewpoint and recognizable target across all nine steps.",
          zoomCues=cues,prompt='',clip={'file':None,'in_sec':0.0,'speed':1.0},transition={'type':'cut','dur_sec':0.0})
existing=next((s for s in shots['shots'] if s['id']==shot['id']),None)
if existing:existing.update(zoomCues=cues,startFrame=a,endFrameExclusive=z,frames=z-a)
else:shots['shots'].append(shot)
shots['status']='partial creative plan; nine-zoom shot captured during lyric review'
shotfile.write_text(json.dumps(shots,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
performed=b/'lyrics/performed.txt';text=performed.read_text(encoding='utf-8')
text=text.replace('Zoom in and in and in to see far things big now.',adjust['lyr-044']['text'])
text=text.replace('The rapid “in” sequence currently follows the arranged wording; its repetition count and interpolated timing still need listening review.','The zoom line contains nine performed “in”s, as confirmed by the songwriter. Individual vowel-attack cues were measured from the original vocal, with a processed-vocal cross-check; onset placement still needs listening verification.')
performed.write_text(text,encoding='utf-8')
print('Updated performed wording, nine acoustic cues and source-of-truth shot intent')
