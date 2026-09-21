import json, subprocess, sys, io
from pathlib import Path
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parent.parent
specs=json.loads((r/'shots/SCN-014-015-production-plan.json').read_text())['shots']
out=r/'motion-graphics/OUTRO-002';out.mkdir(exist_ok=True)
for s in specs:
 if len(sys.argv)>1 and s['name'] not in sys.argv[1:]:continue
 folder=r/'video-tests'/('KLING-SCENE14-'+s['name']+'-002');p=folder/(folder.name+'-01.mp4')
 if not p.exists():continue
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))
 (folder/'probe.json').write_text(json.dumps(probe,indent=2))
 times=[0.5,1,1.5,2,2.5,min(s['generation_seconds']-.3,3.5)]
 if s['name']=='PLAY':times=[1.5,2.5,3.5,4.3,5,5.8]
 if s['name']=='INSPECTOR':times=[.5,1.2,2,2.8,3.5,4.5]
 if s['name']=='HARPER-KID':times=[.5,1.8,3,4.3,5.8,7]
 if s['name']=='FINALE':times=[.5,2.5,5,7.5,10,14.5]
 sheet=Image.new('RGB',(1440,580),(25,25,25));draw=ImageDraw.Draw(sheet)
 for i,t in enumerate(times):
  raw=subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=480:270','-f','image2pipe','-vcodec','png','-threads','1','-'])
  frame=Image.open(io.BytesIO(raw));x=(i%3)*480;y=(i//3)*290
  sheet.paste(frame,(x,y));draw.text((x+5,y+273),s['name']+' '+str(t)+' sec',fill='white')
 sheet.save(out/(s['name']+'-review.jpg'))
 print(s['name'],probe['streams'][0].get('nb_frames'),flush=True)
