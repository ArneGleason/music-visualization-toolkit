import bpy
scene=bpy.context.scene
for name, data in [('render',scene.render),('cycles',scene.cycles)]:
    print(name,[(p.identifier,p.description) for p in data.bl_rna.properties if 'motion' in p.identifier or 'shutter' in p.identifier])
bpy.ops.mesh.primitive_uv_sphere_add()
print('object cycles',[(p.identifier,p.description) for p in bpy.context.object.cycles.bl_rna.properties if 'motion' in p.identifier])
