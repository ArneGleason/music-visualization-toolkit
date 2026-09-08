"""Isolated full-film review wrapper with fixed source registry overrides."""
from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'preview_sections.py').read_text().replace('out/receiver_voice_review/receiver_decision.json','out/blender_migration_v1/full_native_decisions.json')
code=code.replace('out/swirl_tail_review_v1/overlay_cues.json','out/blender_migration_v1/full_native_cues.json')
# The source caches already carry their accepted display transforms. Keep the
# full-film output neutral instead of applying Blender's default AgX again.
code=code.replace("code=src.read_text(encoding='utf-8')", "code=src.read_text(encoding='utf-8')\ncode=code.replace('    r = sc.render', \"    sc.view_settings.view_transform = 'Standard'\\n    sc.view_settings.look = 'None'\\n    sc.view_settings.exposure = 0\\n    sc.view_settings.gamma = 1\\n    r = sc.render\")")
exec(compile(code,str(O/'preview_sections.py'),'exec'),{'__name__':'__main__','__file__':str(O/'preview_sections.py')})
