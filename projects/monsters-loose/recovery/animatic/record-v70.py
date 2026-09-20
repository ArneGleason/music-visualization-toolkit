from pathlib import Path
import json
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');p=r/'shots/shotlist.json';d=json.loads(p.read_text());preview='animatic/MonstersLoose-v70-scene9-performances.mp4'
for s in d['shots']:
 names={'SCN-009-LAB-DISCUSSION':'discussion','SCN-009-TOWN-REPRISE':'fire','SCN-009-DESIGN-PITCH':'presentation'}
 if s['id'] in names:
  n=names[s['id']];s.update(source=f'motion-graphics/SCENE9-PERFORMANCES-001/{n}-timed-v001.mp4',media_type='video',status='generated_for_review',effects_record='motion-graphics/SCENE9-PERFORMANCES-001/selections.json')
  s['note']={'discussion':'Scientists gesture and react; Blender red eye tracks rising silhouette head.','fire':'Gorilla inhales and breathes a sustained flame over rooftops.','presentation':'Mechanical hand points across proposed design and retracts for blur zoom.'}[n]
 if s['id']=='SCN-009-BLUR-ZOOM':s['source']='motion-graphics/SCHEMATIC-ZOOM-002/schematic-blur-zoom-v001.mp4';s['note']='16-frame approved blur camera move rebuilt from last presentation pose.'
 if s.get('source','').startswith('motion-graphics/FLIGHT-SNOW-002'):s.update(status='user_approved',approval_note='User approved natural snow overlap in v69: looks perfect.')
d['current_preview']=preview;d['next_scene_planning'].update(preview=preview,status='all_scene9_performances_assembled_for_review',credits=216)
p.write_text(json.dumps(d,indent=2)+'\n')
n=r/'shots/SCN-009-next-creation-direction.md'
n.write_text(n.read_text()+'\n\n## v70 generated performances\nThree five-second Kling takes, 40 credits each (120 additional; Scene9 total216). Discussion2906..2974, fire2974..3031, presentation3031..3088. Source selections in SCENE9-PERFORMANCES-001/selections.json. Cage eye follows rising head. Zoom002 uses final presentation pose. Approved schematic002 and chewing3104..3223 remain unchanged. All earlier footage and approved countdown/snow effects retained.\n')
(r/'motion-graphics/SCENE9-PERFORMANCES-001/README.md').write_text('Scene9 v70: three Kling performances. See selections.json for exact source-frame maps. Native 24fps discussion and flame; presentation maps80 source-frame intervals into56 output intervals. Blender cage-eye keys follow silhouette head. Last presentation pose feeds SCHEMATIC-ZOOM-002. Approved SCHEMATIC-ACTION-002 retained. 120 additional credits.\n')
