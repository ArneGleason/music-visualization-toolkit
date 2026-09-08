"""Preserve bloom timing/light response, replace only green-guide choreography."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
p=ROOT/'out/garden_begin_bloom_v3/render.py'
s=p.read_text()
start=s.index('# Reuse the approved green guide')
end=s.index("source_path = ROOT /", start)
s=s[:start]+"namespace = {'__file__': str(OUT/'guide.py')}\nexec(compile((OUT/'guide.py').read_text(), str(OUT/'guide.py'), 'exec'), namespace)\n\n"+s[end:]
s=s.replace('garden_begin_bloom_v3','garden_guide_conductor_v4')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
r=json.loads((OUT/'recipe.json').read_text())
r['green_guide']='Above-head conductor: arrives from upper right, beat-led orbit, gathers on song/to, upward cue at begin1828, then settles. Short persistent wake, same green identity. Added light excluded below y143. No face relighting.'
r['pending_lip_sync']='out/garden_bloom_lipsync_v2/handoff.json'
r['lip_sync_used']=False
r['integration']='Current preview uses original plate. Reapply guide.py and original song-timed lantern response after verifying new synced return, source66..134 at24fps; do not overlay this flattened picture over returned lips.'
(OUT/'recipe.json').write_text(json.dumps(r,indent=2))
