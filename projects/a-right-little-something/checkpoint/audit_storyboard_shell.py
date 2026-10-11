import bpy, bmesh, json
from pathlib import Path
bpy.ops.wm.open_mainfile(filepath=str(Path('projects/a-right-little-something/generated/storyboard/opening-v01/opening-storyboard-v01.blend').resolve()))
scene=next(s for s in bpy.data.scenes if s.get('shot_id')=='opening-005')
bpy.context.window.scene=scene
ring=next(o for o in scene.objects if o.name.startswith('Broad equatorial band'))
mesh=bmesh.new();mesh.from_mesh(ring.data)
shell=next(o for o in scene.objects if o.name.startswith('Clear spherical cabin'))
report={'ringBoundaryEdges':sum(e.is_boundary for e in mesh.edges),'ringNonManifoldEdges':sum(not e.is_manifold for e in mesh.edges),'shellModifiers':[m.type for m in shell.modifiers],'shellMaterial':shell.data.materials[0].name,'cameraClipStart':scene.camera.data.clip_start,'minimumShellClearance':scene.get('minimum_camera_shell_clearance')}
Path('projects/a-right-little-something/generated/storyboard/opening-v01/glass-audit.json').write_text(json.dumps(report,indent=2))
print(report)
