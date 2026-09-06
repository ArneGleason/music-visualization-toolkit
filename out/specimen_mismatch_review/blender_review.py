from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
p=ROOT/'tools/blender_comp.py'
s=p.read_text(encoding='utf-8')
old='(ROOT / "generated" / "overlay_cues.json")'
assert s.count(old)==1
s=s.replace(old,'(ROOT / "out" / "specimen_mismatch_review" / "overlay_cues.json")')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
