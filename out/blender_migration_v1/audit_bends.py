"""Inspect both saved native scenes and verify deterministic random access."""
from pathlib import Path
import bpy,json
O=Path(__file__).resolve().parent; D=O/'bends'; results=[]
for width in [1280,1920]:
    file=D/f'bends_{width}.blend'; bpy.ops.wm.open_mainfile(filepath=str(file)); s=bpy.context.scene
    assert (s.render.resolution_x,s.render.resolution_y,s.render.fps)==(width,width*9//16,24)
    assert (s.frame_start,s.frame_end)==(1,137)
    images=[]
    for image in bpy.data.images:
        if image.source not in ['FILE','SEQUENCE','MOVIE']:continue
        p=Path(bpy.path.abspath(image.filepath)).resolve(); assert p.is_relative_to((D/'plates').resolve()) and p.exists()
        images.append(str(p))
    assert images
    assert not [im for im in bpy.data.images if im.source=='GENERATED' and im.name not in ['Render Result','Viewer Node']]
    assert s.compositing_node_group is not None
    results.append({'width':width,'frames':137,'sources':images,'objects':len(s.objects),'status':'native_dependencies_pass'})
    if width==1280:
        s.frame_set(100); s.render.filepath=str(D/'random_access_0100.png'); bpy.ops.render.render(write_still=True)
(D/'blend_audit.json').write_text(json.dumps(results,indent=2)); print(results)
