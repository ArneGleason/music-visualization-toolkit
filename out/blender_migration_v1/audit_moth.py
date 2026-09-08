from pathlib import Path
O=Path(__file__).resolve().parent
code=(O/'audit_walk.py').read_text().replace("D=O/'walk'","D=O/'moth'").replace("walk_{width}","moth_{width}").replace('(1,102,24','(1,55,24').replace('[40,78]','[24,40]')
exec(compile(code,str(O/'audit_walk.py'),'exec'))
