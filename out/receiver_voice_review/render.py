"""Reuse the approved local assembly recipe with a versioned FX destination."""
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent.parent
p=ROOT/'out/receiver_retimed_review/render.py'
s=p.read_text().replace('out/receiver_retimed_review/fx/clean.mp4','out/receiver_voice_review/fx/clean.mp4')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
