import bpy
s=bpy.context.scene
print('SCENE',[(p.identifier,p.type) for p in s.bl_rna.properties if 'compos' in p.identifier or 'node' in p.identifier])
g=bpy.data.node_groups.new('test','CompositorNodeTree')
for kind in ['CompositorNodeLensdist','CompositorNodeMovieClip','CompositorNodeImage','NodeGroupOutput']:
 try:
  n=g.nodes.new(kind);print(kind,[(i.name,i.identifier) for i in n.inputs],[(o.name,o.identifier) for o in n.outputs])
 except Exception as e:print(e)
