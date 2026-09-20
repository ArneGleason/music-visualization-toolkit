import bpy
n=bpy.data.node_groups.new('P','CompositorNodeTree')
for typ in ['CompositorNodeDBlur','CompositorNodeBlur','ShaderNodeMix','CompositorNodeMix','CompositorNodeComposite','CompositorNodeOutputFile']:
 try:
  t=n.nodes.new(typ)
  print(typ,[(s.name,s.type,str(getattr(s,'default_value',None))) for s in t.inputs]);print([(p.identifier,p.type) for p in t.bl_rna.properties if p.identifier not in ['rna_type']][-20:])
 except Exception as e:print(typ,str(e))
