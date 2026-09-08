"""Extend the approved swimmer edit through the chorus and fountain lead-out."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
source=ROOT/'out/spring_into_swimmers_v1/render.py'
code=source.read_text()
code=code.replace('out/spring_establish_v1/','out/swimmer_cutaway_v6/')
code=code.replace("[('s041',3229,3302),('s042',3302,3370),('s043',3370,3438),('s044',3438,3505)]","[('s045',3505,3574),('s046',3574,3642),('s047',3642,3710),('s048',3710,3778)]")
code=code.replace('spring_into_swimmers_v1','swimmer_chorus_review_v1')
code=code.replace('3505','3778')
# Restore new section start, changed by the global end replacement above.
code=code.replace("('s045',3778,3574)","('s045',3505,3574)")
code=code.replace('3100','3376').replace('3504','3777').replace('405','402')
exec(compile(code,str(source),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
