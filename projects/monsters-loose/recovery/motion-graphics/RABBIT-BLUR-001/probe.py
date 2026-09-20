import bpy
s=bpy.context.scene
print('SCENE',[(p.identifier,p.type) for p in s.bl_rna.properties if 'composit' in p.identifier or 'node' in p.identifier])
t=bpy.data.node_groups.new('Probe','CompositorNodeTree')
for typ in ['CompositorNodeBlur','CompositorNodeDBlur','CompositorNodeMixRGB','CompositorNodeImage','CompositorNodeOutputFile']:
 try:
  n=t.nodes.new(typ);print(typ,'inputs',[(i.name,i.identifier) for i in n.inputs]);print('properties',[(p.identifier,p.type) for p in n.bl_rna.properties if p.identifier in ['iterations','angle','distance','size_x','size_y','filter_type','use_relative','factor_x','factor_y','use_alpha','base_path','file_slots']])
 except Exception as e: print(e)
