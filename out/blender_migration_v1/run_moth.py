"""Reuse frame-checked isolated review pipeline with explicit moth clocks."""
from pathlib import Path
import sys
O=Path(__file__).resolve().parent
code=(O/'run_walk.py').read_text()
replacements=[("D=O/'walk'","D=O/'moth'"),("walk_1280","moth_1280"),("walk_native.py","moth_native.py"),("'walk','1920','1,25,40,65,78,102'","'moth','1920','1,12,24,36,45,55'"),("'1','103'","'1','56'"),("'102'","'55'"),("screen_shotlist.json","walk_shotlist.json"),("garden_walk","garden_moth"),("O/'walk_shotlist.json'","O/'moth_shotlist.json'"),("'1374'","'1480'"),("'1513'","'1568'"),("start=57.25:end=63.083333333333","start=61.666666666667:end=65.375"),("'140'","'89'"),("(clean,102),(output,140)","(clean,55),(output,89)"),("audit_walk.py","audit_moth.py"),("check_walk.py","check_moth.py"),("walk_","moth_"),("mod(n\\\\,20)","mod(n\\\\,12)"),("Walk preview","Moth preview")]
# Apply before executing. Restore the input snapshot name after prefix rewrite.
for a,z in replacements:code=code.replace(a,z)
code=code.replace("edl=json.loads((O/'moth_shotlist.json')", "edl=json.loads((O/'walk_shotlist.json')")
if '--repair' in sys.argv:
    start=code.index("run('moth_render',")
    end=code.index("\nrun('moth_1920'",start)
    code=code[:start]+"run('moth_repair',[BL,'-b','--python-exit-code','1','-P',str(O/'moth_native.py'),'--','moth','1280','1,2,3,4,5,6,7,48,49,50,51,52,53,54,55'])"+code[end:]
exec(compile(code,str(O/'run_walk.py'),'exec'))
