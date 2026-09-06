"""Use the shared renderer with an isolated cue input, without editing it."""
from pathlib import Path
OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent
source_path = ROOT/'tools/blender_comp.py'
source = source_path.read_text(encoding='utf-8')
old = '(ROOT / "generated" / "overlay_cues.json")'
new = '(ROOT / "out" / "opening_phrase_cut" / "overlay_cues.json")'
assert source.count(old)==1, 'Shared renderer changed; inspect adapter before rendering'
source = source.replace(old,new)
exec(compile(source,str(source_path),'exec'),{'__name__':'__main__','__file__':str(source_path)})
