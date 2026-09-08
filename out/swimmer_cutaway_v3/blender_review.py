from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
p=ROOT/'tools/blender_comp.py';s=p.read_text(encoding='utf-8')
old='(ROOT / "generated" / "overlay_cues.json")';assert s.count(old)==1
s=s.replace(old,'(ROOT / "out" / "swimmer_cutaway_v3" / "overlay_cues.json")')
old='decisions = load_decisions(ROOT)';assert s.count(old)==1
s=s.replace(old,old+'\n    decisions.update(json.loads((ROOT / "out/receiver_voice_review/receiver_decision.json").read_text()))')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
