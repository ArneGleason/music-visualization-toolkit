"""Move the face exit six frames earlier than v4."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
source=ROOT/'out/swimmer_cutaway_v3/render.py'
code=source.read_text().replace('swimmer_cutaway_v3','swimmer_cutaway_v5')
code=code.replace('3400','3382').replace('78/24','60/24').replace('+100','+82')
code=code.replace('source78','source60').replace('3322+78','3322+60').replace('[78,116]','[60,116]')
exec(compile(code,str(source),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
