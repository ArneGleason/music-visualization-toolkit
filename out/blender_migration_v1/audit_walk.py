from pathlib import Path
import bpy,json
O=Path(__file__).resolve().parent;D=O/'walk';records=[]
for width in [1280,1920]:
    bpy.ops.wm.open_mainfile(filepath=str(D/f'walk_{width}.blend'));s=bpy.context.scene
    assert (s.frame_start,s.frame_end,s.render.fps,s.render.resolution_x,s.render.resolution_y)==(1,102,24,width,width*9//16)
    images=[]
    for im in bpy.data.images:
        if im.source not in ['FILE','SEQUENCE','MOVIE']:continue
        p=Path(bpy.path.abspath(im.filepath)).resolve();assert p.exists() and p.is_relative_to((D/'plates').resolve());images.append(str(p))
    assert len(images)==1 and s.compositing_node_group is not None
    assert not [im for im in bpy.data.images if im.source=='GENERATED' and im.name not in ['Render Result','Viewer Node']]
    records.append({'width':width,'images':images,'status':'source_only_dependencies_pass'})
    if width==1280:
        for f in [40,78]:
            s.frame_set(f);s.render.filepath=str(D/f'random_access_{f:04d}.png');bpy.ops.render.render(write_still=True)
(D/'blend_audit.json').write_text(json.dumps(records,indent=2))
