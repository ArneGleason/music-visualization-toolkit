"""Frame-checked native waking scene and moth-to-eyes context."""
from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'run_walk.py').read_text()
replacements=[("D=O/'walk'","D=O/'waking'"),("walk_1280","waking_1280"),("walk_native.py","waking_native.py"),("'walk','1920','1,25,40,65,78,102'","'waking','1920','1,25,38,49,61,81'"),("'1','103'","'1','82'"),("'102'","'81'"),("screen_shotlist.json","moth_shotlist.json"),("garden_walk","garden_waking_motion_audition"),("O/'walk_shotlist.json'","O/'waking_shotlist.json'"),("'1374'","'1514'"),("'1513'","'1649'"),("start=57.25:end=63.083333333333","start=63.083333333333:end=68.75"),("'140'","'136'"),("(clean,102),(output,140)","(clean,81),(output,136)"),("audit_walk.py","audit_waking.py"),("check_walk.py","check_waking.py"),("walk_","waking_"),("mod(n\\\\,20)","mod(n\\\\,17)"),("Walk preview","Waking preview")]
for a,z in replacements:code=code.replace(a,z)
exec(compile(code,str(O/'run_walk.py'),'exec'))
