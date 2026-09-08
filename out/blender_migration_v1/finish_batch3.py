"""Encode checked native shots and prepare an isolated registry-aware preview edit."""
from pathlib import Path
import json,sys,subprocess,hashlib
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(R/'tools'))
from assembly_sources import load_decisions
families={'opening':86,'birds':76,'guide':60,'bloom':68,'pressure':69,'swim043':116,'swim044':67,'swim047':68,'tunnel':57,'titles':72}
families.update(pieces=48,meant=11)
receipts=[]
for family,n in families.items():
    d=O/family
    assert all((d/f'native_1280/{i:04d}.png').exists() for i in range(1,n+1)),family+' incomplete'
    clean=d/'native_clean.mp4'
    if not clean.exists():subprocess.run(['ffmpeg','-v','error','-n','-framerate','24','-start_number','1','-i',str(d/'native_1280/%04d.png'),'-frames:v',str(n),'-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(clean)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(clean),'-f','null','-'],check=True)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(clean)]))['streams']
    assert len(info)==1 and info[0]['r_frame_rate']=='24/1' and int(info[0]['nb_frames'])==n
    receipts.append({'family':family,'frames':n,'clean':str(clean.relative_to(R)),'sha256':hashlib.sha256(clean.read_bytes()).hexdigest(),'status':'native_rendered_review_pending','resolution_samples':len(list((d/'native_1920').glob('*.png')))})
(O/'batch3_receipts.json').write_text(json.dumps(receipts,indent=2))
mapping={'s001':('opening',0),'garden_walk_return_review':('guide',0),'garden_birds_fx_audition':('birds',0),'garden_begin_bloom_audition':('bloom',0),'landing_retry_s037':('pressure',0),'swimming_overhead_early':('swim043',54),'s044':('swim044',0),'s047':('swim047',0),'o01':('tunnel',0)}
mapping.update(pieces_insert=('pieces',0),meant_artifact_insert=('meant',0))
snapshot=json.loads((O/'lights2_shotlist.json').read_text());decisions=json.loads((O/'lights2_receiver_decision.json').read_text());protected=load_decisions(R)
for s in snapshot['shots']:
    if s['id'] not in mapping:continue
    family,start=mapping[s['id']];path=f'out/blender_migration_v1/{family}/native_clean.mp4'
    s['clip']={'file':path,'in_sec':start/24,'speed':1}
    if s['id'] in protected:
        item=dict(protected[s['id']]);item['delivery_file']=path;item['notes']='Isolated native migration review, not production promotion.';decisions[s['id']]=item
(O/'batch3_shotlist.json').write_text(json.dumps(snapshot,indent=2));(O/'batch3_decisions.json').write_text(json.dumps(decisions,indent=2))
print('All twelve native deliveries decoded and counted; isolated edit ready.')
