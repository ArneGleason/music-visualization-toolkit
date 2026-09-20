from pathlib import Path
import json,shutil
r=Path(__file__).resolve().parents[2];o=Path(__file__).resolve().parent
p=r/'shots/shotlist.json';d=json.loads(p.read_text(encoding='utf-8'))
backup=r/'shots/shotlist-pre-countdown-v60.json'
if not backup.exists():shutil.copy2(p,backup)
selections=json.loads((o/'selections.json').read_text())
d['shots']=[s for s in d['shots'] if s['id'] not in ['COUNTDOWN-SHOWDOWN-PLAN','MOUNTAIN-KICK-PLAN'] and not s['id'].startswith('SCN-008-COUNTDOWN-')]
for name,sel in selections.items():
 d['shots'].append({'id':'SCN-008-COUNTDOWN-'+name.upper(),'start_frame':sel['start_frame'],'end_frame_exclusive':sel['start_frame']+sel['frames'],'source':sel['output'],'source_in_frame':0,'media_type':'video','status':'assembled_for_review','note':sel['note'],'effects_record':'motion-graphics/COUNTDOWN-EDIT-001/selections.json','direction_record':'shots/SCN-008-countdown-battle-ladder.md'})
d['shots'].append({'id':'SCN-008-COUNTDOWN-COUNT4','start_frame':2537,'end_frame_exclusive':2548,'source':'assets/SCN-008-count4-v001.png','source_in_frame':0,'media_type':'image','status':'assembled_for_review','note':'11-frame defeated insect tableau with Blender impact jolt and count4; no paid video.'})
d['shots'].sort(key=lambda s:s.get('start_frame',0))
d['countdown_production']={'status':'assembled_for_review','credits':272,'animatic_review':'animatic/MonstersLoose-v59-countdown-animatic.mp4','preview':'animatic/MonstersLoose-v60-through-arctic-homecoming.mp4','blender':'animatic/MonstersLoose-v60-countdown-and-kick.blend','start_frame':2510,'end_frame_exclusive':2906,'finalists':['recurring green orange-spined lizard','white shaggy black-horned Arctic beast'],'note':'User authorized render/assembly; first Arctic/desert matchup briefly questioned then confirmed. Six generated takes, one still tableau; no paid regeneration.'}
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
