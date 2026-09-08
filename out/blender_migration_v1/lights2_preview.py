from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'preview_sections.py').read_text()
needle='out/receiver_voice_review/receiver_decision.json'
assert code.count(needle)==1
code=code.replace(needle,'out/blender_migration_v1/lights2_receiver_decision.json')
exec(compile(code,str(O/'preview_sections.py'),'exec'),{'__name__':'__main__','__file__':str(O/'preview_sections.py')})
