"""Dependency and saved-scene random access checks; no external FX buffers."""
from pathlib import Path
import bpy,json
O=Path(__file__).resolve().parent; D=O/'message'; records=[]
for width in [1280,1920]:
    file=D/f'message_{width}.blend'; bpy.ops.wm.open_mainfile(filepath=str(file)); s=bpy.context.scene
    assert (s.frame_start,s.frame_end,s.render.fps,s.render.resolution_x,s.render.resolution_y)==(1,230,24,width,width*9//16)
    images=[]
    for im in bpy.data.images:
        if im.source not in ['FILE','SEQUENCE','MOVIE']:continue
        p=Path(bpy.path.abspath(im.filepath)).resolve(); assert p.exists() and p.is_relative_to((D/'plates').resolve()); images.append(str(p))
    assert images and s.compositing_node_group is not None
    assert not [im for im in bpy.data.images if im.source=='GENERATED' and im.name not in ['Render Result','Viewer Node']]
    records.append({'width':width,'status':'native_dependencies_pass','images':images,'view_layers':[v.name for v in s.view_layers]})
    if width==1280:
        for f in [70,211]:
            s.frame_set(f); s.render.filepath=str(D/f'random_access_{f:04d}.png'); bpy.ops.render.render(write_still=True)
(D/'blend_audit.json').write_text(json.dumps(records,indent=2)); print(records)
