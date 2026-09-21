import bpy,json,warnings
from pathlib import Path
warnings.filterwarnings('ignore',category=DeprecationWarning)
o=Path(__file__).resolve().parent;r=o.parent
bpy.ops.wm.open_mainfile(filepath=str(o/'MonstersLoose-v92-outro-performances.blend'))
s=bpy.context.scene;seq=s.sequence_editor.strips
lyrics_before=[st.name for st in seq if st.type=='TEXT' and st.name.startswith('lead-')]
counts_before=[st.name for st in seq if st.type=='TEXT' and st.name.startswith('Count punch')]
removed=[]
for st in list(seq):
 if st.type=='TEXT' and 100<=st.channel<=105:
  removed.append(dict(name=st.name,text=st.text,start=int(st.frame_final_start),end=int(st.frame_final_end)))
  seq.remove(st)
assert [st.name for st in seq if st.type=='TEXT' and st.name.startswith('lead-')]==lyrics_before
assert [st.name for st in seq if st.type=='TEXT' and st.name.startswith('Count punch')]==counts_before
(o/'v93-removed-scene-markers.json').write_text(json.dumps(dict(removed=removed,lyrics_preserved=len(lyrics_before),countdown_graphics_preserved=len(counts_before)),indent=2))
shots=json.loads((r/'motion-graphics/OUTRO-LIGHTS-001/original-shots.json').read_text())
for take in shots:
 p=r/'motion-graphics/OUTRO-LIGHTS-001'/(take['id']+'-beacons-v001.mp4')
 if not p.exists():continue
 for st in list(seq):
  if st.channel==1 and st.frame_final_start==take['start_frame']:seq.remove(st)
 st=seq.new_movie(take['id']+' blinking facility beacons',str(p),channel=1,frame_start=take['start_frame'],fit_method='FIT')
 st.frame_final_duration=take['end_frame_exclusive']-take['start_frame'];st.channel=1
s.frame_end=5290;s.name='Monsters Loose v93 clean lyrics swamp cousin and beacons';s.render.filepath=str(o/'MonstersLoose-v93-swamp-cousin-beacons.mp4')
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(o/'MonstersLoose-v93-swamp-cousin-beacons.blend'))
bpy.ops.render.render(animation=True)
