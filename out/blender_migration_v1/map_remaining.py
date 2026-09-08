"""Static recipe dependency hints, deliberately not a native-certification tool."""
from pathlib import Path
import json,re
O=Path(__file__).resolve().parent;R=O.parents[1]
roots={
 'scope':'tools/screen_sync_phosphor.py',
 'receiver_arrival':'out/receiver_now_v3/render.py',
 'screen_garden':'out/screen_garden_trial/render.py',
 'moth_walk':'out/garden_ghost_wings_v3/render.py',
 'waking':'out/garden_waking_v3/render.py',
 'planet':'out/next_mars_sequence_v1/render.py',
 'world_orb':'out/colony_world_blossom_v2/render.py',
 'shop':'out/shop_wide_synced_v5/render.py',
 'meaning_exchange':'out/meaning_exchange_dual_sync_v6/render.py',
 'bends_mind':'out/bends_mind_fx_v2/render.py',
 'outro':'out/outro_particle_continuity_v1/render.py'}
result={}
for family,entry in roots.items():
    todo=[entry];seen={};missing=[]
    while todo and len(seen)<80:
        rel=todo.pop()
        if rel in seen:continue
        p=R/rel
        if not p.exists():missing.append(rel);continue
        text=p.read_text(encoding='utf-8')
        refs=sorted(set(re.findall(r"(?:out|tools)/[A-Za-z0-9_./-]+\.py",text)))
        refs=[r for r in refs if (R/r).is_file()]
        flags=[token for token in ['cv2.','pixels.foreach_set','np.mgrid','np.zeros','exec(compile','bpy.'] if token in text]
        seen[rel]={'references':refs,'review_flags':flags}
        todo.extend(refs)
    result[family]={'entry':entry,'files':seen,'missing_entry':missing,'status':'static_hints_only_dynamic_wrappers_require_manual_reconciliation'}
(O/'remaining_dependencies.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:len(v['files']) for k,v in result.items()},indent=2))
