from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
p=ROOT/'tools/tracked_light_pilot.py'
s=p.read_text()
for old,new in [
 ("OUT = ROOT / 'out/tracked_light_receiver'","OUT = ROOT / 'out/receiver_retimed_review/fx'"),
 ("ROOT / 'generated/overlay_cues.json'","ROOT / 'out/receiver_retimed_review/overlay_cues.json'"),
 ("ROOT / 'shots/shotlist.json'","ROOT / 'out/receiver_retimed_review/shotlist.json'")]:
    assert s.count(old)==1
    s=s.replace(old,new)
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
