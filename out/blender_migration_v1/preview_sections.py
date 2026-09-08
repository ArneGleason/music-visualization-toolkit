"""Isolated contextual reviews. Keep original source clocks and native lyrics."""
from pathlib import Path
import json,sys
O=Path(__file__).resolve().parent;R=O.parents[1]
src=R/'tools/blender_comp.py'
code=src.read_text(encoding='utf-8')
needle='(ROOT / "generated" / "overlay_cues.json")'
assert code.count(needle)==1
code=code.replace(needle,'(ROOT / "out/swirl_tail_review_v1/overlay_cues.json")')
needle='decisions = load_decisions(ROOT)'
assert code.count(needle)==1
code=code.replace(needle,needle+'\n    decisions.update(json.loads((ROOT / "out/receiver_voice_review/receiver_decision.json").read_text()))')
needle='    bpy.ops.render.render(animation=True)'
assert code.count(needle)==1
numbers='''    numbering = json.loads((ROOT / 'out/blender_migration_v1/migration_register.json').read_text())['shots']
    for item in numbering:
        sa, sb = item['song_frames']
        if sb <= f0 or sa > f1: continue
        num = strips.new_effect(name='review_number_'+item['id'], type='TEXT', channel=110, frame_start=B(sa), length=sb-sa)
        num.text = str(item['review_number'])
        num.font_size = round(H*.032)
        num.location = (.957,.954)
        num.color = (1,1,1,1)
        num.use_shadow = True
        num.shadow_color = (0,0,0,1)
        num.use_outline = True
        num.outline_color = (0,0,0,1)
        num.outline_width = .075
'''
code=code.replace(needle,numbers+needle)
exec(compile(code,str(src),'exec'),{'__name__':'__main__','__file__':str(src)})
