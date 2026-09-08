"""Move the face exit six frames earlier than v5."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
source=ROOT/'out/swimmer_cutaway_v3/render.py'
code=source.read_text().replace('swimmer_cutaway_v3','swimmer_cutaway_v6')
code=code.replace('3400','3376').replace('78/24','54/24').replace('+100','+76')
code=code.replace('source78','source54').replace('3322+78','3322+54').replace('[78,116]','[54,116]')
exec(compile(code,str(source),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
