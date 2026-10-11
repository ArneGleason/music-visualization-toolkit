import bpy
n=bpy.data.node_groups.new('inspect','CompositorNodeTree')
a=n.nodes.new('CompositorNodeOutputFile')
for obj in [a.format]:
 for p in obj.bl_rna.properties:
  print(p.identifier,p.type,getattr(obj,p.identifier,None))
  if p.type=='ENUM': print([i.identifier for i in p.enum_items])
print([(p.identifier,p.type) for p in a.file_output_items.bl_rna.functions['new'].parameters])
it=a.file_output_items.new('RGBA','Image')
print('ITEM',[(p.identifier,p.type) for p in it.bl_rna.properties])
