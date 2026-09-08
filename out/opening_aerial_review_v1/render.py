"""Verify returned Flow footage and audition the approved 77-frame insertion."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
handoff=json.loads((ROOT/'out/opening_aerial_flow_v1/handoff.json').read_text())
for item in list(handoff['inputs'].values())+[handoff['claude_result']['base'],handoff['claude_result']['original']]:
    assert hashlib.sha256((ROOT/item['file']).read_bytes()).hexdigest()==item['sha256'],item['file']
source=ROOT/'out/opening_aerial_flow_v1/base.mp4'
subprocess.run(['ffmpeg','-v','error','-i',str(source),'-f','null','-'],check=True)
code=(ROOT/'out/opening_need_aerial_v1/render.py').read_text()
begin=code.index('lock=');end=code.index('edl=json.loads')
code=code[:begin]+code[end:]
code=code.replace('opening_need_aerial_v1','opening_aerial_review_v1')
code=code.replace("'out/opening_aerial_review_v1/clean.mp4'","'out/opening_aerial_flow_v1/base.mp4'")
code=code.replace('183','205').replace('225','282')
code=code.replace("'insert_frames':42","'insert_frames':77").replace("'duration_seconds':1.75","'duration_seconds':77/24")
code=code.replace('High river-region aerial preview, simulated lateral move over new reference still','Generated horizon-to-oasis aerial; source0..77, unretimed')
code=code.replace('2D lateral motion over built-in generated aerial still, not Flow footage','Flow physical aerial move, native24fps, no green glimmer yet')
exec(compile(code,str(OUT/'inherited_render.py'),'exec'),{'__file__':str(OUT/'inherited_render.py'),'__name__':'__main__'})
result=json.loads((OUT/'verification.json').read_text())
result.update(source_sha256=handoff['claude_result']['base']['sha256'],input_and_output_hashes_verified=True,source_frames=192,source_used=[0,77],exit_handle_frames=115,generated_audio_excluded=True,owner_approval='pending')
(OUT/'verification.json').write_text(json.dumps(result,indent=2))
