import bpy
n=bpy.data.node_groups.new('test','CompositorNodeTree')
for k in ['CompositorNodeTransform','CompositorNodeScale']:
 a=n.nodes.new(k);print(k,[(i.name,str(i.default_value) if hasattr(i,'default_value') else '') for i in a.inputs])
