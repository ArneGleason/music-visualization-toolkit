from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
p=ROOT/'tools/blender_comp.py';s=p.read_text(encoding='utf-8')
old='(ROOT / "generated" / "overlay_cues.json")';assert s.count(old)==1
s=s.replace(old,'(ROOT / "out" / "opening_aerial_glimmer_v1" / "overlay_cues.json")')
old='decisions = load_decisions(ROOT)';assert s.count(old)==1
s=s.replace(old,old+'\n    decisions.update(json.loads((ROOT / "out/receiver_voice_review/receiver_decision.json").read_text()))')
s=s.replace('    bpy.ops.render.render(animation=True)',"    lightdir = ROOT / 'out/opening_aerial_glimmer_v1/lights'\n    light = strips.new_image(name='garden_signal_and_architecture', filepath=str(lightdir/'000.png'), channel=90, frame_start=B(205))\n    for number in range(1,77): light.elements.append(f'{number:03}.png')\n    light.frame_final_duration = 77\n    light.blend_type = 'ADD'\n    light.blend_alpha = 0.85\n"+'    bpy.ops.render.render(animation=True)')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
