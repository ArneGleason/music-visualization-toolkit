import bpy,json,pathlib
base=pathlib.Path('projects/a-right-little-something')
out=base/'generated/storyboard/opening-v02'
bpy.ops.wm.open_mainfile(filepath=str((out/'opening-storyboard-v01.blend').resolve()))
shots={s.get('shot_id'):s for s in bpy.data.scenes if s.get('shot_id')}
assert len(shots)==5,shots
report={}
for ident,scene in shots.items():
    bpy.context.window.scene=scene
    network=next(o for o in scene.objects if o.name.startswith('Thin field /'))
    shell=next(o for o in scene.objects if o.name.startswith('Clear spherical cabin'))
    assert network['hexagonal_cells']==150 and network['pentagonal_closures']==12
    nodes=shell.data.materials[0].node_tree.nodes
    assert not any(n.type in ('BSDF_PRINCIPLED','BSDF_GLASS','FRESNEL') for n in nodes)
    report[ident]={'frames':scene.frame_end,'fieldCells':[150,12],'clearShell':True,'retained':scene.use_fake_user}
for left,right in [('opening-002','opening-003'),('opening-003','opening-004')]:
    a,b=shots[left],shots[right]
    bpy.context.window.scene=a;a.frame_set(a.timeline_markers['EDIT OUT'].frame-1)
    pos=a.camera.location.copy();rot=a.camera.rotation_euler.copy();lens=a.camera.data.lens
    bpy.context.window.scene=b;b.frame_set(b.timeline_markers['EDIT IN'].frame)
    assert (pos-b.camera.location).length<.001
    assert max(abs(x-y) for x,y in zip(rot,b.camera.rotation_euler))<.001
    assert abs(lens-b.camera.data.lens)<.001
report['matchedCutCameras']=['002→003','003→004']
(out/'field-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
