from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'audit_walk.py').read_text().replace("D=O/'walk'","D=O/'waking'").replace("walk_{width}","waking_{width}").replace('(1,102,24','(1,81,24').replace('[40,78]','[38,61]')
exec(compile(code,str(O/'audit_walk.py'),'exec'))
