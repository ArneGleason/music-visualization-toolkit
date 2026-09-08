"""Advance only the face exit to the middle of 'the'."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
source=ROOT/'out/swimmer_cutaway_v3/render.py'
code=source.read_text().replace('swimmer_cutaway_v3','swimmer_cutaway_v4')
code=code.replace('3400','3388').replace('78/24','66/24').replace('+100','+88')
code=code.replace('source78','source66').replace('3322+78','3322+66').replace('[78,116]','[66,116]')
exec(compile(code,str(source),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
